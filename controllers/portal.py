from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.tools import float_round
import logging

_logger = logging.getLogger(__name__)


class PortalPosController(CustomerPortal):

    @http.route('/my/pos_order/new', type='http', auth="user", website=True)
    def portal_new_pos_order(self, search=None, show_all_products=False, **kw):
        values = self._prepare_portal_layout_values()

        base_domain = [
            ('product_tmpl_id.available_in_pos', '=', True),
        ]

        products = request.env['product.product'].sudo()

        if search:
            domain = base_domain + ['|', ('name', 'ilike', search), ('default_code', 'ilike', search)]
            products = products.search(domain, order="name asc")
        elif show_all_products:
            products = products.search(base_domain, order="name asc")
            search = None
        else:
            products = request.env['product.product']

        _logger.info("Products found for portal_new_pos_order (search=%s, show_all_products=%s): %s", search, show_all_products, products.mapped('name'))
        _logger.info("Number of products found: %s", len(products))

        values.update({
            'products': products,
            'page_name': 'new_pos_order',
            'search': search,
            'show_all_products': show_all_products,
        })
        return request.render("pos_portal_integration.portal_new_pos_order_template", values)


    @http.route('/my/pos_order/create', type='http', auth="user", website=True, csrf=True)
    def portal_create_pos_order(self, **post):
        order_lines = []
        partner = request.env.user.partner_id
        current_company = request.env.company

        pos_config = request.env['pos.config'].sudo().search([], limit=1)
        if not pos_config:
            return request.render('pos_portal_integration.no_pos_config_found_template', {})

        pricelist = pos_config.pricelist_id or partner.property_product_pricelist.sudo() or request.env['product.pricelist'].sudo().search([], limit=1)
        if not pricelist:
            return request.render('pos_portal_integration.no_pricelist_found_template', {})

        fiscal_position = partner.property_account_position_id.sudo() or \
                            (pos_config.fiscal_position_ids.sudo().filtered(lambda fp: fp.active)[:1] or False)

        request.env.cr.execute('SAVEPOINT portal_pos_create')
        try:
            amount_tax_total = 0.0
            amount_untaxed_total = 0.0

            for key, value in post.items():
                if key.startswith('product_') and int(value) > 0:
                    product_id = int(key.replace('product_', ''))
                    product = request.env['product.product'].sudo().browse(product_id)
                    if not product.exists():
                        _logger.warning("Product ID %s from portal form does not exist. Skipping.", product_id)
                        continue

                    qty = int(value)
                    product_context = {
                        'pricelist': pricelist.id,
                        'quantity': qty,
                        'company_id': current_company.id,
                        'partner_id': partner.id,
                        'fiscal_position': fiscal_position.id if fiscal_position else False,
                    }

                    price_unit = product.with_context(**product_context).price_compute('list_price')[product.id]
                    price_unit = float_round(price_unit, precision_digits=request.env['decimal.precision'].sudo().precision_get('Product Price'))

                    taxes = product.taxes_id.filtered(lambda t: t.company_id == current_company)
                    if fiscal_position:
                        taxes = fiscal_position.map_tax(taxes)

                    tax_result = taxes.compute_all(price_unit, quantity=qty, product=product, partner=partner)
                    subtotal_excl = tax_result['total_excluded']
                    subtotal_incl = tax_result['total_included']

                    amount_untaxed_total += subtotal_excl
                    amount_tax_total += subtotal_incl - subtotal_excl

                    line_vals = {
                        'product_id': product.id,
                        'qty': qty,
                        'price_unit': price_unit,
                        'name': product.name,
                        'tax_ids': [(6, 0, taxes.ids)],
                        'price_subtotal': subtotal_excl,
                        'price_subtotal_incl': subtotal_incl,
                    }
                    order_lines.append((0, 0, line_vals))

            if order_lines:
                session = request.env['pos.session'].sudo().search([('state', '=', 'opened')], limit=1)
                if not session:
                    return request.render('pos_portal_integration.no_open_session_template', {})

                amount_total = amount_untaxed_total + amount_tax_total

                pos_order = request.env['pos.order'].sudo().create({
                    'partner_id': partner.id,
                    'portal_user_id': request.env.user.id,
                    'lines': order_lines,
                    'portal_order': True,
                    'session_id': session.id,
                    'pricelist_id': pricelist.id,
                    'fiscal_position_id': fiscal_position.id if fiscal_position else False,
                    'company_id': current_company.id,
                    'amount_tax': amount_tax_total,
                    'amount_total': amount_total,
                    'amount_paid': 0.0,
                    'amount_return': 0.0,
                    'state': 'draft',
                })

                # --- NEW: Create notification activity in the backend ---
                activity_type_todo = request.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False).sudo()
                pos_manager_group = request.env.ref('point_of_sale.group_pos_manager', raise_if_not_found=False).sudo()
                pos_order_model_id = request.env.ref('point_of_sale.model_pos_order', raise_if_not_found=False).sudo().id

                customer_name = request.env.user.partner_id.display_name # Get the customer's display name

                if activity_type_todo and pos_manager_group and pos_order_model_id:
                    for user in pos_manager_group.users.sudo():
                        if user.has_group('point_of_sale.group_pos_manager') or user.has_group('point_of_sale.group_pos_user'):
                            request.env['mail.activity'].sudo().create({
                                'res_id': pos_order.id,
                                'res_model_id': pos_order_model_id,
                                'activity_type_id': activity_type_todo.id,
                                # --- CUSTOMIZED SUMMARY AND NOTE ---
                                'summary': f"URGENT: New Orders from {customer_name} - Immediate Attention Required!",
                                'note': f"{customer_name} has just placed a new POS Order (Reference: {pos_order.name}, Total: {pos_order.amount_total:.2f} {pos_order.currency_id.symbol}). Please attend to this order without delay to ensure prompt processing.",
                                # --- END CUSTOMIZATION ---
                                'user_id': user.id,
                                'date_deadline': fields.Date.today(),
                            })
                elif not activity_type_todo:
                    _logger.warning("Activity type 'To Do' (mail.mail_activity_data_todo) not found for notification.")
                elif not pos_manager_group:
                    _logger.warning("POS Manager group (point_of_sale.group_pos_manager) not found for notification.")
                elif not pos_order_model_id:
                     _logger.warning("POS Order model ID (point_of_sale.model_pos_order) not found for notification.")

                # --- END NEW ---

                payment_method = pos_config.payment_method_ids.sudo()[:1]
                if not payment_method:
                    return request.render('pos_portal_integration.no_payment_method_found_template', {})

                request.env['pos.payment'].sudo().create({
                    'amount': amount_total,
                    'payment_date': fields.Date.today(),
                    'payment_method_id': payment_method.id,
                    'pos_order_id': pos_order.id,
                    'session_id': session.id,
                    'name': 'Portal Payment',
                })

            request.env.cr.execute('RELEASE SAVEPOINT portal_pos_create')
        except Exception as e:
            request.env.cr.execute('ROLLBACK TO SAVEPOINT portal_pos_create')
            _logger.exception("Error creating POS order from portal: %s", e)
            raise

        return request.redirect('/my/pos_orders')

    @http.route(['/my/pos_orders', '/my/pos_orders/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_pos_orders(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PosOrder = request.env['pos.order'].sudo()

        domain = [('partner_id', '=', partner.id)]
        pos_order_count = PosOrder.search_count(domain)

        pager = request.website.pager(
            url="/my/pos_orders",
            total=pos_order_count,
            page=page,
            step=self._items_per_page
        )

        pos_orders = PosOrder.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'pos_orders': pos_orders,
            'page_name': 'pos_orders',
            'pager': pager,
            'default_url': '/my/pos_orders',
            'pos_order_count': pos_order_count,
        })
        return request.render("pos_portal_integration.portal_my_pos_orders_template", values)

    @http.route('/my/pos_order/<int:order_id>', type='http', auth="user", website=True)
    def portal_pos_order_detail(self, order_id, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PosOrder = request.env['pos.order'].sudo()
        pos_order = PosOrder.search([('id', '=', order_id), ('partner_id', '=', partner.id)], limit=1)

        if not pos_order:
            return request.render("website.404")

        values.update({
            'pos_order': pos_order,
            'page_name': 'pos_order_detail',
        })
        return request.render("pos_portal_integration.portal_my_pos_order_detail_template", values)

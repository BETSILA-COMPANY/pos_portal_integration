from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # POS Availability (now directly on product, not just related)
    available_in_pos = fields.Boolean(
        string="Available in POS",
        default=True,
        help="Whether this product variant is available in Point of Sale"
    )

    # POS Specific Pricing
    pos_price = fields.Float(
        string="POS Price",
        digits='Product Price',
        help="Special price for POS orders. Falls back to list price if empty."
    )

    # Inventory Fields
    qty_available = fields.Float(
        string="Quantity On Hand",
        compute='_compute_qty_available',
        store=True,
        help="Current inventory quantity"
    )

    # Portal Product Methods
    @api.model
    def get_portal_products(self):
        """Get products available for portal ordering"""
        return self.search([
            ('available_in_pos', '=', True),
            ('sale_ok', '=', True),
            ('active', '=', True)
        ])

    def get_portal_product_data(self):
        """Get structured product data for portal display"""
        self.ensure_one()
        return {
            'id': self.id,
            'name': self.name,
            'default_code': self.default_code,
            'pos_price': self.pos_price or self.lst_price,
            'image': self.image_1920,
            'uom': self.uom_id.name,
            'available_qty': self.qty_available,
            'barcode': self.barcode
        }

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def _compute_qty_available(self):
        """Compute actual quantity available"""
        for product in self:
            product.qty_available = product.with_context(warehouse=False).free_qty

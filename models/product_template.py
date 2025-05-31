from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # POS Availability at template level
    available_in_pos = fields.Boolean(
        string="Available in POS",
        default=True,
        help="Whether this product is available in Point of Sale",
        company_dependent=True
    )

    # POS Category (corrected model name)
    pos_category_id = fields.Many2one(
        'pos.category',
        string="POS Category",
        help="Category used in Point of Sale"
    )

    # POS-specific Price
    pos_price = fields.Float(
        string="POS Price",
        digits='Product Price',
        help="Price used specifically in Point of Sale"
    )

    # Make variants inherit POS availability
    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            template.product_variant_ids.write({
                'available_in_pos': template.available_in_pos
            })
        return templates

    def write(self, vals):
        res = super().write(vals)
        if 'available_in_pos' in vals:
            self.mapped('product_variant_ids').write({
                'available_in_pos': vals['available_in_pos']
            })
        return res


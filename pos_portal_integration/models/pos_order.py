# pos_portal_integration/models/pos_order.py
from odoo import models, fields
from odoo.addons.mail.models.mail_thread import MailThread
from odoo.addons.mail.models.mail_activity_mixin import MailActivityMixin

class PosOrder(models.Model, MailThread, MailActivityMixin):
    _inherit = 'pos.order'

    portal_order = fields.Boolean(string="Portal Order", default=False)
    portal_user_id = fields.Many2one('res.users', string="Portal User", readonly=True)
    portal_state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted to POS'),
        ('confirmed', 'Confirmed by POS'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled')
    ], string="Portal State", default='draft', tracking=True)

    def action_submit_to_pos(self):
        self.write({'portal_state': 'submitted'})

    def action_confirm_in_pos(self):
        self.write({'portal_state': 'confirmed'})

    def action_mark_as_paid(self):
        self.write({'portal_state': 'paid'})

    # Optional: auto-set portal_user_id on create
    # @api.model
    # def create(self, vals):
    #     if vals.get('portal_order') and not vals.get('portal_user_id'):
    #         vals['portal_user_id'] = self.env.user.id
    #     return super().create(vals)


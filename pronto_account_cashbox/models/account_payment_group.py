from odoo import models, fields, api


class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    cancel_reason_note = fields.Char("Detalle el motivo de la cancelación",tracking=True)

    cashbox_session_id = fields.Many2one(
                                'account.cashbox.session',
                                string="Sesión de caja",
                                compute="_compute_cashbox_session_id",
                                store=True,)
    
    cashbox_id = fields.Many2one(
        related='cashbox_session_id.cashbox_id',
        store=True,
    )

    @api.depends("payment_ids.cashbox_session_id")
    def _compute_cashbox_session_id(self):
        for rec in self:
            if rec.payment_ids:
                rec.cashbox_session_id = rec.payment_ids[0].cashbox_session_id
            else:
                rec.cashbox_session_id = False

    def name_get(self):
        """ Add check number to display_name on check_id m2o field """
        res_names = super().name_get()
        for i, (res_name, rec) in enumerate(zip(res_names, self)):
            res_names[i] = (res_name[0], "%s %s" % (res_name[1], " - {}".format(rec.partner_id.name)))
                
        return res_names
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountCashboxSession(models.Model):
    _inherit = 'account.cashbox.session'

    arqueo_inicial_realizado = fields.Boolean('Arqueo realizado',default=False)

    session_journal_ids = fields.Many2many(
        comodel_name='account.journal',
        compute='_compute_session_journal_ids'
    )

    session_cash_control_journal_ids = fields.Many2many(
        comodel_name='account.journal',
        compute='_compute_session_journal_ids'
    )

    def action_account_cashbox_session_open(self):
        super(AccountCashboxSession,self).action_account_cashbox_session_open()
        for session in self:
            if not session.arqueo_inicial_realizado:
                raise ValidationError("El arqueo inicial está pendiente.")
            session.closing_date = False

    def action_cashbox_expense(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gastos',
            'view_mode': 'form',
            'res_model': 'account.cashbox.expense.wizard',
            'target': 'new',
            'context': {
                'tipo_de_movimiento': 'gasto',}
        }

    def action_cashbox_recibo(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cobrar en Efectivo',
            'view_mode': 'form',
            'res_model': 'account.cashbox.expense.wizard',
            'target': 'new',
            'context': {
                'tipo_de_movimiento': 'recibo',}
        }

    def action_cashbox_pago(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pagar en Efectivo',
            'view_mode': 'form',
            'res_model': 'account.cashbox.expense.wizard',
            'target': 'new',
            'context': {
                'tipo_de_movimiento': 'pago',}
        }

    @api.depends('cashbox_id')
    def _compute_session_journal_ids(self):
        for rec in self:
            rec.session_journal_ids = rec.cashbox_id.journal_ids.filtered(lambda x: x in rec.line_ids.mapped('journal_id'))
            rec.session_cash_control_journal_ids = rec.session_journal_ids.filtered(lambda x: x in rec.cashbox_id.cash_control_journal_ids)

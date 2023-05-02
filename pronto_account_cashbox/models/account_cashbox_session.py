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

    session_bank_control_journal_ids = fields.Many2many(
        comodel_name='account.journal',
        compute='_compute_session_journal_ids'
    )

    transfer_in_ids = fields.One2many('account.cashbox.transfer', 'destination_cashbox_session_id')
    transfer_in_count = fields.Integer(
        string="Transferencias Recibidas", compute="_compute_transfers"
    )

    transfer_out_ids = fields.One2many('account.cashbox.transfer', 'origin_cashbox_session_id')
    transfer_out_count = fields.Integer(
        string="Transferencias Enviadas", compute="_compute_transfers"
    )

    transfer_in_pending_ids = fields.One2many('account.cashbox.transfer', related='cashbox_id.transfer_in_pending_ids')
    transfer_in_pending_count = fields.Integer(
        string="Transf. Pendientes", related='cashbox_id.transfer_in_pending_count'
    )

    @api.depends("transfer_in_ids", "transfer_out_ids")
    def _compute_transfers(self):
        for session in self:
            session.transfer_in_count = len(session.transfer_in_ids)
            session.transfer_out_count = len(session.transfer_out_ids)
            # if session.transfer_out_count > 0:
            #     import pdb; pdb.set_trace()

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

    def action_session_transfers_out(self):
        view = self.env.ref('pronto_account_cashbox.account_cashbox_transfer_view_tree')
        return {
            'name': self.name,
            'view_mode': 'tree,form',
            'res_model': 'account.cashbox.transfer',
            'domain': [('origin_cashbox_session_id', '=', self.id)],
            # 'view_id': view.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            # 'context': {'search_default_state_posted':True},
        }

    def action_session_transfers_in(self):
        view = self.env.ref('pronto_account_cashbox.account_cashbox_transfer_view_tree')
        return {
            'name': self.name,
            'view_mode': 'tree,form',
            'res_model': 'account.cashbox.transfer',
            'domain': [('destination_cashbox_session_id', '=', self.id)],
            # 'view_id': view.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            # 'context': {'search_default_state_posted':True},
        }

    def action_session_transfers_pending(self):
        view = self.env.ref('pronto_account_cashbox.account_cashbox_transfer_view_tree')
        return {
            'name': self.name,
            'view_mode': 'tree,form',
            'res_model': 'account.cashbox.transfer',
            'domain': [('destination_cashbox_id', '=', self.cashbox_id.id),('state','=','sent')],
            # 'view_id': view.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            # 'context': {'search_default_state_posted':True},
        }

    def action_cashbox_move(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Operaciones varias',
            'view_mode': 'form',
            'res_model': 'account.cashbox.move.wizard',
            'target': 'new',
            # 'context': {
            #     'tipo_de_movimiento': 'recibo',}
        }

    def action_cashbox_vendor_bill(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cargar Compra',
            'view_mode': 'form',
            'res_model': 'account.cashbox.vendor.bill.wizard',
            'target': 'new',
        }

    def action_session_transactions(self):
        # view = self.env.ref('account.view_account_payment_tree')
        return {
            'name': self.name,
            'view_mode': 'tree',
            'res_model': 'account.payment',
            'domain': [('cashbox_session_id', '=', self.id)],
            # 'view_id': view.id,
            'type': 'ir.actions.act_window',
            'context': {'search_default_state_posted':True},
        }
    
    @api.depends('cashbox_id','cashbox_id.journal_ids','cashbox_id.cash_control_journal_ids')
    def _compute_session_journal_ids(self):
        for rec in self:
            rec.session_journal_ids = rec.cashbox_id.journal_ids.filtered(lambda x: x in rec.line_ids.mapped('journal_id'))
            rec.session_cash_control_journal_ids = rec.session_journal_ids.filtered(lambda x: x in rec.cashbox_id.cash_control_journal_ids)
            rec.session_bank_control_journal_ids = rec.session_journal_ids.filtered(lambda x: x.type == 'bank')

    def action_session_payments(self):        
        action = super(AccountCashboxSession,self).action_session_payments()
        search_default_journal_id = self.env.context.get('search_default_journal_id', False)
        if search_default_journal_id:
            domain = [('cashbox_session_id', '=', self.id),('journal_id', '=', search_default_journal_id)]
            search_default_journal = False
        else:
            domain =  [('cashbox_session_id', '=', self.id)]
            search_default_journal = True

        action["domain"] = domain
        action["context"]["search_default_journal"] = search_default_journal
        return action
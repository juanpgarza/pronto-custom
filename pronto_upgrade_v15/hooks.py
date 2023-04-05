from odoo import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    payments = env['account.payment'].search([]).filtered(lambda x: x.is_internal_transfer 
                                                    and not x.is_matched 
                                                    and not x.paired_internal_transfer_payment_id
                                                    and x.journal_id.id in (52,29,40,37,53,13,17,16,15,14)) 

    for payment in payments:
        # import pdb; pdb.set_trace()
        payment._create_paired_internal_transfer_payment()
        
    _logger.info("{} pagos creados".format(len(payments)))

    # raise ValidationError("Listo")

    # account_payment_obj = env["account.payment"]

    # query = """
    #     select
    #     ac."number",
    #     ac.bank_id,
    #     ac.payment_date,
    #     ap.id as account_payment_id,
    #     ap.payment_type
    #     from account_check_account_payment_rel acapr
    #     left join account_check ac on ac.id = acapr.account_check_id 
    #     left join account_payment ap on ap.id = acapr.account_payment_id 
    #     where account_check_id = 1
    # """
    
    # cr.execute(query)

    # checks = cr.dictfetchall()
    # for check in checks:
    #     account_payment = account_payment_obj.browse(check["account_payment_id"])

    #     if check["payment_type"] == 'inbound':
    #         # es el cheque, osea, el payment original
    #         vals = {
    #             'check_number': check["account_payment_id"],
    #             'l10n_latam_check_bank_id': check["bank_id"], 
    #             'l10n_latam_check_payment_date': check["date"], 

    #         }
    #         _logger.info("Cheque Nro {}".format(check["account_payment_id"]))
    #     else:
    #         _logger.info("Cheque Nro {}".format(check["account_payment_id"]))

    #     # account_payment.write(vals)

    # raise ValidationError("Listo")
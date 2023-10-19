##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
from odoo.tools import config

class ProntoWebsiteSale(WebsiteSale):

    @route()
    def confirm_order(self, **post):
        res = super().confirm_order(**post)
        order = request.website.sale_get_order()
        # import pdb; pdb.set_trace()
        if order.partner_id.user_id:
            order.user_id = order.partner_id.user_id
        
        notification_ids = []
        notification_ids.append((0,0,{
                'res_partner_id':order.user_id.id}))        
        order.message_post(
            body='Se confirmó el pedido!', 
            message_type='notification', 
            # subtype='mail.mt_comment',
            notification_ids=notification_ids)

        return res           
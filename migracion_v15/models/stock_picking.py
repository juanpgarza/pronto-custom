# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def default_get(self, defaul_fields):
        res = super().default_get(defaul_fields)
        # import pdb; pdb.set_trace()
        # if not res.get('location_id'):
        #     res['location_id'] = 8
        # if not res.get('location_dest_id'):
        #     res['location_dest_id'] = 5            
        return res

    
    def _set_scheduled_date(self):
        # import pdb; pdb.set_trace()
        for picking in self:
            picking.move_lines.write({'date': picking.scheduled_date})
        # for picking in self:
        #     if picking.state in ('done', 'cancel'):
        #         raise UserError(_("You cannot change the Scheduled Date on a done or cancelled transfer."))
        #     picking.move_lines.write({'date': picking.scheduled_date})

    def write(self, vals):
        if vals.get('picking_type_id') and any(picking.state != 'draft' for picking in self):
            return True
        # import pdb; pdb.set_trace()
        return super().write(vals)
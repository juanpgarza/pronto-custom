# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.model
    def asignar_identificador_externo(self):

        ##### xmlrpc_migration.stock_warehouse_11 # Felix SM 1140
        warehouse_id = self.env.ref('xmlrpc_migration.stock_warehouse_11')
        prefijo = "stock_picking_type_"
        #
        identificador = prefijo + '78'
        ext_id = self.env["ir.model.data"].search([('module','=','xmlrpc_migration'),('name','=',identificador)])

        if not ext_id:
            type_id = self.env[self._name].search([('name','=','Receipts'), ('code','=','incoming'), ('warehouse_id','=',warehouse_id.id) ])

            self.crear_external_id(identificador, type_id)

        #
        identificador = prefijo + '79'
        ext_id = self.env["ir.model.data"].search([('module','=','xmlrpc_migration'),('name','=',identificador)])

        if not ext_id:
            type_id = self.env[self._name].search([('code','=','outgoing'), ('warehouse_id','=',warehouse_id.id) ])

            self.crear_external_id(identificador, type_id)

        return True

    def crear_external_id(self, name, res_id):

        vals = {
            'module': 'xmlrpc_migration',
            'model': self._name,
            'name': name,
            'res_id': res_id.id,
        }

        return self.env["ir.model.data"].create(vals)


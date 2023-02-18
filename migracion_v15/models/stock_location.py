# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    @api.model
    def asignar_identificador_externo(self):

        prefijo = "stock_location_"
        #
        identificador = prefijo + '100'
        ext_id = self.env["ir.model.data"].search([('module','=','xmlrpc_migration'),('name','=',identificador)])

        if not ext_id:
            loc_id_parent = self.env[self._name].search([('name','=','FSM2')])

            self.crear_external_id(identificador, loc_id_parent)
        # else:
        #     loc_id_parent = ext_id

        #
        identificador = prefijo + '101'
        ext_id = self.env["ir.model.data"].search([('module','=','xmlrpc_migration'),('name','=',identificador)])

        if not ext_id:
            loc_id = self.env[self._name].search([('name','=','Stock'),('location_id','=',loc_id_parent.id)])

            self.crear_external_id(identificador, loc_id)

        return True

    def crear_external_id(self, name, res_id):

        vals = {
            'module': 'xmlrpc_migration',
            'model': self._name,
            'name': name,
            'res_id': res_id.id,
        }

        return self.env["ir.model.data"].create(vals)

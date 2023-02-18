# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    # def message_track(self, tracked_fields, initial_values):
    #     # tracked_fields = {}
    #     import wdb; wdb.set_trace()
    #     return super().message_track(tracked_fields, initial_values)
        # return True

    def _finalize_tracking(self):
        # para que no registre la modificación de los campos en el chatter
        # no encontre un context y me seguia registrando los campos en los montos de las líneas de las SO
        return

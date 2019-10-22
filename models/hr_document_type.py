# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class HrDocumentType(models.Model):
    _name = 'hr.document.type'
    _order = 'sequence, name'


    # Compute and search fields

    def _compute_documents_number(self):
        Documents = self.env['hr.documents']

        for record in self:
            docs = Documents.search([('document_type', '=', record.id)])
            # tutti i documenti
            record.documents_number = len(docs)
            # documenti con una data di scadenza minore della soglia impostata
            record.warning_number = len(docs.filtered(lambda x: x.days_left > 0 and x.days_left < x.default_warning_limit_date_hr))
            # documenti con una data di scadenza superata
            record.alert_number = len(docs.filtered(lambda x: x.days_left == 0))


    # Fields declaration

    name = fields.Char(
        string='Name',
        required=True
    )

    warning_limit_date_hr = fields.Integer(
        string='Warning limit date',
        default=15
    )

    documents_number = fields.Integer(
        string='Number of documents',
        compute=_compute_documents_number,
        readonly=True
    )

    warning_number = fields.Integer(
        string='Number of warnings',
        compute=_compute_documents_number,
        readonly=True
    )

    alert_number = fields.Integer(
        string='Number of alerts',
        compute=_compute_documents_number,
        readonly=True
    )

    sequence = fields.Integer(
        string='Sequence',
        default=20
    )


    # Action methods

    @api.multi
    def action_show_folder_documents(self):
        action_id = self.env.ref('hr_cgt.view_hr_documents_action').read()[0]
        # ctx = action_id['context'].copy()

        ctx = {
            'search_default_document_type': self.id
        }

        action_id['context'] = ctx
        return action_id

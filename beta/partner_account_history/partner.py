# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
import tools


class partner_account_history(orm.Model):
    _name = 'partner.account.history'
    _auto = False

    def allopen(self, cr, uid, ids, context=None):
        models = self.pool.get('ir.model.data')
        inv_view = models.get_object_reference(
            cr, uid, 'account', 'invoice_form'
        )
        inv_view_id = inv_view and inv_view[1] or False

        vou_view = models.get_object_reference(
            cr, uid, 'account_voucher', 'view_voucher_form'
        )
        vou_view_id = vou_view and vou_view[1] or False

        mov_view = models.get_object_reference(
            cr, uid, 'account', 'view_move_form'
        )
        mov_view_id = mov_view and mov_view[1] or False

        if not context:
            context = {}

        inv_id = self.browse(cr, uid, ids[0]).iid.id
        vou_id = self.browse(cr, uid, ids[0]).vid.id
        mov_id = self.browse(cr, uid, ids[0]).midd.id

        inv_type = self.browse(cr, uid, ids[0]).t

        if inv_type == 'Supplier Invoice' or inv_type == 'Supplier Credit':
            # invoice_type_to_return = 'out_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [inv_view_id],
                'res_model': 'account.invoice',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': inv_id,
            }
        elif inv_type == 'Customer Credit' or inv_type == 'Customer Invoice':
            # invoice_type_to_return = 'in_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [inv_view_id],
                'res_model': 'account.invoice',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': inv_id,
            }
        elif inv_type == 'Supplier Payment' or inv_type == 'Purchase Receipt':
            # invoice_type_to_return = 'out_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [vou_view_id],
                'res_model': 'account.voucher',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': vou_id,
            }
        elif inv_type == 'Customer Payment' or inv_type == 'Sales Receipt':
            # invoice_type_to_return = 'in_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [vou_view_id],
                'res_model': 'account.voucher',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': vou_id,
            }
        else:
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [mov_view_id],
                'res_model': 'account.move',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': mov_id,
            }

        return dic_to_ret

    _columns = {
        'p': fields.many2one('res.partner', 'Partner'),
        'ic': fields.boolean('Customer'),
        'iss': fields.boolean('Supplier'),
        'iid': fields.many2one('account.invoice', 'Related Document'),
        'vid': fields.many2one('account.voucher', 'Related Document'),
        'midd': fields.many2one('account.move', 'Related Document'),
        'e': fields.char('Entered', size=10),
        'ef': fields.char('Effective', size=10),
        'efd': fields.date('Effective'),
        'd': fields.char('Due', size=10),
        'pn': fields.char('Name', size=128),
        'doc': fields.char('Document', size=128),
        'r': fields.char('Reference/Number', size=128),
        't': fields.char('Type', size=24),
        's': fields.char('State', size=24),
        'oa': fields.float('Original Amount', digits=(12, 2)),
        'b': fields.float('Balance', digits=(12, 2)),
    }

    _order = "pn, efd"

    def init(self, cr):
        query = """
SELECT cast(100000000000 + ai.id AS bigint) AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       ai.id AS IID,
       0 AS VID,
       0 AS MIDD,
       to_char(ai.create_date,'MM-DD-YYYY') AS E,
       to_char(date_invoice,'MM-DD-YYYY') AS EF,
       date_invoice AS efd,
       to_char(date_due,'MM-DD-YYYY') AS D,
       ai.supplier_invoice_number AS DOC,
       number AS R,
       'Supplier Invoice' AS T,
       CASE
           WHEN STATE ='draft' THEN 'Draft'
           WHEN STATE ='proforma2' THEN 'Pro-forma'
           WHEN STATE ='proforma' THEN 'Pro-forma'
           WHEN STATE ='paid' THEN 'Paid'
           WHEN STATE = 'open' THEN 'Open'
           WHEN STATE ='cancel' THEN 'Cancelled'
       END AS S,
       amount_total AS OA,
       residual AS B
FROM account_invoice AS ai,
     res_partner AS p
WHERE ai.type = 'in_invoice'
  AND ai.partner_id = p.id
UNION
SELECT cast(100000000000 + ai.id AS bigint) AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       ai.id AS IID,
       0 AS VID,
       0 AS MIDD,
       to_char(ai.create_date,'MM-DD-YYYY') AS E,
       to_char(date_invoice,'MM-DD-YYYY') AS EF,
       date_invoice AS efd,
       to_char(date_due,'MM-DD-YYYY') AS D,
       ai.name AS DOC,
       number AS R,
       'Supplier Credit' AS T,
       CASE
           WHEN STATE ='draft' THEN 'Draft'
           WHEN STATE ='proforma2' THEN 'Pro-forma'
           WHEN STATE ='proforma' THEN 'Pro-forma'
           WHEN STATE ='paid' THEN 'Paid'
           WHEN STATE = 'open' THEN 'Open'
           WHEN STATE ='cancel' THEN 'Cancelled'
       END AS S,
       amount_total AS OA,
       residual AS B
FROM account_invoice AS ai,
     res_partner AS p
WHERE ai.type = 'in_refund'
  AND ai.partner_id = p.id
UNION
SELECT cast(100000000000 + ai.id AS bigint) AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       ai.id AS IID,
       0 AS VID,
       0 AS MIDD,
       to_char(ai.create_date,'MM-DD-YYYY') AS E,
       to_char(date_invoice,'MM-DD-YYYY') AS EF,
       date_invoice AS efd,
       to_char(date_due,'MM-DD-YYYY') AS D,
       ai.internal_number AS DOC,
       number AS R,
       'Customer Invoice' AS T,
       CASE
           WHEN STATE ='draft' THEN 'Draft'
           WHEN STATE ='proforma2' THEN 'Pro-forma'
           WHEN STATE ='proforma' THEN 'Pro-forma'
           WHEN STATE ='paid' THEN 'Paid'
           WHEN STATE = 'open' THEN 'Open'
           WHEN STATE ='cancel' THEN 'Cancelled'
       END AS S,
       amount_total AS OA,
       residual AS B
FROM account_invoice AS ai,
     res_partner AS p
WHERE ai.type = 'out_invoice'
  AND ai.partner_id = p.id
UNION
SELECT cast(100000000000 + ai.id AS bigint) AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       ai.id AS IID,
       0 AS VID,
       0 AS MIDD,
       to_char(ai.create_date,'MM-DD-YYYY') AS E,
       to_char(date_invoice,'MM-DD-YYYY') AS EF,
       date_invoice AS efd,
       to_char(date_due,'MM-DD-YYYY') AS D,
       ai.name AS DOC,
       number AS R,
       'Customer Credit' AS T,
       CASE
           WHEN STATE ='draft' THEN 'Draft'
           WHEN STATE ='proforma2' THEN 'Pro-forma'
           WHEN STATE ='proforma' THEN 'Pro-forma'
           WHEN STATE ='paid' THEN 'Paid'
           WHEN STATE = 'open' THEN 'Open'
           WHEN STATE ='cancel' THEN 'Cancelled'
       END AS S,
       amount_total AS OA,
       residual AS B
FROM account_invoice AS ai,
     res_partner AS p
WHERE ai.type = 'out_refund'
  AND ai.partner_id = p.id
UNION
SELECT av.id AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       0 AS IID,
       av.id AS VID,
       0 AS MIDD,
       to_char(av.create_date,'MM-DD-YYYY') AS E,
       to_char(av.date,'MM-DD-YYYY') AS EF,
       av.date AS efd,
       '' AS D,
       av.name AS DOC,
       reference AS R,
       'Sales Receipt' AS T,
       CASE
           WHEN STATE='draft' THEN 'Draft'
           WHEN STATE='proforma' THEN 'Pro-forma'
           WHEN STATE='posted' THEN 'Posted'
           WHEN STATE= 'cancel' THEN 'Cancelled'
       END AS S,
       amount AS OA,
       0 AS B
FROM account_voucher AS av,
     res_partner AS p
WHERE av.type = 'sale'
  AND av.partner_id = p.id
UNION
SELECT av.id AS id,
       '' AS number,
       customer AS IC,
       supplier AS ISS,
       partner_id AS P,
       p.name AS PN,
       0 AS IID,
       av.id AS VID,
       0 AS MIDD,
       to_char(av.create_date,'MM-DD-YYYY') AS E,
       to_char(av.date,'MM-DD-YYYY') AS EF,
       av.date AS efd,
       '' AS D,
       av.name AS DOC,
       reference AS R,
       'Purchase Receipt' AS T,
       CASE
           WHEN STATE='draft' THEN 'Draft'
           WHEN STATE='proforma' THEN 'Pro-forma'
           WHEN STATE='posted' THEN 'Posted'
           WHEN STATE= 'cancel' THEN 'Cancelled'
       END AS S,
       amount AS OA,
       0 AS B
FROM account_voucher AS av,
     res_partner AS p
WHERE av.type = 'purchase'
  AND av.partner_id = p.id
UNION
SELECT av.id AS id,
       av.number,customer AS IC,
                 supplier AS ISS,
                 partner_id AS P,
                 p.name AS PN,
                 0 AS IID,
                 av.id AS VID,
                 0 AS MIDD,
                 to_char(av.create_date,'MM-DD-YYYY') AS E,
                 to_char(av.date,'MM-DD-YYYY') AS EF,
                 av.date AS efd,
                 '' AS D,
                 av.name AS DOC,
                 number AS R,
                 'Supplier Payment' AS T,
                 CASE
                     WHEN STATE='draft' THEN 'Draft'
                     WHEN STATE='proforma' THEN 'Pro-forma'
                     WHEN STATE='posted' THEN 'Posted'
                     WHEN STATE= 'cancel' THEN 'Cancelled'
                 END AS S,
                 amount AS OA,
                 CASE
                     WHEN
                            (SELECT count(name)
                             FROM account_move_line
                             WHERE name=number) > 1 THEN
                            (SELECT sum(debit) - sum(credit)
                             FROM account_move_line
                             WHERE name =number)
                     ELSE amount
                 END AS B
FROM account_voucher AS av,
     res_partner AS p
WHERE av.type = 'payment'
  AND av.partner_id = p.id
UNION
SELECT av.id AS id,
       av.number,customer AS IC,
                 supplier AS ISS,
                 partner_id AS P,
                 p.name AS PN,
                 0 AS IID,
                 av.id AS VID,
                 0 AS MIDD,
                 to_char(av.create_date,'MM-DD-YYYY') AS E,
                 to_char(av.date,'MM-DD-YYYY') AS EF,
                 av.date AS efd,
                 '' AS D,
                 av.name AS DOC,
                 number AS R,
                 'Customer Payment' AS T,
                 CASE
                     WHEN STATE='draft' THEN 'Draft'
                     WHEN STATE='proform' THEN 'Pro-forma'
                     WHEN STATE='posted' THEN 'Posted'
                     WHEN STATE= 'cancel' THEN 'Cancelled'
                 END AS S,
                 amount AS OA,
                 CASE
                     WHEN
                            (SELECT count(name)
                             FROM account_move_line
                             WHERE name=number) > 1 THEN
                            (SELECT sum(credit) - sum(debit)
                             FROM account_move_line
                             WHERE name =number)
                     ELSE amount
                 END AS B
FROM account_voucher AS av,
     res_partner AS p
WHERE av.type = 'receipt'
  AND av.partner_id = p.id
UNION
SELECT cast(500000000000 + am.id AS bigint) AS id,
       '' AS number,
       p.customer AS IC,
       p.supplier AS ISS,
       am.partner_id AS P,
       p.name AS PN,
       0 AS IID,
       0 AS VID,
       am.id AS MIDD,
       to_char(am.create_date,'MM-DD-YYYY') AS E,
       to_char(am.date,'MM-DD-YYYY') AS EF,
       am.date AS efd,
       '' AS D,
       am.name AS DOC,
       am.ref AS R,
       'Manual Journal' AS T,
       CASE
           WHEN am.STATE='draft' THEN 'Unposted'
           WHEN am.STATE='posted' THEN 'Posted'
       END AS S,
       sum(aml.debit) AS OA,
       0 AS B
FROM account_move am,
     account_move_line aml,
     res_partner AS p
WHERE am.id = aml.move_id
  AND am.partner_id = p.id
  AND am.id NOT IN
    (SELECT DISTINCT move_id
     FROM account_invoice
     WHERE move_id IS NOT NULL)
  AND am.id NOT IN
    (SELECT DISTINCT move_id
     FROM account_voucher
     WHERE move_id IS NOT NULL)
GROUP BY am.id,
         ic,
         iss,
         p,
         pn,
         iid,
         vid,
         midd,
         e,
         ef,
         efd,
         d,
         doc,
         r,
         t,
         s,
         b
        """
        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))

        cr.execute(
            "CREATE OR REPLACE VIEW %s AS ( %s)" %
            (self._name.replace('.', '_'), query)
        )

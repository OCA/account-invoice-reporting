* Activate developer mode.
* Go to *Settings > Technical > Parameters > System Parameters*.
* Locate the setting with key
  "account_invoice_report_payment_info.info_pattern"
  or create a new one if not exists.
* Set a format pattern using the key available in _get_reconciled_info_JSON_values method.
  This module adds move_ref key to all those odoo core keys:

  * 'name': payment.name
  * 'journal_name': payment.journal_id.name,
  * 'amount': amount_to_show,
  * 'currency': currency_id.symbol,
  * 'digits': [69, currency_id.decimal_places],
  * 'position': currency_id.position,
  * 'date': payment.date,
  * 'payment_id': payment.id,
  * 'account_payment_id': payment.payment_id.id,
  * 'invoice_id': payment.invoice_id.id,
  * 'invoice_view_id': invoice_view_id,
  * 'move_id': payment.move_id.id,
  * 'ref': payment_ref,

https://github.com/odoo/odoo/blob/1e35b8987c619f200e84da2ba97040b38347edde/addons/account/models/account_move.py#L1351

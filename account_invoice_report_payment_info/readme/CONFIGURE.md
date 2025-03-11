- Activate developer mode.
- Go to *Settings \> Technical \> Parameters \> System Parameters*.
- Locate the setting with key
  "account_invoice_report_payment_info.info_pattern" or create a new one
  if not exists.
- Set a format pattern using the key available in
  \_compute_payments_widget_reconciled_info method. This module adds move_ref
  key to all those odoo core keys:
  - 'name'
  - 'journal_name'
  - 'company_name'
  - 'amount'
  - 'currency_id'
  - 'date'
  - 'partial_id'
  - 'account_payment_id'
  - 'payment_method_name'
  - 'move_id'
  - 'ref'
  - 'is_exchange'
  - 'amount_company_currency'
  - 'amount_foreign_currency'

<https://github.com/odoo/odoo/blob/536df945a53edd390e8382a6e179a36668553e63/addons/account/models/account_move.py#L1371>

The displayed per-line subtotal and the invoice untaxed total can diverge when
the **Round Globally** tax-rounding method is combined with a zero-decimal
currency (such as JPY). Odoo rounds each line's displayed subtotal to the
currency precision, but derives the untaxed total from the unrounded amounts and
rounds it only once, so the per-line subtotals printed on the invoice no longer
add up to the untaxed total.

For example, two lines of `100.5` each are shown as `101` (`100.5` rounded), so
a reader adds up `202`, while the untaxed total is `round(201.0) = 201`.

This behavior was introduced in Odoo 18. See
[odoo/odoo#265433](https://github.com/odoo/odoo/issues/265433) for details. This
module does not change any accounting figure; it only discloses the hidden
decimals on the report so the printed amounts reconcile.

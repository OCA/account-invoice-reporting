When an invoice uses **Round Globally** tax rounding with a zero-decimal
currency (such as JPY), the per-line subtotal shown on the invoice report is
rounded to the currency precision. The sum of these rounded line subtotals can
then differ from the invoice untaxed total, which is computed on the unrounded
amounts.

This module discloses the hidden decimals: when a line's currency-rounded
subtotal differs from its unrounded value, the invoice report shows the
unrounded subtotal (with product-price decimal precision) instead of the
rounded one. Lines without a rounding difference keep the standard
currency-formatted presentation.

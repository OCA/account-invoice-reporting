This module computes both at full precision (`price_subtotal_unrounded` on
`account.move.line` and `amount_untaxed_unrounded` on `account.move`, the latter
equal to the sum of the former) and discloses the unrounded per-line subtotal on
the invoice report. Rounding is presentation-only: the underlying fields stay
exact (computed at full precision, not currency-rounded) and can be reused by
other reports, while the report shows the subtotal at a configurable per-company
precision.

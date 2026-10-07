This module computes the line subtotal at full precision
(`price_subtotal_unrounded` on `account.move.line`) and discloses it on the
invoice report. Rounding is presentation-only: the underlying field stays exact
(computed at full precision, not currency-rounded) and can be reused by other
reports, while the report shows the subtotal at a configurable per-company
precision.

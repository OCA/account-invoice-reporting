Price-included taxes are out of scope.

The disclosure works for tax-excluded lines because Odoo derives the untaxed
total as `round(sum of the unrounded line bases)`. Printing those unrounded
bases therefore makes the per-line subtotals reconcile with the untaxed total.

For a price-included tax Odoo derives the untaxed total differently: as
`amount_total - amount_tax`, each rounded once under Round Globally. Take two
lines of `100.30` with a 10% included tax (JPY): each line base is
`100.30 / 1.1 = 91.18` (sum `182.36`), but the invoice shows an untaxed total
of `183` (`round(200.60) - round(18.24) = 201 - 18`). The summed bases do not
even round to that figure, so disclosing the unrounded per-line base would not
reconcile with the untaxed total — the premise the module relies on does not
hold. The per-line base is also a back-computed value, not the figure a
Japanese tax-included (内税) invoice shows.

Lines carrying a price-included tax therefore keep the standard rounded
subtotal; only tax-excluded lines get the unrounded value. The model field
`price_subtotal_unrounded` is still computed at full precision for every line,
so it stays correct if reused elsewhere — only the report omits it for
price-included lines.

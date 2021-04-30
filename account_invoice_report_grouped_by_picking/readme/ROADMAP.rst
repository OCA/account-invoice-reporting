* As a result of the grouping by pickings, we don't support notes and descriptions.
* Anyways, an invoice with no pickings should be printed as usual. The problem is
  that in the current state of the report, a heavy refactoring is needed to be able to
  fallback to the regular behavior in such case.

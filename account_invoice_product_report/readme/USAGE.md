Go to *Accounting → Reporting → Invoice Product Report*.

A wizard opens with the following filters:

- **Date From** / **Date To** – Billing period (required).
- **Customers** – Limit to selected customers. Leave empty for all.
- **Companies** – Limit to selected companies. Leave empty for all allowed
  companies.

Then pick an output:

- **View** – Show the report on screen (HTML).
- **Export PDF** – Download a PDF.
- **Export Excel** – Download an `.xlsx` file.

**Report content**

The header recalls the selected period, customers and companies (*All* when a
filter is left empty). The table has one row per company and customer, and one
column per product:

- *Company*, *Customer Code*, *Customer Name*, then one column per product.

Each cell is the **net amount** for that company / customer / product = posted
customer invoices minus credit notes within the period; an empty cell shows `-`.
Figures are never aggregated across companies.

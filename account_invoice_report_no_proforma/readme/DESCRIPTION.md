In Odoo 18, the *Download > PDF* menu and the portal of a posted customer invoice that has not been sent yet return a document titled PROFORMA, because the legal PDF is only generated and stored through the *Send* wizard.

This module removes the PROFORMA title and filename suffix from that document, so it is printed as a regular invoice. The document is still rendered on the fly, so it always reflects the current state of the invoice (e.g. registered payments), and no attachment is stored.

The proforma stored by the *Send* wizard as a fallback when the electronic document generation fails is kept as is.

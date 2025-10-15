This module assumes you have configured and are using ``sale_stock_picking_note`` as
described in its README (i.e., the **Picking Customer Comments** field is available on
the Contact's *Sales & Purchases* tab and on the Sales Order *Other Information* tab).

**Case 1: Single Sales Order -> Single Invoice**:

#. On the Sales Order, open the *Other Information* tab and set **Picking Customer
   Comments**.
#. When you create and print the invoice from this SO, the invoice report will display
   that **Picking Customer Comments** value from the Sales Order.

**Case 2: Multiple Sales Orders -> One (Grouped) Invoice**:

*When the invoice aggregates two or more sales orders, the report prints one 
value taken from the invoice's Delivery Address (shipping partner).*

#. Create two Sales Orders for the same customer using the same **Delivery Address**.
   Each sales order will have **Picking Customer Comments** set from its **Delivery 
   Address**. You may edit the SO value or leave it as is.
#. Deliver both Sales Orders by validating their related delivery pickings.
#. From the sales order list view, select both Sales Orders and invoice them, grouping
   into a single invoice.
#. Print the grouped invoice; the invoice report will display the **Delivery Address**
   value.

**Notes:**

- Make sure *Settings > Invoicing > Customer Invoices > Customer Addresses* is enabled.
- Changes made directly on pickings are not considered.
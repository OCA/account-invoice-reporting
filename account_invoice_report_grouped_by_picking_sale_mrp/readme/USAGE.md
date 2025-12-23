1.  Go to *Manufacturing -\> Products -\> Bills of Materials* and
    create a new BoM selecting the product, 'Kit' in 'BoM Type' field
    and filling the components list.
2.  Go to *Sales -\> Orders -\> Quotations* and create a new quotation
    with the 'Kit' previously created and qty 1.
3.  Confirm the sale order and you will see one delivery (accessible via
    smart-button) with the components of the kit.
4.  Validate the delivery.
5.  Go back to the sale order and create an invoice by clicking on
    Create Invoice button in the status bar.
6.  Print the invoice and the generated report will have 1 group with
    the name of the sales order and the name of the delivery. Inside
    there will be a line with the name of the product and quantity 1,
    despite the delivery operation has the components of the kit.

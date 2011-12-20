<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    %for inv in objects:
    <% setLang(inv.partner_id.lang) %>
    <div class="address">
        <table class="recipient">
            <tr><td class="name">${inv.partner_id.title or ''}  ${inv.partner_id.name }</td></tr>
            <tr><td>${inv.address_invoice_id.street or ''}</td></tr>
            <tr><td>${inv.address_invoice_id.street2 or ''}</td></tr>
            <tr><td>${inv.address_invoice_id.zip or ''} ${inv.address_invoice_id.city or ''}</td></tr>
            %if inv.address_invoice_id.country_id:
            <tr><td>${inv.address_invoice_id.country_id.name or ''} </td></tr>
            %endif
            %if inv.address_invoice_id.phone:
            <tr><td>${_("Tel")}: ${inv.address_invoice_id.phone}</td></tr>
            %endif
            %if inv.address_invoice_id.fax:
            <tr><td>${_("Fax")}: ${inv.address_invoice_id.fax}</td></tr>
            %endif
            %if inv.address_invoice_id.email:
            <tr><td>${_("E-mail")}: ${inv.address_invoice_id.email}</td></tr>
            %endif
            %if inv.partner_id.vat:
            <tr><td>${_("VAT")}: ${inv.partner_id.vat}</td></tr>
            %endif
        </table>
    </div>

    <h1 style="clear: both; padding-top: 20px;">
        %if inv.type == 'out_invoice' and inv.state == 'proforma2':
            ${_("PRO-FORMA")}
        %elif inv.type == 'out_invoice' and inv.state == 'draft':
            ${_("Draft Invoice")}
        %elif inv.type == 'out_invoice' and inv.state == 'cancel':
            ${_("Cancelled Invoice")} ${inv.number or ''}
        %elif inv.type == 'out_invoice':
            ${_("Invoice")} ${inv.number or ''}
        %elif inv.type == 'in_invoice':
            ${_("Supplier Invoice")} ${inv.number or ''}
        %elif inv.type == 'out_refund':
            ${_("Refund")} ${inv.number or ''}
        %elif inv.type == 'in_refund':
            ${_("Supplier Refund")} ${inv.number or ''}
        %endif
    </h1>

    <table class="basic_table" width="100%">
        <tr>
            <td>${_("Document")}</td>
            <td>${_("Invoice Date")}</td>
            <td>${_("Partner Ref.")}</td>
        </tr>
        <tr>
            <td>${inv.name or ''}</td>
            <td>${formatLang(inv.date_invoice, date=True)}</td>
            <td>${inv.address_invoice_id and inv.address_invoice_id.partner_id and inv.address_invoice_id.partner_id.ref or ''}</td>
        </tr>
    </table>

    <table class="list_table" width="100%" style="margin-top: 20px;">
        <thead>
            <tr>
                <th>${_("Description")}</th>
                <th>${_("Taxes")}</th>
                <th class="amount">${_("Qty")}</th>
                <th class="amount">${_("Unit Price")}</th>
                <th class="amount">${_("Disc.(%)")}</th>
                <th class="amount">${_("Price")}</th>
            </tr>
        </thead>
        <tbody>
        %for line in inv.invoice_line :
            <tr class="line">
                <td>${line.name}</td>
                <td>${ ', '.join([ tax.name or '' for tax in line.invoice_line_tax_id ])}</td>
                <td class="amount">${line.quantity} ${line.uos_id and line.uos_id.name or ''}</td>
                <td class="amount">${formatLang(line.price_unit)}</td>
                <td class="amount">${formatLang(line.discount or 0.00, digits=get_digits(dp='Account'))}</td>
                <td class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            %if line.note :
                <tr>
                    <td colspan="6" class="note">${line.note | carriage_returns}</td>
                </tr>
            %endif
        %endfor
        </tbody>
        <tfoot>
            <tr>
                <td style="border-style:none" colspan="4"/>
                <td style="border-top:2px solid">
                    <b>${_("Net Total:")}</b>
                </td>
                <td class="amount" style="border-top:2px solid;">${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            <tr>
                <td style="border-style:none" colspan="4"/>
                <td style="border-style:none">
                    <b>${_("Taxes:")}</b>
                </td>
                <td class="amount">${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            <tr>
                <td style="border-style:none" colspan="4"/>
                <td style="border-top:2px solid">
                    <b>${_("Total:")}</b>
                </td>
                <td class="amount" style="border-top:2px solid;">${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
        </tfoot>
    </table>

    <table class="list_table" width="40%" style="margin-top: 20px;">
        <tr>
            <th>${_("Tax")}</th>
            <th>${_("Base")}</th>
            <th class="amount">${_("Amount")}</th>
        </tr>
        %if inv.tax_line :
        %for t in inv.tax_line :
            <tr>
                <td>${ t.name } </td>
                <td>${ t.base }</td>
                <td class="amount">${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
            </tr>
        %endfor
        %endif
        <tr>
            <td style="border-style:none"/>
            <td style="border-top:2px solid"><b>${_("Total")}</b></td>
            <td class="amount" style="border-top:2px solid">${ formatLang(inv.amount_tax) }</td>
        </tr>
    </table>
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>

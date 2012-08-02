<html>
<head>
    <style type="text/css">
        ${css}
                    .list_invoice_table {
                        border:thin solid #E3E4EA;
                        text-align:center;
                        border-collapse: collapse;
                    }
                    .list_invoice_table td {
                        border-top : thin solid #EEEEEE;
                        text-align:left;
                        font-size:12;
                        padding-right:3px
                        padding-left:3px
                        padding-top:3px
                        padding-bottom:3px
                    }

                    .list_bank_table {
                        text-align:center;
                        border-collapse: collapse;
                    }
                    .list_bank_table td {
                        text-align:left;
                        font-size:12;
                        padding-right:3px
                        padding-left:3px
                        padding-top:3px
                        padding-bottom:3px
                    }

                    .list_bank_table th {
                        background-color: #EEEEEE;
                        text-align:left;
                        font-size:12;
                        font-weight:bold;
                        padding-right:3px
                        padding-left:3px
                    }

                    .list_invoice_table th {
                        background-color: #EEEEEE;
                        border: thin solid #000000;
                        text-align:center;
                        font-size:12;
                        font-weight:bold;
                        padding-right:3px
                        padding-left:3px
                    }

                    .list_invoice_table thead {
                        display:table-header-group;
                    }


                    .list_tax_table {
                    }
                    .list_tax_table td {
                        text-align:left;
                        font-size:12;
                    }

                    .list_tax_table th {
                    }


                    .list_tax_table thead {
                        display:table-header-group;
                    }

                    .list_total_table {
                        border:thin solid #E3E4EA;
                        text-align:center;
                        border-collapse: collapse;
                    }
                    .list_total_table td {
                        border-top : thin solid #EEEEEE;
                        text-align:left;
                        font-size:12;
                        padding-right:3px
                        padding-left:3px
                        padding-top:3px
                        padding-bottom:3px
                    }

                    .list_total_table th {
                        background-color: #EEEEEE;
                        border: thin solid #000000;
                        text-align:center;
                        font-size:12;
                        font-weight:bold;
                        padding-right:3px
                        padding-left:3px
                    }


                    .list_total_table thead {
                        display:table-header-group;
                    }

                    .no_bloc {
                        border-top: thin solid  #ffffff ;
                    }

                    .right_table {
                        right: 4cm;
                        width:"100%";
                    }

                    .std_text {
                        font-size:12;
                    }

                    td.amount {
                        text-align: right;
                    }

                    tfoot.totals tr:first-child td{
                        padding-top: 15px;
                    }

                    th.date {
                        width: 90px;
                    }

                    td.date {
                        white-space: nowrap;
                        width: 90px;
                    }

                    td.vat {
                        white-space: nowrap;
                    }

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
            <tr><td class="name">${inv.partner_id.title.name or ''}  ${inv.partner_id.name }</td></tr>
            <tr><td>${inv.address_invoice_id.title.name or ''}  ${inv.address_invoice_id.name }</td></tr>
            <tr><td>${inv.address_invoice_id.street or ''}</td></tr>
            <tr><td>${inv.address_invoice_id.street2 or ''}</td></tr>
            <tr><td>${inv.address_invoice_id.zip or ''} ${inv.address_invoice_id.city or ''}</td></tr>
            %if inv.address_invoice_id.country_id:
            <tr><td>${inv.address_invoice_id.country_id.name or ''} </td></tr>
            %endif
        </table>
    </div>
    <div>

    %if inv.note1_webkit :
        <p class="std_text"> ${inv.note1_webkit | carriage_returns} </p>
    %endif
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
    <h3  style="clear: both; padding-top: 20px;">
        ${_("Subject : ")} ${inv.name or ''}
    </h3>

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${_("Invoice Date")}</td>
            <th class="date">${_("Due Date")}</td>
            <th>${_("Your Ref.")}</td>
            <th>${_("Our Ref.")}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td class="date">${formatLang(inv.date_due, date=True)}</td>
            <td>${inv.reference or ''}</td>
            <td width="20%">${inv.origin or ''}</td>
        </tr>
    </table>

    <table class="list_invoice_table" width="100%" style="margin-top: 20px;">
        <thead>
            <tr>
                <th>${_("Description")}</th>
                <th>${_("Taxes")}</th>
                <th>${_("Qty")}</th>
                <th>${_("Unit Price")}</th>
                <th>${_("Disc.(%)")}</th>
                <th>${_("Net Sub Total")}</th>
            </tr>
        </thead>
        <tbody>
        %for line in inv.invoice_line :
            <tr >
                <td>${line.name}</td>
                <td style="text-align:center;">${ ', '.join([ tax.name or '' for tax in line.invoice_line_tax_id ])}</td>
                <td class="amount">${line.quantity} ${line.uos_id and line.uos_id.name or ''}</td>
                <td class="amount">${formatLang(line.price_unit)}</td>
                <td class="amount">${formatLang(line.discount or 0.00, digits=get_digits(dp='Account'))}</td>
                <td class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            %if line.note :
                <tr>
                    <td colspan="6" class="note" style="font-style:italic; font-size: 10; border-top: thin solid  #ffffff ; padding:20;">${line.note | carriage_returns}</td>
                </tr>
            %endif
        %endfor
        </tbody>
        <tfoot class="totals">
            <tr>
                <td colspan="5" style="text-align:right;border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
                    <b>${_("Net :")}</b>
                </td>
                <td class="amount" style="border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
                    ${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                </td>
            </tr>
            <tr class="no_bloc">
                <td colspan="5" style="text-align:right; border-top: thin solid  #ffffff ; border-right: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
                    <b>${_("Taxes:")}</b>
                </td>
                <td class="amount" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;">
                        ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                </td>
            </tr>
            <tr>
                <td colspan="5" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;border-bottom: thin solid  #ffffff ;text-align:right;">
                    <b>${_("Total:")}</b>
                </td>
                <td class="amount" style="border-right: thin solid  #ffffff ;border-top: thin solid  #ffffff ;border-left: thin solid  #ffffff ;border-bottom: thin solid  #ffffff ;">
                        <b>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</b>
                </td>
            </tr>
        </tfoot>
    </table>
        <br/>
    <table class="list_total_table" width="40%" >
        <tr>
            <th style="text-align:left;">${_("Rate")}</th>
            <th>${_("Base")}</th>
            <th>${_("Tax")}</th>
        </tr>
        %if inv.tax_line :
        %for t in inv.tax_line :
            <tr>
                <td style="text-align:left;">${ t.name } </td>
                <td class="amount">${ formatLang(t.base, digits=get_digits(dp='Account')) }</td>
                <td class="amount">${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
            </tr>
        %endfor
        %endif
    </table>
        <br/>
        <br/>
        <h4>
                ${_("Thank you for your prompt payment")}
        </h4>
        <br/>
    <table class="list_bank_table" width="100%" >
        <tr>
            <th style="width:20%;">${_("Bank Account")}</th>
            <td style="width:30%;text-align:left;">${ inv.partner_bank_id and inv.partner_bank_id.acc_number or '-' } </td>
            %if inv.address_invoice_id and inv.address_invoice_id.partner_id and inv.address_invoice_id.partner_id.vat :
            <th style="width:20%;">${_("Customer VAT No")}</th>
            <td style="width:30%;">${inv.address_invoice_id.partner_id.vat or '-'}</td>
            %endif
        </tr>
        <tr>
            <th style="width:20%;">${_("IBAN")}</th>
            <td style="width:30%;text-align:left;">${ inv.partner_bank_id and inv.partner_bank_id.iban or '-' }</td>
            <th style="width:20%;">${_("Our VAT No")}</td>
            <td style="width:30%;" class="vat">${company_vat() or '-'}</td>
        </tr>
        <tr>
            <th width="20%">${_("BIC")}</th>
            <td style="width:30%;">${ inv.partner_bank_id and inv.partner_bank_id.bank and inv.partner_bank_id.bank.bic or '-' }</td>
        </tr>
    </table>
    <br/>
    %if inv.comment :
        <p class="std_text">${inv.comment | carriage_returns}</p>
    %endif
    %if inv.note2_webkit :
        <p class="std_text">${inv.note2_webkit | carriage_returns}</p>
    %endif
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>

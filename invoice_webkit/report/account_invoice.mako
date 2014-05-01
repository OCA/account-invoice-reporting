## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}

.list_main_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines,
.list_main_footers {
    padding: 0;
}
.list_main_footers {
    padding-top: 15px;
}
.list_main_lines td,
.list_main_footers td,
.list_main_footers th {
    border-style: none;
    text-align:left;
    font-size:12;
    padding:0;
}
.list_main_footers th {
    text-align:right;
}

td .total_empty_cell {
    width: 77%;
}
td .total_sum_cell {
    width: 13%;
}

.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}

.main_col1 {
    width: 40%;
}
td.main_col1 {
    text-align:left;
}
.main_col2,
.main_col3,
.main_col4,
.main_col6 {
    width: 10%;
}
.main_col5 {
    width: 7%;
}
td.main_col5 {
    text-align: center;
    font-style:italic;
    font-size: 10;
}
.main_col7 {
    width: 13%;
}

.list_bank_table {
    text-align:center;
    border-collapse: collapse;
    page-break-inside: avoid;
    display:table;
}

.act_as_row {
   display:table-row;
}
.list_bank_table .act_as_thead {
    background-color: #EEEEEE;
    text-align:left;
    font-size:12;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
    white-space:nowrap;
    background-clip:border-box;
    display:table-cell;
}
.list_bank_table .act_as_cell {
    text-align:left;
    font-size:12;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
    white-space:nowrap;
    display:table-cell;
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
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
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

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-size:12;
}

th.date {
    width: 90px;
}

td.amount, th.amount {
    text-align: right;
    white-space: nowrap;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

td.vat {
    white-space: nowrap;
}
.address .recipient {
    font-size: 12px;
    margin-left: 350px;
    margin-right: 120px;
    float: right;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner, commercial_partner=None)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        <% company_partner = False %>
        %if commercial_partner:
            %if commercial_partner.id != partner.id:
                <% company_partner = commercial_partner %>
            %endif
        %elif partner.parent_id:
            <% company_partner = partner.parent_id %>
        %endif

        %if company_partner:
            <tr><td class="name">${company_partner.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for inv in objects:
    <% setLang(inv.partner_id.lang) %>
    <div class="address">
      <table class="recipient">
        %if hasattr(inv, 'commercial_partner_id'):
        ${address(partner=inv.partner_id, commercial_partner=inv.commercial_partner_id)}
        %else:
        ${address(partner=inv.partner_id)}
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
    <h3  style="clear: both; padding-top: 20px;">
        ${_("Subject : ")} ${inv.name or ''}
    </h3>

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${_("Invoice Date")}</td>
            <th class="date">${_("Due Date")}</td>
            <th style="text-align:center;width:120px;">${_("Responsible")}</td>
            <th style="text-align:center">${_("Payment Term")}</td>
            <th style="text-align:center">${_("Our reference")}</td>
            %if inv.reference and inv.reference != inv.name:
                <th style="text-align:center">${_("Your reference")}</td>
            %endif
        </tr>
        <tr>
            <td class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td class="date">${formatLang(inv.date_due, date=True)}</td>
            <td style="text-align:center;width:120px;">${inv.user_id and inv.user_id.name or ''}</td>
            <td style="text-align:center">${inv.payment_term and inv.payment_term.note or ''}</td>
            <td style="text-align:center">${inv.origin or ''}</td>
            %if inv.reference and inv.reference != inv.name:
                <td style="text-align:center">${inv.reference}</td>
            %endif
        </tr>
    </table>

    <div>
    %if inv.note1:
        <p class="std_text"> ${inv.note1 | n} </p>
    %endif
    </div>

    <table class="list_main_table" width="100%">
      <thead>
        <tr>
          <th class="list_main_headers" style="width: 100%">
            <table style="width:100%">
              <tr>
                <th class="main_col1">${_("Description")}</th>
                <th class="amount main_col2">${_("Qty")}</th>
                <th class="amount main_col3">${_("UoM")}</th>
                <th class="amount main_col4">${_("Unit Price")}</th>
                <th class="main_col5">${_("Taxes")}</th>
                <th class="amount main_col6">${_("Disc.(%)")}</th>
                <th class="amount main_col7">${_("Net Sub Total")}</th>
              </tr>
            </table>
          </th>
        </tr>
      </thead>
      <tbody>
        %for line in inv.invoice_line:
          <tr>
            <td class="list_main_lines" style="width: 100%">
              <div class="nobreak">
                <table style="width:100%">
                  <tr>
                    <td class="main_col1">${line.name.replace('\n','<br/>') or '' | n}</td>
                    <td class="amount main_col2">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                    <td class="amount main_col3">${line.uos_id and line.uos_id.name or ''}</td>
                    <td class="amount main_col4">${formatLang(line.price_unit)}</td>
                    <td class="main_col5">${ ', '.join([tax.description or tax.name for tax in line.invoice_line_tax_id])}</td>
                    <td class="amount main_col6">${line.discount and formatLang(line.discount, digits=get_digits(dp='Account')) or ''} ${line.discount and '%' or ''}</td>
                    <td class="amount main_col7">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
                  </tr>
                  %if line.formatted_note:
                    <caption class="formatted_note">
                      ${line.formatted_note| n}
                    </caption>
                  %endif
                </table>
              </div>
            </td>
          </tr>
        %endfor
      </tbody>
      <tfoot class="totals">
        <tr>
          <td class="list_main_footers" style="width: 100%">
            <div class="nobreak">
              <table style="width:100%">
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Net :")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Taxes:")}
                  </th>
                  <td class="amount total_sum_cell">
                    ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                  </td>
                </tr>
                <tr>
                  <td class="total_empty_cell"/>
                  <th>
                    ${_("Total:")}
                  </th>
                  <td class="amount total_sum_cell">
                    <b>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</b>
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>
      </tfoot>
    </table>
        <br/>
    <table class="list_total_table" width="60%" >
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
    <%
      inv_bank = inv.partner_bank_id
    %>
    <div class="list_bank_table act_as_table" style="width:100%;" >
      <!-- vat value are taken back from commercial id -->
        <div class="act_as_row">
            <div class="act_as_thead" style="width:20%;">${_("Bank")}</div>
            <div class="act_as_cell" style="width:40%;text-align:left;">${inv_bank and inv_bank.bank_name or '-' } </div>
            %if inv.partner_id and inv.partner_id.vat :
            <div class="act_as_thead" style="width:20%;">${_("Customer VAT No")}</div>
            <div class="act_as_cell" style="width:20%;">${inv.partner_id.vat or '-'}</div>
            %else:
            <!-- conserve table's cells widths -->
            <div class="act_as_cell" style="width:20%;"></div>
            <div class="act_as_cell" style="width:20%;"></div>
            %endif
        </div>
        <div class="act_as_row">
            <div class="act_as_thead" style="width:20%;">${_("Bank account")}</div>
            <div class="act_as_cell" style="width:40%;text-align:left;">${ inv_bank and inv_bank.acc_number or '-' }</div>
            <div class="act_as_thead" style="width:20%;">${_("Our VAT No")}</div>
            <div class="act_as_cell" style="width:20%;" class="vat">${inv.company_id.partner_id.vat or '-'}</div>
        </div>
        <div class="act_as_row">
            <div class="act_as_thead" style="width:20%;">${_("BIC")}</div>
            <div class="act_as_cell"  style="width:40%;">${inv_bank and inv_bank.bank_bic or '-' }</div>
        </div>
    </div>
    <br/>
    %if inv.comment :
        <p class="std_text">${inv.comment | carriage_returns}</p>
    %endif
    %if inv.note2 :
        <p class="std_text">${inv.note2 | n}</p>
    %endif
    %if inv.fiscal_position and inv.fiscal_position.note:
        <br/>
        <p class="std_text">
        ${inv.fiscal_position.note | n}
        </p>
    %endif
    <p style="page-break-after:always"/>
    %endfor
</body>
</html>

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
			border-top : thin solid #E3E4EA;
			text-align:left;
			font-size:12;
			padding-right:3px
			padding-left:3px
			padding-top:3px
			padding-bottom:3px
			}
			
			.list_invoice_table th {
			background-color: #E3E4EA;
			border: thin solid #000000;
			text-align:center;
			font-size:12;
			font-weight:bold;
			padding-right:3px
			padding-left:3px
			}
			
			.list_table thead {
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


			.list_table thead {
			    display:table-header-group;
			}


			.list_total_table {
				border-collapse: collapse;
			}
			.list_total_table td {
			text-align:right;
			font-size:12;
			}

			.no_bloc {
				border-top: thin solid  #ffffff ;
			}

			
			.list_total_table th {
				background-color: #E3E4EA;
				border-collapse: collapse;
			}


			.right_table {
			right: 4cm;
			width:"100%";
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
    
    <h3 style="clear: both; padding-top: 20px;">
    	${_("Subject : ")} ${inv.name or ''}
    </h3>

    <table class="basic_table" width="100%">
        <tr>
            <td>${_("Invoice Date")}</td>
            <td>${_("Due Date")}</td>
            <td>${_("Your Ref.")}</td>
        </tr>
        <tr>
            <td>${inv.date_invoice or ''}</td>
            <td>${formatLang(inv.date_due, date=True)}</td>
            <td>${inv.address_invoice_id and inv.address_invoice_id.partner_id and inv.address_invoice_id.partner_id.ref or ''}</td>
        </tr>
    </table>

    <table class="list_invoice_table" width="100%" style="margin-top: 20px;">
        <thead>
            <tr>
                <th>${_("Description")}</th>
                <th>${_("Taxes")}</th>
                <th class="amount">${_("Qty")}</th>
                <th class="amount">${_("Unit Price")}</th>
                <th class="amount">${_("Disc.(%)")}</th>
                <th class="amount">${_("Net Sub Total")}</th>
            </tr>
        </thead>
        <tbody>
        %for line in inv.invoice_line :
            <tr >
                <td>${line.name}</td>
                <td>${ ', '.join([ tax.tax_code_id.name or '' for tax in line.invoice_line_tax_id ])}</td>
                <td style="text-align:right;" class="amount">${line.quantity} ${line.uos_id and line.uos_id.name or ''}</td>
                <td style="text-align:right;" class="amount">${formatLang(line.price_unit)}</td>
                <td style="text-align:right;" class="amount">${formatLang(line.discount or 0.00, digits=get_digits(dp='Account'))}</td>
                <td style="text-align:right;" class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            %if line.note :
                <tr>
                    <td colspan="6" class="note" style="font-style:italic; font-size: 10; border-top: thin solid  #ffffff ; padding:20;">${line.note | carriage_returns}</td>
                </tr>
            %endif
        %endfor
        </tbody>
    <tfoot >
            <tr>
            	<td style="border-left: thin solid  #ffffff ;"></td>
            	<td></td>
            	<td></td>
            	<td ></td>
                <td>
                    <b>${_("Net Total:")}</b>
                </td>
                <td class="amount" style="text-align:right;border-right: thin solid  #ffffff ;">${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            <tr class="no_bloc">
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;border-left: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ;">
                    <b>${_("Taxes:")}</b>
                </td>
                <td class="amount" style="border-top: thin solid  #ffffff ;border-right: thin solid  #ffffff ;text-align:right;">
	                ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
	       		</td>
            </tr>
            <tr>
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;border-left: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;"></td>
            	<td style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;">
                    <b>${_("Total:")}</b>
                </td>
                <td class="amount" style="border-top: thin solid  #ffffff ; border-bottom: thin solid  #ffffff ;border-right: thin solid  #ffffff ;text-align:right;">
					${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
				</td>
            </tr>
	</tfoot>
    </table>
	<br/>
    <table class="list_total_table" width="40%" >
        <tr>
            <th>${_("Tax Name")}</th>
            <th>${_("Net")}</th>
            <th>${_("Tax")}</th>
        </tr>
        %if inv.tax_line :
        %for t in inv.tax_line :
            <tr>
                <td style="text-align:left;">${ t.name } </td>
                <td>${ t.base }</td>
                <td>${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
            </tr>
        %endfor
        %endif
    </table>
    <p style="page-break-after:always"></p>
    %endfor
</body>
</html>

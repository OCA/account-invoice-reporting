import {ReportAction} from "@web/webclient/actions/reports/report_action";
import {patch} from "@web/core/utils/patch";

// Add an "Export Excel" button to the report viewer control panel for this
// module's QWeb reports. The XLSX report shares the HTML report name plus a
// "_xlsx" suffix (account_invoice_product_report.report_invoice_product ->
// account_invoice_product_report.report_invoice_product_xlsx).
const MODULE_NAME = "account_invoice_product_report";

patch(ReportAction.prototype, {
    setup() {
        super.setup(...arguments);
        this.isXlsxReport = this.props.report_name.startsWith(`${MODULE_NAME}.`);
    },

    exportXlsx() {
        const xlsxName = `${this.props.report_name}_xlsx`;
        this.action.doAction({
            type: "ir.actions.report",
            report_type: "xlsx",
            report_name: xlsxName,
            report_file: xlsxName,
            data: this.props.data || {},
            context: this.props.context || {},
            display_name: this.title,
        });
    },
});

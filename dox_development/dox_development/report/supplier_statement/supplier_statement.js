// Copyright (c) 2023, Nesscale Solutions Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier Statement"] = {
	"filters": [
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Link",
			"options": "Supplier",
			"reqd": 1,
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
			on_change: function () {
				var party_type = "Supplier";
				var parties = frappe.query_report.get_filter_value('party');
				var party = parties;
				var fieldname = erpnext.utils.get_party_name(party_type) || "name";
				frappe.db.get_value(party_type, party, fieldname, function (value) {
					frappe.query_report.set_filter_value('party_name', value[fieldname]);
				});
				// if (!party_type || parties.length === 0 || parties.length > 1) {
				// 	frappe.query_report.set_filter_value('party_name', "");
				// 	return;
				// } else {

				// }
			}
		},
		{
			"fieldname": "party_name",
			"label": __("Party Name"),
			"fieldtype": "Read Only"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname": "presentation_currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"reqd": 1,
			"width": "60px",
			"options": "Currency",
		},
	]
};


// Copyright (c) 2023, Nesscale Solutions Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Statement"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"default": frappe.defaults.get_default("company"),
			"hidden":true
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1,
			get_data: function (txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
			on_change: function () {
				var party_type = "Customer";
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
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			"get_query": function() {
				// Get the report data
				var reportData = frappe.query_report.data;
		
				// Get the unique branches from the report data
				var reportBranches = reportData.map(row => row.branch);
				var uniqueBranches = [...new Set(reportBranches)];
		
				return {
					filters: {
						name: ["in", uniqueBranches]
					}
				};
			}
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
			"fieldname": "address",
			"label": __("Address"),
			"fieldtype": "Link",
			"options": "Address",
			"get_query": function () {
				var party = frappe.query_report.get_filter_value('party');
				if (party) {
					return {
						filters: {
							link_doctype: "Customer",
							link_name: party
						}
					};
				}
			}
		},
		{
			"fieldname": "remark",
			"label": __("Remark"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "terms",
			"label": __("Terms and Conditons"),
			"fieldtype": "Link",
			"options":"Terms and Conditions",
			"width": "60px"
		},
	],
    onload: function(report) {
        // Listen for changes in 'filter_1'
        report.page.fields_dict.party.$input.on('change', function() {
            // Clear values of 'filter_2' and 'filter_3' when 'filter_1' changes
            report.set_filter_value('branch', '');
            report.set_filter_value('address', '');
        });
    }
};


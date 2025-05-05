// Copyright (c) 2023, Nesscale Solutions Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Petty Cash Statement"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"hidden": true
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"reqd": 1,
			"options": "Branch"
		},
		{

			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"reqd": 1,
			"get_query": function () {
				return {
					"filters": {
						"account_type": "Cash"
					}
				};
			}
		},
		{
			"fieldname": 'from_date',
			"label": __('From Date'),
			"fieldtype": 'Date',
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 0
		},
		{
			"fieldname": 'to_date',
			"label": __('To Date'),
			"fieldtype": 'Date',
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 0
		},
	],
};

# Copyright (c) 2023, Nesscale Solutions Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext import get_default_company


def execute(filters=None):
    company = get_default_company()
    columns, data = [], []
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Select First from date and to date"))
        return columns, data
    if not filters.get("party"):
        frappe.throw(_("Select Supplier to view statement"))
        return columns, data
    filters_report = {
        "company": company,
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "party_type": "Supplier",
        "party": [filters.get("party")],
        "party_name": filters.get("party_name"),
        "group_by": "Group by Voucher (Consolidated)",
        "cost_center": [],
        "project": [],
        "include_dimensions": 1,
        "presentation_currency": filters.get("presentation_currency")
    }
    from frappe.desk.query_report import run

    res = run("General Ledger", filters=filters_report)
    data = res.get("result")
    columns = [
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {"label": "Voucher Type", "fieldname": "voucher_type", "width": 120},
        {
            "label": "Voucher No",
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 180,
        },
        {
            "label": "Debit",
            "fieldname": "debit",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Credit",
            "fieldname": "credit",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Balance",
            "fieldname": "balance",
            "fieldtype": "Float",
            "width": 130,
        },
    ]
    return columns, data

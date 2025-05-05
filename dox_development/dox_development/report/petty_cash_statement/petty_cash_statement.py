# Copyright (c) 2023, rakesh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns, data = [], []

    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.msgprint(_("Select First from date and to date"))
        return columns, data
    
    if not filters.get("account"):
        frappe.msgprint(_("Select Account to view statement"))
        return columns, data
    elif not filters.get("branch"):
        frappe.msgprint(_("Select Branch to view statement"))
        return columns, data
    
    
    filters_report = {
        "company": filters.get("company"),
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "account": [filters.get("account")],
        "party": [],
        "group_by": "Group by Voucher (Consolidated)",
        "branch": [filters.get("branch")],
        "project": [],
        "include_dimensions": 1,
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
        {
            "label": "Voucher No",
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 200,
        },
        {
            "label": "Debit (SAR)",
            "fieldname": "debit",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Credit (SAR)",
            "fieldname": "credit",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Balance (SAR)",
            "fieldname": "balance",
            "fieldtype": "Float",
            "width": 130,
        },
        {"label": _("Remarks"), "fieldname": "remarks", "width": 400},
    ]
    return columns, data

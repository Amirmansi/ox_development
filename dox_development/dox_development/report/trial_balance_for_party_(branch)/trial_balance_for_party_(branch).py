# Copyright (c) 2023, rakesh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    filters_report = {
        "company": filters.get("company"),
        "fiscal_year": filters.get("fiscal_year"),
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "branch": filters.get("branch"),
        "party_type": filters.get("party_type"),
    }
    from frappe.desk.query_report import run

    res = run("Trial Balance for Party", filters=filters_report)
    data = res.get("result")
    if filters.party_type == "Customer":
        for row in data:
            customer = row.get("party")
            if customer != "'Totals'":
                customer_doc = frappe.db.get_value(
                    "Customer", {"name": customer}, "customer_group", as_dict=1
                )
                if customer_doc:
                    row["customer_group"] = customer_doc.get("customer_group")
    columns = [
        {
            "fieldname": "party",
            "label": _(filters.party_type),
            "fieldtype": "Link",
            "options": filters.party_type,
            "width": 200,
        },
        {
            "fieldname": "opening_debit",
            "label": _("Opening (Dr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "fieldname": "opening_credit",
            "label": _("Opening (Cr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "fieldname": "debit",
            "label": _("Debit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "fieldname": "credit",
            "label": _("Credit"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "fieldname": "closing_debit",
            "label": _("Closing (Dr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "fieldname": "closing_credit",
            "label": _("Closing (Cr)"),
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
    ]
    if filters.party_type == "Customer":
        columns.insert(
            1,
            {
                "fieldname": "customer_group",
                "label": _("Customer Group"),
                "fieldtype": "Data",
                "width": 120,
            },
        )
    return columns, data

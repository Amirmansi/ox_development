import frappe
from frappe import _


def execute(filters=None):
    frappe.errprint("call")
    columns = []
    if not filters.get("from_date") or not filters.get("to_date"):
        frappe.throw(_("Select First from date and to date"))
        return columns, []

    if not filters.get("party"):
        frappe.throw(_("Select Customer to view statement"))
        return columns, []

    filters_report = {
        "company": filters.get("company"),
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "party_type": "Customer",
        "party": [filters.get("party")],
        "party_name": filters.get("party_name"),
        "group_by": "Group by Voucher (Consolidated)",
        "branch": [] if not filters.get("branch") else [filters.get("branch")],
        "cost_center": [],
        "project": [],
        "include_dimensions": 1,
    }

    from frappe.desk.query_report import run, add_custom_column_data

    res = run("General Ledger", filters=filters_report)
    data = res.get("result")

    columns = [
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {"label": "Voucher Type", "fieldname": "voucher_type", "width": 140},
        {
            "label": "Voucher No",
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 180,
        },
        {
            "label": "Branch",
            "options": "Branch",
            "fieldname": "branch",
            "width": 100,
            "hidden": 1,
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
    ]
    if filters.remark:
        columns.insert(
            3,
            {
                "label": _("Remarks"),
                "fieldname": "remarks",
                "insert_after_index": 1,
                "width": 400,
            },
        )

    custom_columns = [
        {
            "doctype": "Payment Entry",
            "fieldname": "mode_of_payment",
            "link_field": "voucher_no",
        },
        {
            "doctype": "Sales Invoice",
            "fieldname": "invoice_type",
            "link_field": "voucher_no",
        },
        {
            "doctype": "Payment Entry",
            "fieldname": "payment_type",
            "link_field": "voucher_no",
        },
    ]

    add_custom_column_data(custom_columns, data)

    for row in data:
        if row.get("voucher_type") == "Sales Invoice":
            if row.get("invoice_type") == "Credit Note":
                row["voucher_type"] = "Sales Return"
            else:
                row["voucher_type"] = row.get("invoice_type")
        if row.get("voucher_type") == "Payment Entry":
            row[
                "voucher_type"
            ] = f"{row.get('payment_type')} / {row.get('mode_of_payment')}"
        if row.get("voucher_type") == "Journal Entry":
            row["voucher_type"] = "Adjustment Entry"

        address = frappe.db.get_value(
            "Address",
            {"name": filters.get("address")},
            ["address_title", "address_line1", "city", "county", "country"],
            as_dict=1,
        )
        if address:
            row["address"] = address
        else:
            row["address"] = {}

        terms = frappe.db.get_value(
            "Terms and Conditions", filters.get("terms"), "terms", as_dict=1
        )
        if terms:
            row["terms"] = terms.get("terms")
        else:
            row["terms"] = {}
    return columns, data

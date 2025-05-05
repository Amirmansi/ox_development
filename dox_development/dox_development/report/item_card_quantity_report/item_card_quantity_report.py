# Copyright (c) 2023, rakesh and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    filters_report = {
        "company": filters.get("company"),
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "warehouse": filters.get("warehouse"),
        "item_code": filters.get("item_code"),
        "batch_no": filters.get("batch_no"),
        "variant_of": filters.get("variant_of"),
    }
    from frappe.desk.query_report import run

    res = run("Stock Ledger", filters=filters_report)
    data = res.get("result")
    (
        total_in_qty,
        total_qty_out,
        total_sales_invoice,
        total_purchase,
        total_stock_entry,
        reconcilation,
    ) = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    for row in data:
        if row.get("voucher_type") == "Sales Invoice":
            total_sales_invoice += 1
        elif (
            row.get("voucher_type") == "Purchase Receipt"
            or row.get("voucher_type") == "Purchase Invoice"
        ):
            total_purchase += 1
        elif row.get("voucher_type") == "Stock Entry":
            total_stock_entry += 1
        reconcilation = total_sales_invoice - total_purchase + total_stock_entry
        total_in_qty += row.get("in_qty", 0.0)
        total_qty_out += row.get("out_qty", 0.0)
        row["total_in"] = total_in_qty
        row["total_sales"] = total_sales_invoice
        row["total_purchase"] = total_purchase
        row["total_stock"] = total_stock_entry
        row["total_out"] = total_qty_out
        row["reconcilation"] = reconcilation

    columns = [
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 100,
        },
        {
            "label": _("In Qty"),
            "fieldname": "in_qty",
            "fieldtype": "Float",
            "width": 100,
            "convertible": "qty",
        },
        {
            "label": _("Out Qty"),
            "fieldname": "out_qty",
            "fieldtype": "Float",
            "width": 100,
            "convertible": "qty",
        },
        {
            "label": _("Balance Qty"),
            "fieldname": "qty_after_transaction",
            "fieldtype": "Float",
            "width": 100,
            "convertible": "qty",
        },
        {
            "label": _("Voucher #"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 200,
        },
    ]

    return columns, data

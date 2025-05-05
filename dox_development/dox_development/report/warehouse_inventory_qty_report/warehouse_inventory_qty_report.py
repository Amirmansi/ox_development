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
    }
    from frappe.desk.query_report import run

    res = run("Stock Balance", filters=filters_report, ignore_prepared_report=True)
    data = res.get("result")
    total_balance_qty, count_of_inventory_item = 0.0, 0.0
    for row in data:
        if isinstance(row, dict):
            total_balance_qty += row["bal_qty"]
            count_of_inventory_item += len(row["item_code"])
            row["total_balance_qty"] = total_balance_qty
            row["total_inventory_item"] = count_of_inventory_item
            batch_number = frappe.db.get_value(
                "Batch", {"item": row["item_code"]}, ["name"], as_dict=1
            )
            if batch_number:
                row["batch_no"] = batch_number.get("name")

    columns = [
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 150,
        },
        {"label": _("Item Name"), "fieldname": "item_name", "width": 150},
        {
            "label": _("Stock UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 90,
        },
        {
            "label": _("Batch"),
            "fieldname": "batch_no",
            "fieldtype": "Link",
            "options": "Batch",
            "width": 100,
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 100,
            "hidden": 1,
        },
        {
            "label": _("Balance Qty"),
            "fieldname": "bal_qty",
            "fieldtype": "Float",
            "width": 100,
            "convertible": "qty",
        },
    ]
    return columns, data

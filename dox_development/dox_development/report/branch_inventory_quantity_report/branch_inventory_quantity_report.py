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
        "branch": [] if not filters.get("branch") else [filters.get("branch")],
    }

    from frappe.desk.query_report import run

    res = run("Stock Ledger", filters=filters_report)
    data = res.get("result")
    columns = [
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 100,
        },
        {"label": _("Item Name"), "fieldname": "item_name", "width": 100},
        {
            "label": _("Stock UOM"),
            "fieldname": "stock_uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 100,
        },
        {
            "label": _("Batch"),
            "fieldname": "batch_no",
            "fieldtype": "Link",
            "options": "Batch",
            "width": 100,
        },
    ]

    selected_branch = filters_report["branch"]  # Get the selected branch
    for branch in selected_branch:
        warehouses = frappe.get_all(
            "Branch Default Warehouse",
            filters={"parent": branch},
            fields=["warehouse"],
        )
        for warehouse in warehouses:
            columns.append(
                {
                    "label": _("{0} Qty").format(warehouse.get("warehouse")),
                    "fieldname": warehouse.get("warehouse"),
                    "fieldtype": "Float",
                    "width": 200,
                }
            )
            for i in range(len(data)):
                row = data[i]
                warehouse_qty = frappe.db.get_value(
                    "Bin",
                    {
                        "warehouse": warehouse.get("warehouse"),
                        "item_code": row.get("item_code"),
                    },
                    "actual_qty",
                )
                if warehouse_qty:
                    data[i][warehouse.get("warehouse")] = warehouse_qty
                else:
                    data[i][warehouse.get("warehouse")] = 0

    return columns, data

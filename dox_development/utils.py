import frappe

# required fields for address
# Address Line 1
# City/Town
# State/Province
# Postal Code
def update_address(doc, method=None):
    try:
        address_data = dict()
        doc.tax_category = doc.tax_category_custom
        doc.tax_id = doc.trn_custom
        # frappe.log_error(
        #     title="dox check",
        #     message=[
        #         doc.building_no,
        #         doc.street,
        #         doc.city,
        #         doc.province,
        #         doc.country,
        #         doc.postal_code,
        #     ],
        # )
        if (
            doc.building_no
            == doc.street
            == doc.city
            == doc.province
            == doc.postal_code
            == None
        ):
            frappe.log_error(title="dox theme return", message="return")
            return
        address_data["address_line1"] = doc.building_no
        address_data["address_line2"] = doc.street
        address_data["additional_no"] = doc.additional_no
        address_data["city"] = doc.city
        address_data["state"] = doc.province
        address_data["county"] = doc.district
        address_data["country"] = doc.country
        address_data["pincode"] = doc.postal_code
        if doc.address_link == None or not len(doc.address_link) > 0:
            address_id = _create_address(address_data, doc.name)
            doc.address_link = address_id
            doc.save()
        else:
            address_data["name"] = doc.address_link
            address_id = _update_address(address_data, doc.name)
    except Exception as e:
        frappe.log_error(title="dox theme error", message=frappe.get_traceback())


def _create_address(data, customer_name):
    try:
        doc = frappe.get_doc(
            {
                "doctype": "Address",
                "address_line1": data.get("address_line1"),
                "address_line2": data.get("address_line2"),
                "city": data.get("city"),
                "state": data.get("state"),
                "county": data.get("county"),
                "country": data.get("country"),
                "pincode": data.get("pincode"),
                "additional_no": data.get("additional_no"),
                "customer_address": 1,
                "links": [{"link_doctype": "Customer", "link_name": customer_name}],
            }
        ).insert(ignore_permissions=True)
        return doc.name
    except Exception as e:
        frappe.log_error(title="Dox Theme Error", message=frappe.get_traceback())


def _update_address(data, customer_name):
    try:

        address = frappe.db.get_all(
            "Address",
            filters={
                "link_doctype": "Customer",
                "link_name": customer_name,
                "name": data.get("name"),
            },
        )
        if not len(address) > 0:
            return frappe.throw("invalid address")
        doc = frappe.get_doc("Address", data.get("name"))
        doc.address_line1 = data.get("address_line1")
        doc.address_line2 = data.get("address_line2")
        doc.city = data.get("city")
        doc.state = data.get("state")
        doc.country = data.get("country")
        doc.county = data.get("county")
        doc.additional_no = data.get("additional_no")
        doc.pincode = data.get("pincode")
        doc.customer_address = 1
        doc.save(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(title="dox theme error", message=frappe.get_traceback())


def gen_response(status, message, data=[]):
    frappe.response["status_code"] = status
    frappe.response["message"] = message
    frappe.response["data"] = data

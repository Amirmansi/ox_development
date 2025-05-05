frappe.pages['item_sales_page'].on_page_load = function (wrapper) {
	const sales_page = new SalesPage(wrapper);
	$(wrapper).bind("show", () => {
		sales_page.show();
	});
	window.item_sales_page = sales_page;
}

class SalesPage {
	constructor(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Item Sales Page',
			single_column: true
		});

		this.page.main.addClass("frappe-card");
		this.page.body.append('<div class="table-area"></div>');
		this.$content = $(this.page.body).find(".table-area");
		this.make_filters();
	}

	make_filters() {
		this.search = this.page.add_field({
			label: __("Search"),
			fieldname: "search",
			fieldtype: "Data",
			change: () => {
				this.refresh_data();
			},
		});
	}

	show() {
		this.refresh_data();
	}

	refresh_data() {
		let search = this.search.get_value();
		let args;
		if (search.length > 0) {
			args = { search };
		} else {
			args = {};
		}

		this.page.add_inner_message(__("Refreshing..."));
		frappe.call({
			method: "dox_development.dox_development.page.item_sales_page.item_sales_page.get_info",
			args,
			callback: (res) => {
				this.page.add_inner_message("");
				let template = "item_sales_page";
				this.$content.html(
					frappe.render_template(template, {
						data: res.message || [],
					})
				);
				this.render_table(res.message)
				let main = this
				$(".view_stock_button").click(function () {

					main.custom_dialog($(this).data("item"))
				});
			},
		});
	}

	render_table(data) {
		var thead = $(this.page.body).find("#thead");
		var tbody = $(this.page.body).find("#tbody");

		for (const key in data[0]) {
			thead.append("<th>" + key + "</th>");
		}
		thead.append("<th></th>");
		data.forEach(item => {
			var tr = "<tr>"
			for (const key in item) {
				tr += "<td>" + item[key] + "</td>";
			}
			tr += "<td><button data-item='" + item["Item Code"] + "' class='view_stock_button btn btn-primary btn-sm primary-action'>View Stock</button></td>";
			tr += "</tr>";
			tbody.append(tr);
		});
	}

	gen_html_table(data) {
		var thead = "";
		var tbody = "";
		for (const key in data[0]) {
			thead += ("<th>" + key + "</th>");
		}
		data.forEach(item => {
			var tr = "<tr>"
			for (const key in item) {
				tr += "<td>" + item[key] + "</td>";
			}
			tr += "</tr>";
			tbody += (tr);
		});
		return `<table class="table"><thead>` + thead + `</thead><tbody id="tbody">` + tbody + `</tbody></table>`
	}


	custom_dialog(item) {
		let html,args
		args = { item };
		frappe.call({
			method: "dox_development.dox_development.page.item_sales_page.item_sales_page.get_warehouse_info",
			args,
			callback: (res) => {
				html = this.gen_html_table(res.message)
				const fields = [{
						fieldtype: 'HTML',
						fieldname: 'stock_details'
				}]
		
				var dialog = new frappe.ui.Dialog({
					title: __('Inventory Stock'),
					fields: fields,
				});
				dialog.fields_dict.stock_details.$wrapper.append(html);
				dialog.show();
			},
		});

	}


}

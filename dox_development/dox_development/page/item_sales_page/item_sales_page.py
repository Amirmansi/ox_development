# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE


import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count, Max
from pypika.terms import Case
from erpnext.stock.utils import get_stock_balance
from frappe.utils import today


@frappe.whitelist()
def get_warehouse_info(item):
    warehouse_list = frappe.db.get_list("Warehouse", pluck="name")
    data = []
    for warehouse in warehouse_list:
        data.append(
            {
                "item": item,
                "warehouse": warehouse,
                "qty": get_stock_balance(item, warehouse, today()),
            }
        )
    return data


# item			item_code;	origin;	brand
# price list
# item price	item_code;	price_list;	rate
@frappe.whitelist()
def get_info(search=None):
    # FINAL DB QUERY DYNAMIC CODE START
    filter_list = frappe.db.sql(
        f"""
	SELECT GROUP_CONCAT( DISTINCT
			CONCAT(
				"MAX(CASE WHEN `tabItem Price`.price_list = '",
				`tabItem Price`.price_list,
				"' THEN `tabItem Price`.`price_list_rate` END) '",
				`tabItem Price`.price_list,"'"
				)
			)
			FROM `tabItem Price` LEFT JOIN `tabPrice List`
			ON `tabItem Price`.`price_list`= `tabPrice List`.`name`
			WHERE (`tabPrice List`.`selling` = '1')
	"""
    )
    # filter_list = frappe.db.sql(
    # f"""
    # SELECT GROUP_CONCAT(DISTINCT CONCAT("MAX(CASE WHEN `tabItem Price`.price_list = '",`tabItem Price`.price_list,"' THEN `tabItem Price`.`price_list_rate` END) '", `tabItem Price`.price_list,"'")) FROM `tabItem Price`
    # """
    # )
    # return filter_list

    search_query = ""
    if not search == None:
        search_query = f"""
			WHERE (`tabItem`.`item_code` LIKE '%{search}%')
		"""
    result = frappe.db.sql(
        f"""
	SELECT 	`tabItem`.`item_code` as 'Item Code',
			`tabItem`.`brand` as 'Brand',
			`tabItem`.`country_of_origin` as 'Origin',
			{filter_list[0][0]},
			(SELECT IFNULL(SUM(`tabBin`.`actual_qty`), 0) FROM `tabBin` WHERE `tabBin`.`item_code`=`tabItem Price`.`item_code`) as 'Total Stock Qty'
			FROM `tabItem Price` 
			JOIN `tabItem` 
			ON `tabItem Price`.`item_code`=`tabItem`.`item_code`
			{search_query}
			GROUP BY `tabItem Price`.`item_code`
	""",
        as_dict=1,
    )
    return result
    # FINAL DB QUERY DYNAMIC CODE END

    # item_price = frappe.qb.DocType('Item Price')
    # item = frappe.qb.DocType('Item')
    # result = (frappe.qb.from_(item_price)
    # .inner_join(item)
    # .on(item_price.item_code == item.item_code).select(
    # 	item_price.item_code,
    # 	item.brand,
    # 	item.country_of_origin,
    # 	Max(Case().when(item_price.price_list == "Standard Selling", item_price.price_list_rate)).as_('standard_selling'),
    # 	Max(Case().when(item_price.price_list == "Standard Buying", item_price.price_list_rate)).as_('standard_buying')
    # 	).groupby(item_price.item_code))

    # return result.run(as_dict=1)

    # item_price = frappe.get_all("Item Price", fields=["item_code","price_list","price_list_rate"])
    # return item_price
    # Item = frappe.qb.DocType('Item')
    # ItemPrice = frappe.qb.DocType('Item Price')

    # query = (frappe.qb.from_(ItemPrice)).inner_join(Item).on(Item.item_code == ItemPrice.item_code).select(Item.item_code,Item.brand,Item.country_of_origin,ItemPrice.price_list,ItemPrice.price_list_rate).run()

    # SET @sql = NULL;
    # SELECT
    # GROUP_CONCAT(DISTINCT
    # 			CONCAT('MAX(IF(s.price_list = "', `price_list`,'", `price_list_rate`,"")) AS ',price_list)
    # 			) INTO @sql
    # FROM `tabItem Price`;
    # SET @sql = CONCAT('SELECT s.item_code,  ', @sql, '
    # 				FROM `tabItem Price` s
    # 				GROUP BY s.item_code
    # 				ORDER BY s.item_code');
    # SELECT @sql;
    # PREPARE stmt FROM @sql;
    # EXECUTE stmt;

    # static working
    # SELECT
    # item_code,
    # MAX(CASE WHEN price_list = "Standard Selling" THEN price_list_rate END) "standard_selling",
    # MAX(CASE WHEN price_list = "Standard Buying" THEN price_list_rate END) "standard_buying"
    # FROM `tabItem Price`
    # GROUP BY item_code
    # ORDER BY item_code ASC

    #  SELECT GROUP_CONCAT(DISTINCT CONCAT("MAX(CASE WHEN price_list = `",price_list,"` THEN price_list_rate END) `", REPLACE(price_list,' ','_'),"`")) FROM `tabItem Price`

    # item_price = frappe.qb.DocType('Item Price')
    # item = frappe.qb.DocType('Item')
    # result = frappe.qb.from_(item_price).select("CASE WHEN price_list = `price_list` THEN price_list_rate END ` REPLACE(price_list,' ','_'),").groupby(item_price.price_list).run()
    # price_list_data = frappe.qb.from_(item_price).select("price_list").groupby(item_price.price_list).run()

    # result = frappe.qb.from_(item_price).select(
    # 	"item_code",
    # 	Max(Case().when(item_price.price_list == "Standard Selling", item_price.price_list_rate).as_('standard_selling')),
    # 	Max(Case().when(item_price.price_list == "Standard Buying", item_price.price_list_rate).as_('standard_buying'))
    # 	).groupby(item_price.item_code)

    # return result.run()

    # return str(result)

    # result = frappe.qb.from_(item_price).select(
    # 	"item_code",
    # 	Max(Case().when(item_price.price_list == "Standard Selling", item_price.price_list_rate).as_('standard_selling')),
    # 	Max(Case().when(item_price.price_list == "Standard Buying", item_price.price_list_rate).as_('standard_buying'))
    # 	).groupby(item_price.item_code)

    # return result.run()
    # SELECT GROUP_CONCAT(DISTINCT CONCAT("MAX(CASE WHEN price_list = '",price_list,"' THEN price_list_rate END) '", REPLACE(price_list,' ','_'),"'")) FROM `tabItem Price`
    # SELECT GROUP_CONCAT(DISTINCT CONCAT("MAX(CASE WHEN tabItem Price.price_list = '",tabItem Price.price_list,"' THEN tabItem Price.price_list_rate END) '", `tabItem Price.price_list`,"'")) FROM `tabItem Price`

    # filter_list = frappe.db.sql(
    # f"""
    # SELECT GROUP_CONCAT(DISTINCT CONCAT("MAX(CASE WHEN price_list = '",price_list,"' THEN price_list_rate END) '", price_list,"'")) FROM `tabItem Price`
    # """
    # )

    # return filter_list

    # MAX(CASE WHEN `price_list`='Standard Selling' THEN `price_list_rate` END) `standard_selling`,
    # MAX(CASE WHEN `price_list`='Standard Buying' THEN `price_list_rate` END) `standard_buying`

    # result = frappe.db.sql(
    # f"""
    # SELECT `item_code`,
    # {filter_list[0][0]}
    # FROM `tabItem Price` GROUP BY `item_code`
    # """
    # ,as_dict=1)
    # return result
    # return f"""
    # SELECT `tabItem.item_code`, `tabItem.country_of_origin`,  `tabItem.brand`,
    # {filter_list[0][0]}
    # FROM `tabItem`
    # INNER JOIN `tabItem Price` ON `tabItem.item_code` = `tabItem Price.item_code`
    #  GROUP BY `item_code`
    # """

    # {filter_list[0][0]}

    # result = frappe.db.sql(
    # f"""
    # SELECT `item_code`
    # FROM `tabItem` as I
    # INNER JOIN `tabItem Price` as IP ON `I.item_code` = `IP.item_code`
    #  GROUP BY `IP.item_code`
    # """
    # )
    # return str(result)

    # MAX(CASE WHEN `tabItem Price`.`price_list`='Standard Selling' THEN `tabItem Price`.`price_list_rate` END) as standard_selling,
    # MAX(CASE WHEN `tabItem Price`.`price_list`='Standard Buying' THEN `tabItem Price`.`price_list_rate` END) as standard_buying

    # 	SET @sub = MAX(CASE WHEN price_list = `Standard Buying` THEN price_list_rate END) `Standard_Buying`,MAX(CASE WHEN price_list = `Standard Selling` THEN price_list_rate END) `Standard_Selling`
    # 	SELECT
    # 		item_code,
    # 		@sub
    # 	FROM `tabItem Price`
    # 	GROUP BY item_code
    # 	ORDER BY item_code ASC

    # 	"""
    # )

    # query = ""
    # for q in result:
    # 	query+=q[0]
    # return query


# 	-- create a table
# CREATE TABLE exams (
#         pkey INTEGER,
#         item_code varchar(15),
#         price_list varchar(15),
#         price_list_rate int,
#         PRIMARY KEY  (pkey)
#       );

#       insert into exams (item_code,price_list,price_list_rate) values ('Bob','Standard Selling',75);
#       insert into exams (item_code,price_list,price_list_rate) values ('Bob','Standard Buying',77);


#       insert into exams (item_code,price_list,price_list_rate) values ('Sue','Standard Selling',90);
#       insert into exams (item_code,price_list,price_list_rate) values ('Sue','Standard Buying',97);

#       select * from exams;

#       select item_code,
# price_list_rate*(1-abs(sign(price_list-'Standard Selling'))) as selling,
# price_list_rate*(1-abs(sign(price_list-'Standard Buying'))) as buying
# from exams group by item_code;

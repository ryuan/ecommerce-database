--Let's relate product variants in each order, and the seller for those variants.
--From the joined table, we can aggregate by sellers to find the top 20 sellers by sales.
--We can also determine their average order value and the quantity of items sold.
SELECT
    bus_name AS seller,
    ROUND(SUM(price)*0.01, 2) AS total_sales,
    ROUND(AVG(price)*0.01, 2) AS avg_order_value,
    COUNT(o_id) AS num_sales
FROM
    orders
    JOIN ord_var USING(o_id)
    JOIN variants USING(v_id)
    JOIN sell_prod USING(p_id)
    JOIN sellers USING(s_id)
GROUP BY
    s_id
ORDER BY
    total_sales DESC
LIMIT
    20
;


--We join tables based on orders, collections, and the variants in each order.
--We then rank the top 3 Memorial Day collections with less than 35,000 products based on sales.
SELECT
    c_name AS mem_day_collection,
    ROUND(SUM(price)*0.01, 2) AS total_sales,
    COUNT(p_id) AS num_products
FROM
    orders
    NATURAL JOIN ord_var
    NATURAL JOIN variants
    NATURAL JOIN coll_prod
    NATURAL JOIN collections
WHERE
    c_name LIKE '%Memorial Day%'
GROUP BY
    c_id
HAVING
    num_products < 35000
ORDER BY
    total_sales DESC
LIMIT
    3
;


--Let's combine two subqueries now, one to extract count of low stock variants for each seller,
--and another to count the total number of variants for each seller.
--Joining the two, we can return the top 20 sellers with the highest percent of sold out variants.
SELECT
    seller,
    num_sold_out,
    total_stock,
    ROUND((num_sold_out * 1.0 / total_stock) * 100, 2) AS pct_sold_out
FROM (
    SELECT
        bus_name AS seller,
        COUNT(quantity) AS num_sold_out
    FROM
        sellers
        NATURAL JOIN sell_prod
        NATURAL JOIN variants
    WHERE
        quantity = 10
    GROUP BY
        seller
    ORDER BY
        num_sold_out DESC
    )
    NATURAL JOIN (
    SELECT
        bus_name AS seller,
        COUNT(quantity) AS total_stock
    FROM
        sellers
        NATURAL JOIN sell_prod
        NATURAL JOIN variants
    GROUP BY
        seller
    ORDER BY
        total_stock DESC
    )
ORDER BY
    pcnt_sold_out DESC
LIMIT
    20
;


--We find the percent of orders where the order's shipping addres matches 
--the customer's stated default shipping address in their account settings.
SELECT
    same_add_id * 1.0 / any_id AS pct_same_ship_add
FROM (
    SELECT
        COUNT(o_id) AS same_add_id
    FROM
        customers
        NATURAL JOIN ord_cust
        NATURAL JOIN orders
    WHERE
        def_ship_add = ship_add
    )
    NATURAL JOIN (
    SELECT
        COUNT(o_id) AS any_id
    FROM
        customers
        NATURAL JOIN ord_cust
        NATURAL JOIN orders
    )
;
--Summary of each non-trivial order (orders over $100 in value), highlighting the sum order subtotal, 
--ship cost, and total with shipping. Identifies the customer for analytics or marketing.
--Uses (1) aggregation with (1) HAVING, (1) orders_overview VIEW, and (1) ON variation of JOIN.
SELECT
    po_num,
    oo.o_date,
    oo.o_time,
    SUM(price_dol * 100) / 100 AS subtotal,
    ship_cost,
    SUM(price_dol * 100) / 100 + ship_cost AS total,
    cust_name
FROM
    orders_overview oo
    JOIN orders ON po_num = o_id
GROUP BY
    po_num
HAVING
    subtotal > 100
ORDER BY
    po_num ASC
;


--Returns the stock status of for all products, easily identifying out-of-stock and low-stock SKUs.
--Also shows who the seller is, allowing triggers to notify them to replinish stock.
--Uses (2) aggregation on v_id, (2) product_master VIEW, (2) NATURAL JOIN variation, and (1) CASE stmt.
SELECT
    p_name,
    type,
    bus_name AS fulfilled_by,
    v_title,
    v_name,
    SKU,
    quantity,
    CASE
        WHEN quantity > 10 THEN 'in_stock'
        WHEN quantity = 0 THEN 'out_of_stock'
        ELSE 'low_stock'
    END AS stock_level
FROM
    product_master
    NATURAL JOIN sell_prod
    NATURAL JOIN sellers
GROUP BY
    v_id
ORDER BY
    p_id
;


--Quickly reference a table that associates orders to each seller and their sales/fufillment duties.
--This table not only shows stock levels in case an order includes sold-out/low-stock items,
--but it can be easily filtered with other queries (as seen below) to perform analytics!
--Creates and uses (1) temporary table. Features (3) aggregation and (3) JOIN's USING variation.
CREATE TEMPORARY TABLE sell_ord AS
SELECT
    o_id,
    bus_name AS fulfilled_by,
    v_title,
    v_name,
    SKU,
    price * 0.01 AS price_dol,
    quantity
FROM
    orders
    JOIN ord_var USING(o_id)
    JOIN variants USING(v_id)
    JOIN sell_prod USING(p_id)
    JOIN sellers USING(s_id)
ORDER BY
    o_id ASC
;

SELECT
    fulfilled_by,
    SUM(price_dol) AS total_sales
FROM
    sell_ord
GROUP BY
    fulfilled_by
ORDER BY
    total_sales DESC
;


--Retrieve the password for the user with email brenda29@yahoo.com from the assumed private customers
--table by referencing through the public users VIEW table. This seems more secure for users.
--This query (3) uses the last of our yet unused VIEW, which is the user VIEW.
SELECT
    email,
    cust_password
FROM
    users
    JOIN customers ON email = cust_email
WHERE
    email = 'brenda29@yahoo.com'
;


--Show not just the products included in each collection, but the variants of each product as well.
--This is the 'true' list of items in any collection since prices+stock are associated with variants.
--Saving this query as a temp table to use in next query - let's see what we can do.
CREATE TEMPORARY TABLE coll_var AS
SELECT
    c_id,
    c_name,
    p_name,
    v_id,
    SKU,
    price
FROM
    collections
    JOIN coll_prod USING(c_id)
    JOIN products USING(p_id)
    JOIN variants USING(p_id)
;


--Wow! Using the temporary table from above, we can quickly use it
--to find the highest grossing collection on the store by joining with the orders_overview VIEW.ABORT
--Super helpful on a real website if we wanted to find out which collection page
--(such as which product category page) has generated the most amount of sales.
SELECT
    c_name,
    SUM(price_dol) AS total_sales
FROM
    coll_var
    JOIN ord_var USING(v_id)
    JOIN orders_overview ON po_num = o_id
GROUP BY
    c_id
ORDER BY
    total_sales DESC
;
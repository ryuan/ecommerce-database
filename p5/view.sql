--View for base user entity that offers greater security by omitting password and query simplicity.
CREATE VIEW users AS
SELECT
    'c' || cust_id AS id,
    cust_name AS name,
    cust_email AS email,
    cust_phone AS phone,
    'Customer' AS user_type
FROM
    customers
UNION
SELECT
    's' || s_id AS id,
    s_name,
    s_email,
    bus_phone,
    'Seller' AS user_type
FROM
    sellers
;


--View for comprehensive data for each product, joining each product with its variants and image URLs.
--This is exactly what gets exported by Shopify when you choose to export product CSV data,
--and is also the view that Shopify displays when you want to make bulk edits
--(as opposed to editing each products on its individual page). Note that p_id is excluded for safety.
--This view is really help for faster quering, and also displays user-friendly price in dollars+cents.
CREATE VIEW product_master AS
SELECT
    p_name,
    type,
    vendor,
    p_description,
    v_title,
    v_name,
    SKU,
    price * 0.01 AS price_dol,
    quantity,
    weight,
    url
FROM
    products
    NATURAL JOIN variants
    NATURAL JOIN images
ORDER BY
    p_id ASC
;


--View highlighting key order data, sorted chronologically. Summarizes each order value by summing
--all products/variants in the order and shipping costs. Also provide basic customer contact info.
CREATE VIEW orders_overview AS
SELECT
    o_id AS po_num,
    o_date,
    o_time,
    SUM(price) * 0.01 AS subtotal,
    ship_cost,
    SUM(price) * 0.01 + ship_cost AS total,
    cust_name,
    ship_add,
    o_phone,
    o_status
FROM
    orders
    NATURAL JOIN variants
    NATURAL JOIN ord_var
    NATURAL JOIN ord_cust
    NATURAL JOIN customers
GROUP BY
    o_id
ORDER BY
    o_date DESC,
    o_time DESC
;
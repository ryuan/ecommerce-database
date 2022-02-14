--Return all variants belonging to products sold by vendors Nike, Burton, or Bauer
SELECT
    p_name AS product_name,
    vendor,
    type,
    var_title,
    var_name,
    price * 0.01 AS price_dec
FROM (
    SELECT
        *
    FROM
        products
    WHERE
        vendor IN ('Nike', 'Burton', 'Bauer')
    )
    JOIN variants USING (p_id)
ORDER BY
    p_name ASC
;


--Return all orders placed by customers from Kentucky and show the order datetime and status
SELECT
    o_id AS order_num,
    cust_name,
    o_date AS order_date,
    o_time AS order_time,
    o_status AS order_status
FROM (
    SELECT
        cust_id,
        cust_name
    FROM
        customers
    WHERE
        def_ship_add LIKE '% KY %'
    )
    JOIN ord_cust USING (cust_id)
    JOIN orders USING (o_id)
ORDER BY
    o_id ASC
;


-- Return all images associated with each product on the store.
SELECT
    p_name AS product_name,
    url AS image_url
FROM
    products
    JOIN images USING (p_id)
ORDER BY
    product_name ASC
;


--Return the vendor/brand and 3rd-party seller of all products on the store
SELECT
    p_name AS product_name,
    vendor,
    bus_name AS seller_name
FROM
    products
    JOIN sell_prod USING (p_id)
    JOIN sellers USING (s_id)
ORDER BY
    seller_name ASC
;


--Return all collections and their products, sorted by collection name then product name
SELECT
    c_name AS collection,
    p_name AS product_name
FROM
    collections
    JOIN coll_prod USING (c_id)
    JOIN products USING (p_id)
ORDER BY
    collection ASC,
    product_name ASC
;
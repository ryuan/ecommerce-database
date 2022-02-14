--Calculate the average price of all products (considering all variants)
--for vendors Billabong, CCM, West Elm, Anthropologie
SELECT
    vendor
    type,
    AVG(price * 0.01) AS price_dec
FROM (
    SELECT
        *
    FROM
        products
    WHERE
        vendor IN ('Billabong', 'CCM', 'West Elm', 'Anthropologie')
    )
    JOIN variants USING (p_id)
GROUP BY
    vendor
ORDER BY
    price_dec ASC
;


--Calculate the top 5 product types with the most number of products
SELECT
    type,
    COUNT(p_id) AS num_products
FROM
    products
GROUP BY
    type
ORDER BY
    num_products DESC
LIMIT
    5
;


--Calculate the top 5 sellers in terms of number of orders
SELECT
    bus_name,
    COUNT(o_id) AS num_orders
FROM
    orders
    JOIN ord_prod USING (o_id)
    JOIN sell_prod USING (p_id)
    JOIN sellers USING (s_id)
GROUP BY
    bus_name
ORDER BY
    num_orders DESC
LIMIT
    5
;

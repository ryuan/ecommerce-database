--Select all sold-out variant SKUs that have distinct variant titles (size, color)

SELECT 
    sku 
FROM 
    variants 
WHERE (
    quantity == 0
    AND
    var_title != 'Title'
    )
;

--Filter for all orders that have been canceled or refunded in the past 2 years, sorted by order date

SELECT
    o_id,
    o_date
FROM
    orders
WHERE
    (o_status == "Canceled" OR o_status == "Refund Requested" OR o_status == "Refunded")
    AND
    o_date > date('now', '-2 years')
ORDER BY
    o_date DESC
;

--Find all customers and their email whose default shipping address is in Virginia, sorted by name

SELECT
    cust_name,
    cust_email
FROM
    customers
WHERE
    def_ship_add LIKE '% VA %'
ORDER BY
    cust_name ASC
;
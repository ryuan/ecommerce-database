--INSERT a new 3rd-party seller named Harry Potter, then UPDATE his hashed password
INSERT INTO sellers
VALUES (
    10, 
    'Harry Potter',  
    'potter@uchicago.edu', 
    'aweubfauwkebau13284132987421394bquwebuwyb', 
    'Hogwarts Inc.',
    '646-888-6666',
    '333-342132'
    )
;


--INSERT new coffee table product
INSERT INTO products
VALUES (
    30,
    'Athena Bohemian Handcarved Coffee Table',
    'Home',
    'Safavieh',
    'A chic, rustic coffee table with Mayan tribal pattern handcarved by master artisans out of acacia wood. Perfect for any living room seeking a statement piece.'
    )
;


--INSERT using output control products of 'Home' type into collections with 'Furniture' in title
INSERT INTO coll_prod(c_id, p_id)
SELECT
    c_id,
    p_id
FROM (
    SELECT
        c_id
    FROM
        collections
    WHERE
        c_name LIKE '%Furniture%'
    GROUP BY
        c_id
    )
    JOIN (
    SELECT
        p_id
    FROM
        products
    WHERE
        type = 'Home'
    )
;


--INSERT using output control sellers as customers
INSERT INTO customers(cust_name, cust_email, cust_password, cust_phone)
SELECT
    s_name,
    s_email,
    s_password,
    bus_phone
FROM
    sellers
;


--DELETE all products whose vendor is Burton
DELETE FROM products
WHERE
    vendor = 'Burton'
;


--DELETE all variants whose price is over $200
DELETE FROM variants
WHERE
    price > 20000
;


--UPDATE the password of the Harry Potter entry created earlier from the sellers table
UPDATE sellers
SET s_password = '2ABC4F4DDBA9B2F6ABA8E767AEB453D46D9DC4A5FCFB531D663723D04B804F56'
WHERE s_name = 'Harry Potter'
;


--UPDATE the order status of PO#16 to 'Delivered' from 'Shipped'
UPDATE orders
SET o_status = 'Delivered'
WHERE o_id = '16'
;
--Modifications to activate validate_email_format trigger
--The below modification will fail due to invalid email format
INSERT INTO customers (cust_name, cust_email, cust_password, cust_phone)
    VALUES ('Aerys Targaryen', 'burnthemall@gmail', '12d08adaf1c5d2ae0ebacb5aeda0b8ea9bd65be177c3d4a0bec2433eff1bf123', '646-123-4567')
;
--The below modification will succeed
INSERT INTO customers (cust_name, cust_email, cust_password, cust_phone)
    VALUES ('Daenerys Targaryen', 'dragonlover@gmail.com', 'dt4238b993864aa36bba4d5f8084eac221dbc3e6ffb8875cd94ec002cf1d27xz', '241-765-4321')
;
--Query to verify that customer data for Aerys failed to insert, but data for Daenerys succeeded:
SELECT
    cust_id,
    cust_name,
    cust_email
FROM
    customers
WHERE
    cust_name LIKE '%Targaryen%'
;

--Modifications to activate log_customer_contact_update trigger
--The below mod will fail due to not updating either email or phone number
UPDATE customers
SET
    cust_name = 'Robert Baratheon'
WHERE
    cust_id = 1
;
--The below modification will succeed
UPDATE customers
SET
    cust_phone = '243-513-4239',
    cust_email = 'imbored@yahoo.com'
WHERE
    cust_id = 1
;
--Query to verify that the data for customer with id=1 updated only for phone number and email:
SELECT
    *
FROM
    user_logs
WHERE
    user_id = 1 AND user_type = 'CUSTOMER'
;

--Modifications to activate log_seller_contact_update trigger
--The below mod will fail due to not updating either email or phone number
UPDATE sellers
SET
    s_name = 'Stannis Baratheon'
WHERE
    s_id = 1
;
--The below modification will succeed
UPDATE sellers
SET
    bus_phone = '888-321-7654',
    s_email = 'sonoffire@gmail.com'
WHERE
    s_id = 1
;
--Query to verify that the data for customer with id=1 updated only for phone number and email:
SELECT
    *
FROM
    user_logs
WHERE
    user_id = 1 AND user_type = 'SELLER'
;

--Modifications to activate verify_product_name_length trigger
--The below modification will fail due to product name shorter than 4 chars
INSERT INTO products (p_name, type, vendor)
    VALUES ('RXXT', 'Graphics Card', 'AMD')
;
--The below modification will succeed
INSERT INTO products (p_name, type, vendor)
    VALUES ('Radeon RX 6900 XT', 'Graphics Card', 'AMD')
;
--Query to verify that the Radeon RX 6900 XT GPU is the only graphics card on the store:
SELECT
    *
FROM
    products
WHERE
    vendor = 'AMD'
;
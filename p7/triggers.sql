--Integrity constraint on email format of a new customer account data
CREATE TRIGGER validate_email_format
    BEFORE INSERT ON customers
BEGIN
    SELECT
        CASE
            WHEN new.cust_email NOT LIKE '%_@__%.__%' THEN
                RAISE (ABORT, 'Your email is not in a valid format')
        END;
END
;

--2 triggers for logging changes to email and phone number of customer and seller user accounts
--I would like to test if a single, unified log can be used to track changes in two tables
CREATE TRIGGER log_customer_contact_update
    AFTER UPDATE ON customers
    WHEN old.cust_phone <> new.cust_phone OR old.cust_email <> new.cust_email
BEGIN
    INSERT INTO user_logs (
        user_id,
        old_phone,
        new_phone,
        old_email,
        new_email,
        user_action,
        user_type,
        created_at
    )
    VALUES (
        new.cust_id,
        old.cust_phone,
        new.cust_phone,
        old.cust_email,
        new.cust_email,
        'UPDATE',
        'CUSTOMER',
        DATETIME('NOW')
    );
END
;

CREATE TRIGGER log_seller_contact_update
    AFTER UPDATE ON sellers
    WHEN old.bus_phone <> new.bus_phone OR old.s_email <> new.s_email
BEGIN
    INSERT INTO user_logs (
        user_id,
        old_phone,
        new_phone,
        old_email,
        new_email,
        user_action,
        user_type,
        created_at
    )
    VALUES (
        new.s_id,
        old.bus_phone,
        new.bus_phone,
        old.s_email,
        new.s_email,
        'UPDATE',
        'SELLER',
        DATETIME('NOW')
    );
END
;

--Trigger to check the length of name for a new product
CREATE TRIGGER verify_product_name_length
    BEFORE INSERT ON products
BEGIN
    SELECT
        CASE
            WHEN length(new.p_name) < 5 THEN
            RAISE (ABORT, 'The product name is too short (less than 5 characters)')
        END;
END
;
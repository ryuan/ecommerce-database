--------------------------
-------- ENTITIES --------
--------------------------

--
-- Name: products; Type: TABLE
--

CREATE TABLE products (
    p_id integer,
    p_name varchar() NOT NULL,
    p_description varchar(),
    type varchar(),
    vendor varchar(),
    PRIMARY KEY (p_id)
);

--
-- Name: images; Type: TABLE
--

CREATE TABLE images (
    url varchar(),
    p_id integer NOT NULL,
    PRIMARY KEY (url)
    FOREIGN KEY (p_id) REFERENCES products(p_id) ON DELETE CASCADE
);

--
-- Name: variants; Type: TABLE
--

CREATE TABLE variants (
    sku varchar(),
    opt_name varchar(),
    price integer,
    quantity integer,
    weight integer,
    p_id integer,
    PRIMARY KEY (p_id, sku, opt_name, quantity, weight),
    FOREIGN KEY (p_id) REFERENCES products(p_id) ON DELETE CASCADE
);

--
-- Name: collections; Type: TABLE
--

CREATE TABLE collections (
    c_id integer,
    c_name varchar() NOT NULL,
    c_description varchar(),
    PRIMARY KEY (c_id)
);

--
-- Name: orders; Type: TABLE
--

CREATE TABLE orders (
    o_id integer,
    ship_opt varchar() NOT NULL,
    ship_cost integer NOT NULL,
    subtotal integer NOT NULL,
    tax integer NOT NULL,
    total integer NOT NULL,
    bill_add varchar() NOT NULL,
    ship_add varchar() NOT NULL,
    o_email varchar() NOT NULL,
    o_date datetime() NOT NULL,
    o_phone varchar() NOT NULL,
    o_status varchar() NOT NULL,
    PRIMARY KEY (o_id)
);

--
-- Name: customers; Type: TABLE
--

CREATE TABLE customers (
    cust_id integer,
    cust_name varchar() NOT NULL,
    cust_email varchar() NOT NULL,
    cust_password varchar() NOT NULL,
    def_bill_add varchar(),
    def_ship_add varchar(),
    cust_phone varchar() NOT NULL,
    tax_exempt boolean NOT NULL,
    PRIMARY KEY (cust_id)
);

--
-- Name: sellers; Type: TABLE
--

CREATE TABLE sellers (
    s_id integer,
    s_name varchar() NOT NULL,
    s_email varchar() NOT NULL,
    s_password varchar() NOT NULL,
    bus_name varchar() NOT NULL,
    bus_phone varchar() NOT NULL,
    ein integer NOT NULL,
    PRIMARY KEY (s_id)
);

---------------------------
------ RELATIONSHIPS ------
---------------------------

--
-- Name: coll_prod; Type: TABLE
--

CREATE TABLE coll_prod (
    c_id integer NOT NULL,
    p_id integer NOT NULL,
    FOREIGN KEY (c_id) REFERENCES collections(c_id),
    FOREIGN KEY (p_id) REFERENCES products(p_id)
);

--
-- Name: sell_prod; Type: TABLE
--

CREATE TABLE sell_prod (
    s_id integer NOT NULL,
    p_id integer NOT NULL,
    FOREIGN KEY (s_id) REFERENCES sellers(s_id),
    FOREIGN KEY (p_id) REFERENCES products(p_id)
);

--
-- Name: ord_prod; Type: TABLE
--

CREATE TABLE ord_prod (
    o_id integer NOT NULL,
    p_id integer NOT NULL,
    FOREIGN KEY (o_id) REFERENCES orders(o_id),
    FOREIGN KEY (p_id) REFERENCES products(p_id)
);

--
-- Name: ord_cust; Type: TABLE
--

CREATE TABLE ord_cust (
    o_id integer NOT NULL,
    cust_id integer NOT NULL,
    FOREIGN KEY (o_id) REFERENCES orders(o_id),
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
);


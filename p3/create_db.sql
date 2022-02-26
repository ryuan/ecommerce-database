--------------------------
-------- ENTITIES --------
--------------------------

--
-- Name: products; Type: TABLE
--

CREATE TABLE products (
    p_id integer,
    p_name varchar(255) NOT NULL,
    type varchar(255),
    vendor varchar(255),
    PRIMARY KEY (p_id)
);

--
-- Name: images; Type: TABLE
--

CREATE TABLE images (
    url varchar(255),
    p_id integer NOT NULL,
    PRIMARY KEY (url)
    FOREIGN KEY (p_id) REFERENCES products(p_id) ON DELETE CASCADE
);

--
-- Name: variants; Type: TABLE
--

CREATE TABLE variants (
    v_id integer,
    sku varchar(255),
    v_title varchar(255) NOT NULL,
    v_name varchar(255) NOT NULL,
    price integer,
    quantity integer,
    weight integer,
    p_id integer,
    PRIMARY KEY (v_id),
    FOREIGN KEY (p_id) REFERENCES products(p_id) ON DELETE CASCADE
);

--
-- Name: collections; Type: TABLE
--

CREATE TABLE collections (
    c_id integer,
    c_name varchar(255) NOT NULL,
    PRIMARY KEY (c_id)
);

--
-- Name: orders; Type: TABLE
--

CREATE TABLE orders (
    o_id integer,
    ship_opt varchar(255) NOT NULL,
    ship_cost integer NOT NULL,
    bill_add varchar(255) NOT NULL,
    ship_add varchar(255) NOT NULL,
    o_date date NOT NULL,
    o_time time NOT NULL,
    o_phone varchar(255) NOT NULL,
    o_status varchar(255) NOT NULL,
    PRIMARY KEY (o_id)
);

--
-- Name: customers; Type: TABLE
--

CREATE TABLE customers (
    cust_id integer,
    cust_name varchar(255) NOT NULL,
    cust_email varchar(255) NOT NULL,
    cust_password varchar(255) NOT NULL,
    def_bill_add varchar(255),
    def_ship_add varchar(255),
    cust_phone varchar(255) NOT NULL,
    PRIMARY KEY (cust_id)
);

--
-- Name: sellers; Type: TABLE
--

CREATE TABLE sellers (
    s_id integer,
    s_name varchar(255) NOT NULL,
    s_email varchar(255) NOT NULL,
    s_password varchar(255) NOT NULL,
    bus_name varchar(255) NOT NULL,
    bus_phone varchar(255) NOT NULL,
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
-- Name: ord_var; Type: TABLE
--

CREATE TABLE ord_var (
    o_id integer NOT NULL,
    v_id integer NOT NULL,
    FOREIGN KEY (o_id) REFERENCES orders(o_id),
    FOREIGN KEY (v_id) REFERENCES variants(v_id)
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


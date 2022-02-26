--This index lets us quickly lookup pricing and quantity data.
--Orders are currently mapped to variants, and variants are mapped to products with foreign key.
--The index lets us quickly relate the two for both the first query and third query.
CREATE INDEX idx_variants ON variants (v_id, p_id, quantity, price);

--The largest relation by far is our coll_prod relation, which maps collections with all its products.
--As such, the second query takes a long time to run due to the massive 800,000 tuple dataset.
--To speed up the query, index the collection name so that references to it is immediate.
CREATE INDEX idx_collections ON collections (c_name);
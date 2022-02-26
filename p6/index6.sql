--This index lets us quickly lookup pricing and quantity data.
--Orders are currently mapped to variants, and variants are mapped to products with foreign key.
--The index lets us quickly relate the two for both the first query and third query.
CREATE UNIQUE INDEX idx_variants ON variants (v_id, p_id, quantity, price);
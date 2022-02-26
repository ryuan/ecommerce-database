--Counts the number of tuples in each relation

SELECT
    *
FROM (
    SELECT COUNT(*) AS NumTuples, 'products' AS Relation FROM products
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'images' AS Relation FROM images
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'variants' AS Relation FROM variants
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'collections' AS Relation FROM collections
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'orders' AS Relation FROM orders
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'customers' AS Relation FROM customers
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'sellers' AS Relation FROM sellers
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'coll_prod' AS Relation FROM coll_prod
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'sell_prod' AS Relation FROM sell_prod
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'ord_var' AS Relation FROM ord_var
    UNION ALL
    SELECT COUNT(*) AS NumTuples, 'ord_cust' AS Relation FROM ord_cust
    )
ORDER BY
    NumTuples DESC
;
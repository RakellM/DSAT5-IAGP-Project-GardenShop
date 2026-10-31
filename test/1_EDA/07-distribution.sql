-- 7. DISTRIBUTIONS

-- 7a. Products per category
SELECT 
    c.category_name, 
    COUNT(p.product_id) AS n
FROM categories AS c
LEFT JOIN products AS p 
    ON p.category_id = c.category_id
GROUP BY c.category_id
ORDER BY n DESC;

-- 7b. Products per supplier
SELECT 
    s.supplier_name, 
    COUNT(p.product_id) AS n
FROM suppliers AS s
LEFT JOIN products AS p 
    ON p.supplier_id = s.supplier_id
GROUP BY s.supplier_id
ORDER BY n DESC;

-- 7c. Active products below reorder level (the core restock list)
SELECT 
    product_id, 
    product_name, 
    quantity_on_hand, 
    reorder_level,
    reorder_level - quantity_on_hand AS units_to_order
FROM products
WHERE discontinued = 0
  AND quantity_on_hand < reorder_level
ORDER BY quantity_on_hand ASC;

-- 7d. Estimated stock value at cost (active products)
SELECT 
    ROUND(SUM(quantity_on_hand * cost), 2) AS stock_value_at_cost,
    COUNT(*)                               AS active_products
FROM products
WHERE discontinued = 0;

-- 6. BUSINESS-RULE SANITY

-- 6a. Order status distribution
SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC;

-- 6b. Cancelled orders must NOT have a shipped_date (expect 0 rows)
SELECT order_id, status, shipped_date
FROM orders
WHERE status = 'cancelled' AND shipped_date IS NOT NULL;

-- 6c. Shipped orders must HAVE a shipped_date (expect 0 rows)
SELECT order_id
FROM orders
WHERE status = 'shipped' AND shipped_date IS NULL;

-- 6d. shipped_date >= order_date (expect 0 rows)
SELECT order_id, order_date, shipped_date
FROM orders
WHERE shipped_date IS NOT NULL AND shipped_date < order_date;

-- 6e. unit_price vs current product price (informational — historical pricing allowed)
SELECT oi.order_item_id, oi.unit_price, p.price
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
WHERE ROUND(oi.unit_price, 2) != ROUND(p.price, 2);

-- 6f. Negative values anywhere (expect 0 for all)
SELECT 'products.price'          AS col, COUNT(*) AS bad FROM products WHERE price < 0
UNION ALL SELECT 'products.cost',            COUNT(*) FROM products WHERE cost < 0
UNION ALL SELECT 'products.quantity_on_hand',COUNT(*) FROM products WHERE quantity_on_hand < 0
UNION ALL SELECT 'products.reorder_level',   COUNT(*) FROM products WHERE reorder_level < 0
UNION ALL SELECT 'order_items.quantity',     COUNT(*) FROM order_items WHERE quantity < 0
UNION ALL SELECT 'order_items.unit_price',   COUNT(*) FROM order_items WHERE unit_price < 0;

-- 6g. cost >= price (expect 0 rows)
SELECT product_id, product_name, cost, price
FROM products WHERE cost >= price;

-- 6h. Stock health (active products only)
SELECT
  SUM(CASE WHEN quantity_on_hand = 0 THEN 1 ELSE 0 END) AS zero_stock,
  SUM(CASE WHEN quantity_on_hand > 0
            AND quantity_on_hand < reorder_level THEN 1 ELSE 0 END) AS low_stock,
  SUM(CASE WHEN quantity_on_hand >= reorder_level THEN 1 ELSE 0 END) AS ok_stock
FROM products
WHERE discontinued = 0;

-- 6i. Discontinued products: stock + sales history
SELECT p.product_id, p.product_name, p.quantity_on_hand,
       (SELECT COUNT(*) FROM order_items oi WHERE oi.product_id = p.product_id) AS sales_lines
FROM products p
WHERE p.discontinued = 1;

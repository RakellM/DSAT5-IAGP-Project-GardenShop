SELECT COUNT(*) AS total_rows,
       (SELECT COUNT(*) FROM customers)
     + (SELECT COUNT(*) FROM products)
     + (SELECT COUNT(*) FROM categories)
     + (SELECT COUNT(*) FROM orders)
     + (SELECT COUNT(*) FROM order_items)
     + (SELECT COUNT(*) FROM suppliers) AS recomputed_total
FROM customers LIMIT 1;

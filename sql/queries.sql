-- Q1: Customers whose completed orders above ₹500 total more than ₹8,000
SELECT
    customer_id,
    SUM(order_amount) AS total_spend
FROM orders
WHERE status = 'completed'
  AND order_amount > 500
GROUP BY customer_id
HAVING SUM(order_amount) > 8000
ORDER BY total_spend DESC;


-- Q2: Revenue by city and product category
SELECT
    c.city,
    p.category,
    SUM(o.order_amount) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.city, p.category
ORDER BY c.city, p.category;


-- Q3: Products priced above the average catalogue price
SELECT
    product_id,
    product_name,
    price_inr
FROM products
WHERE price_inr > (
    SELECT AVG(price_inr)
    FROM products
)
ORDER BY price_inr DESC;


-- Q4: Customers without any completed orders
SELECT
    c.customer_id,
    c.city
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
   AND o.status = 'completed'
WHERE o.order_id IS NULL
ORDER BY c.customer_id;


-- Q5: Customers whose completed spend is above
-- the average completed spend per active customer
WITH customer_spend AS (
    SELECT
        customer_id,
        SUM(order_amount) AS total_spend
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_spend
FROM customer_spend
WHERE total_spend > (
    SELECT AVG(total_spend)
    FROM customer_spend
)
ORDER BY total_spend DESC;


-- Q6: Rank customers by completed spend within each city
WITH customer_city_spend AS (
    SELECT
        c.city,
        c.customer_id,
        SUM(o.order_amount) AS total_spend
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.city, c.customer_id
)
SELECT
    city,
    customer_id,
    total_spend,
    RANK() OVER (
        PARTITION BY city
        ORDER BY total_spend DESC
    ) AS spend_rank,
    ROW_NUMBER() OVER (
        PARTITION BY city
        ORDER BY total_spend DESC, customer_id
    ) AS row_num
FROM customer_city_spend
ORDER BY city, spend_rank, customer_id;


-- Q7: Daily completed revenue and cumulative revenue
WITH daily_revenue AS (
    SELECT
        DATE(order_ts) AS order_date,
        SUM(order_amount) AS daily_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_ts)
)
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
FROM daily_revenue
ORDER BY order_date;
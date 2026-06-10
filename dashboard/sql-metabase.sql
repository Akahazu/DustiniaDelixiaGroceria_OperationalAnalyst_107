-- Total Orders
SELECT count(*) AS total_orders
FROM ddg_analytics.fact_operational_performance

-- Late Delivery Rate
SELECT
    round(avg(is_late) * 100, 2) || '%' AS late_rate_percent
FROM ddg_analytics.fact_operational_performance

-- Average Delivery Time
SELECT
    round(avg(actual_delivery_time),2) AS avg_delivery_days
FROM ddg_analytics.fact_operational_performance

-- Average Review Score
SELECT
    round(avg(review_score),2) AS avg_review
FROM ddg_analytics.fact_operational_performance

-- Bar Chart: Keterlambatan per Wilayah
SELECT
    customer_state,
    count(*) AS total_orders,
    round(avg(is_late) * 100,2) AS late_rate
FROM ddg_analytics.fact_operational_performance
GROUP BY customer_state
HAVING total_orders > 20
ORDER BY late_rate DESC

-- Bar Chart : Seller Bermasalah
SELECT
    seller_id,
    count(*) AS total_orders,
    round(avg(is_late)*100,2) AS late_rate
FROM ddg_analytics.fact_operational_performance
GROUP BY seller_id
HAVING total_orders > 10
ORDER BY late_rate DESC
LIMIT 10

-- Scatter Plot : Seller Process Days Vs Days Delayed
SELECT
    seller_process_days,
    days_delayed
FROM ddg_analytics.fact_operational_performance
WHERE days_delayed > 0
limit 200

-- Scatter Plot : Transit Kurir Vs Days Delayed
SELECT
    carrier_transit_days,
    days_delayed
FROM ddg_analytics.fact_operational_performance
WHERE days_delayed > 0
limit 200

-- Customer Satisfaction
SELECT
    actual_delivery_time,
    review_score
FROM ddg_analytics.fact_operational_performance

-- Table : Distribusi Review
SELECT
    review_score,
    count(*) AS total
FROM ddg_analytics.fact_operational_performance
GROUP BY review_score
ORDER BY review_score

-- Grouped Bar Chart : Seller Type Performance
SELECT
    seller_type,
    count(*) AS total_orders,
    round(avg(is_late)*100,2) AS late_rate,
    round(avg(review_score),2) AS avg_review
FROM ddg_analytics.fact_operational_performance
GROUP BY seller_type
ORDER BY late_rate DESC

-- Horizontal Bar Chart : Weight Class Analysis
SELECT
    weight_class,
    round(avg(actual_delivery_time),2) AS avg_delivery_days,
    round(avg(is_late)*100,2) AS late_rate
FROM ddg_analytics.fact_operational_performance
GROUP BY weight_class

-- Scatter Plot : Cost Efficiency
SELECT
    cost_per_km,
    actual_delivery_time,
    is_late
FROM ddg_analytics.fact_operational_performance
WHERE cost_per_km > 0

-- Pie Chart : Delay Severenity
SELECT
    CASE
        WHEN days_delayed = 0 THEN 'On Time'
        WHEN days_delayed <= 3 THEN '1-3 Days'
        WHEN days_delayed <= 7 THEN '4-7 Days'
        ELSE '>7 Days'
    END AS delay_group,
    count(*) AS total
FROM ddg_analytics.fact_operational_performance
GROUP BY delay_group

-- Horizontal Bar Chart : Negative Review Analysis
SELECT DISTINCT
    phrase,
    score
FROM ddg_analytics.top_negative_bigrams
ORDER BY score DESC
LIMIT 8

-- Table : Inefficient States
SELECT 
    customer_state,
    round(avg(cost_per_km), 2) as avg_cost_per_km,
    round(avg(actual_delivery_time), 2) as avg_days
FROM ddg_analytics.fact_operational_performance
WHERE cost_per_km > 0
GROUP BY customer_state
ORDER BY avg_cost_per_km DESC
LIMIT 10

-- Table : Review Vs Keterlambatan
SELECT 
    CASE WHEN is_late = 1 THEN 'TELAT' ELSE 'TEPAT WAKTU' END AS status,
    round(avg(review_score), 2) as avg_review_score,
    count(*) as total_orders
FROM ddg_analytics.fact_operational_performance
GROUP BY status

--  Table : Time Composition 
SELECT 
    round(avg(seller_process_days), 2) as avg_seller_time,
    round(avg(carrier_transit_days), 2) as avg_carrier_time
FROM ddg_analytics.fact_operational_performance
WHERE is_late = 1

-- carrier vs seller delay contribution
SELECT
    CASE
        WHEN seller_process_days > carrier_transit_days
            THEN 'Seller Processing'
        ELSE 'Carrier Transit'
    END AS dominant_delay_source,
    count(*) AS total
FROM ddg_analytics.fact_operational_performance
WHERE is_late = 1
GROUP BY dominant_delay_source

-- Grouped Bar Chart : Delivery Matrix
SELECT
    seller_type,
    round(avg(actual_delivery_time),2) AS avg_delivery,
    round(avg(review_score),2) AS avg_review,
    count(*) AS total_orders
FROM ddg_analytics.fact_operational_performance
GROUP BY seller_type
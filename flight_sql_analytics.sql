-- ============================================================
--  CREATE TABLE
--  Match every column in the CSV exactly.
-- ============================================================

Drop TABLE IF EXISTS airline_otp;
CREATE TABLE airline_otp (
    year        INTEGER,
    month_num   INTEGER,
    month_name  VARCHAR(20),
    airline     VARCHAR(100),
    otp_pct     DECIMAL(5,2),
    otp_status  VARCHAR(30)
);

Drop TABLE IF EXISTS carrier_traffic;
CREATE TABLE carrier_traffic (
    airline          VARCHAR(100),
    year             INTEGER,
    month            INTEGER,
	aircraft_count   NUMERIC,
	passenger_count  NUMERIC,
    load_factor_pct  DECIMAL(8,3),
    month_name      VARCHAR(20)
);
select * from carrier_traffic;

Drop TABLE IF EXISTS route_traffic;
CREATE TABLE route_traffic (
    year         INTEGER,
    month        INTEGER,
    origin_city  VARCHAR(100),
    dest_city    VARCHAR(100),
    pax_to       BIGINT,
    pax_from     BIGINT,
    total_pax    BIGINT
);

Drop TABLE IF EXISTS daily_otp;
CREATE TABLE daily_otp (
    date         DATE,
    year         INTEGER,
    month        INTEGER,
    otp_indigo   DECIMAL(5,2),
    otp_airindia DECIMAL(5,2),
    otp_spicejet DECIMAL(5,2),
    otp_vistara  DECIMAL(5,2),
    otp_akasa    DECIMAL(5,2),
    plf_indigo   DECIMAL(5,2),
    plf_airindia DECIMAL(5,2)
);

--==================================
-- IMPORTING CLEAN FILES AND VERIFY
--==================================
SELECT * FROM airline_otp
LIMIT 5;

SELECT *FROM carrier_traffic
LIMIT 5;

SELECT * FROM daily_otp
LIMIT 5;

SELECT * FROM route_traffic
LIMIT 5;

--==========================
-- BUSINESS QUESTIONS 
--==========================

-- ── QUERY 1: Overall OTP KPI Summary ────────────────────────────

SELECT
    COUNT(DISTINCT airline)                          AS total_airlines,
    COUNT(*)                                         AS total_records,
    ROUND(AVG(otp_pct)::NUMERIC, 2)                  AS avg_otp_pct,
    ROUND(MIN(otp_pct)::NUMERIC, 2)                  AS worst_otp,
    ROUND(MAX(otp_pct)::NUMERIC, 2)                  AS best_otp,
    SUM(CASE WHEN otp_status = 'Above Benchmark'
             THEN 1 ELSE 0 END)                      AS months_above_benchmark,
    SUM(CASE WHEN otp_status = 'Below Benchmark'
             THEN 1 ELSE 0 END)                      AS months_below_benchmark
FROM airline_otp;
 
 
-- ── QUERY 2: Airline OTP Ranking with RANK() ────────────────────
-- Who is India's most punctual airline Jan–May 2024?

SELECT
    airline,
    ROUND(AVG(otp_pct)::NUMERIC, 2)                  AS avg_otp_pct,
    ROUND(MIN(otp_pct)::NUMERIC, 2)                  AS worst_month_otp,
    ROUND(MAX(otp_pct)::NUMERIC, 2)                  AS best_month_otp,
    COUNT(CASE WHEN otp_status = 'Above Benchmark'
               THEN 1 END)                           AS months_above_benchmark,
    RANK() OVER (ORDER BY AVG(otp_pct) DESC)         AS otp_rank
FROM airline_otp
GROUP BY airline
ORDER BY avg_otp_pct DESC;
 
 
-- ── QUERY 3: Month-over-Month OTP Change using LAG() ────────────
-- Which airline improved or worsened each month?
SELECT
    airline,
    month_name,
    month_num,
    otp_pct,
    LAG(otp_pct) OVER (
        PARTITION BY airline
        ORDER BY month_num
    )                                                AS prev_month_otp,
    ROUND((otp_pct - LAG(otp_pct) OVER (
        PARTITION BY airline ORDER BY month_num
    ))::NUMERIC, 2)                                  AS otp_change,
    CASE
        WHEN otp_pct > LAG(otp_pct) OVER (
            PARTITION BY airline ORDER BY month_num)
        THEN 'Improved'
        WHEN otp_pct < LAG(otp_pct) OVER (
            PARTITION BY airline ORDER BY month_num)
        THEN 'Declined'
        ELSE 'No Change'
    END                                              AS trend
FROM airline_otp
ORDER BY airline, month_num;
 
 
-- ── QUERY 4: Worst Performing Months using CTE ──────────────────
-- Which month had the worst OTP across all airlines?
WITH monthly_avg AS (
    SELECT
        month_num,
        month_name,
        ROUND(AVG(otp_pct)::NUMERIC, 2)              AS avg_otp,
        COUNT(CASE WHEN otp_status = 'Below Benchmark'
                   THEN 1 END)                       AS airlines_below_benchmark
    FROM airline_otp
    GROUP BY month_num, month_name
)
SELECT
    month_name,
    avg_otp,
    airlines_below_benchmark,
    CASE
        WHEN avg_otp < 60 THEN 'Critical'
        WHEN avg_otp < 70 THEN 'Poor'
        WHEN avg_otp < 75 THEN 'Below Benchmark'
        ELSE 'Acceptable'
    END                                              AS performance_tier
FROM monthly_avg
ORDER BY avg_otp ASC;
 
 
-- ── QUERY 5: IndiGo Deep Dive ────────────────────────────────────
-- Targeted analysis for IndiGo 
SELECT
    month_name,
    otp_pct,
    otp_status,
    CASE
        WHEN otp_pct >= 85 THEN 'Above DGCA target (85%)'
        WHEN otp_pct >= 75 THEN 'Meets minimum benchmark'
        ELSE 'Below benchmark — needs improvement'
    END                                              AS performance_note,
    ROUND((otp_pct - AVG(otp_pct) OVER ())::NUMERIC,2)
                                                     AS vs_indigo_avg
FROM airline_otp
WHERE airline = 'IndiGo'
ORDER BY month_num;
 
 
-- ── QUERY 6: Top 10 Busiest Routes in India ──────────────────────
-- Route profitability proxy — passenger volume by city pair
SELECT
    origin_city,
    dest_city,
    SUM(total_pax)                                   AS total_passengers,
    ROUND(AVG(total_pax)::NUMERIC, 0)                AS avg_monthly_pax,
    COUNT(*)                                         AS months_active,
    RANK() OVER (ORDER BY SUM(total_pax) DESC)       AS route_rank
FROM route_traffic
WHERE year = 2024
GROUP BY origin_city, dest_city
ORDER BY total_passengers DESC
LIMIT 10;
 
 
-- ── QUERY 7: City Hub Analysis — Top Origin Cities ───────────────
-- Which cities are the biggest departure hubs?
SELECT
    origin_city,
    SUM(pax_to)                                      AS total_departing_pax,
    COUNT(DISTINCT dest_city)                        AS destinations_served,
    ROUND(AVG(pax_to)::NUMERIC, 0)                   AS avg_pax_per_route,
    RANK() OVER (ORDER BY SUM(pax_to) DESC)          AS hub_rank
FROM route_traffic
WHERE year = 2024
  AND pax_to > 0
GROUP BY origin_city
ORDER BY total_departing_pax DESC
LIMIT 15;
 
 
-- ── QUERY 8: Carrier Load Factor Trend using Window Function ─────
-- Is IndiGo filling its planes more over time?
SELECT
    airline,
    year,
    ROUND(AVG(load_factor_pct)::NUMERIC, 2)          AS avg_load_factor,
    ROUND(AVG(passenger_count)::NUMERIC, 0)          AS avg_monthly_passengers,
    ROUND(AVG(load_factor_pct)::NUMERIC, 2) -
    FIRST_VALUE(ROUND(AVG(load_factor_pct)::NUMERIC,2))
        OVER (PARTITION BY airline ORDER BY year)    AS change_from_first_year
FROM carrier_traffic
WHERE year >= 2019
GROUP BY airline, year
ORDER BY airline, year;
 
 
-- ── QUERY 9: Daily OTP Seasonality — Best vs Worst Months ────────
-- Using daily data to find which month has highest delays

SELECT
    month,
    TO_CHAR(TO_DATE(month::TEXT, 'MM'), 'Mon') AS month_name,
    ROUND(AVG(otp_indigo), 2)    AS indigo_avg_otp,
    ROUND(AVG(otp_airindia), 2)  AS airindia_avg_otp,
    ROUND(AVG(otp_spicejet), 2)  AS spicejet_avg_otp,
    ROUND(AVG(otp_vistara), 2)   AS vistara_avg_otp,
    COUNT(*)                     AS days_of_data
FROM daily_otp
WHERE year IN (2023, 2024)
GROUP BY month
ORDER BY month;
 
-- ── QUERY 10: High Load + Low OTP — Capacity Stress Signal ───────
-- Do airlines perform worse when they fly more passengers?
-- used JOIN across carrier_traffic + airline_otp in this  query

WITH carrier_2024 AS (
    SELECT
        airline,
        month,
        ROUND(AVG(load_factor_pct)::NUMERIC, 2)      AS avg_load_factor,
        SUM(passenger_count)                          AS total_passengers
    FROM carrier_traffic
    WHERE year = 2024
    GROUP BY airline, month
),
otp_2024 AS (
    SELECT
        airline,
        month_num  AS month,
        otp_pct
    FROM airline_otp
    WHERE year = 2024
)
SELECT
    c.airline,
    c.month,
    c.avg_load_factor,
    o.otp_pct,
    c.total_passengers,
    CASE
        WHEN c.avg_load_factor > 85
         AND o.otp_pct < 75  THEN 'Capacity Stress — High load, poor OTP'
        WHEN c.avg_load_factor > 85
         AND o.otp_pct >= 75 THEN 'Efficient — High load, good OTP'
        WHEN c.avg_load_factor <= 85
         AND o.otp_pct < 75  THEN 'Operational Issues — Low load, poor OTP'
        ELSE 'Normal Operations'
    END               AS operational_insight
FROM carrier_2024 c
JOIN otp_2024 o
  ON LOWER(c.airline) = LOWER(o.airline)
  AND c.month = o.month
ORDER BY c.airline, c.month;
 

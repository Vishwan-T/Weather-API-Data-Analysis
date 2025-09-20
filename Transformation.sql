CREATE DATABASE IF NOT EXISTS weather_db;

-- Use the database
USE weather_db;

-- Create the weather_logs table
CREATE TABLE IF NOT EXISTS weather_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_date DATE NOT NULL,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    condition VARCHAR(50) NOT NULL,
    UNIQUE KEY unique_city_date (log_date, city)
);



-- 1. Clean & Standardize Data
-- Standardize city names to Title Case
UPDATE weather_logs
SET city = CONCAT(UPPER(LEFT(city,1)), LOWER(SUBSTRING(city,2)));

-- Remove extra spaces
UPDATE weather_logs
SET city = TRIM(city);


-- 2. Aggregations & Trends
-- Average temperature per city
SELECT city, AVG(temperature) AS avg_temp
FROM weather_logs
GROUP BY city;

-- Highest & lowest temperature logged per city
SELECT city, 
       MAX(temperature) AS max_temp, 
       MIN(temperature) AS min_temp
FROM weather_logs
GROUP BY city;

-- Most frequent condition per city
SELECT city, condition, COUNT(*) AS condition_count
FROM weather_logs
GROUP BY city, condition
ORDER BY condition_count DESC;


-- 3. Daily / Monthly Analysis
-- Daily summary across all cities
SELECT log_date, 
       AVG(temperature) AS avg_temp,
       MAX(temperature) AS high_temp,
       MIN(temperature) AS low_temp
FROM weather_logs
GROUP BY log_date;

-- Monthly average temperature per city
SELECT DATE_FORMAT(log_date, '%Y-%m') AS month, city, 
       AVG(temperature) AS avg_temp
FROM weather_logs
GROUP BY month, city
ORDER BY month DESC;

-- 4. Weather Condition Insights

-- Most common weather condition overall
SELECT condition, COUNT(*) AS frequency
FROM weather_logs
GROUP BY condition
ORDER BY frequency DESC
LIMIT 1;

-- Percentage distribution of conditions
SELECT condition, 
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM weather_logs), 2) AS percentage
FROM weather_logs
GROUP BY condition;

-- 5. Advanced Transformations
-- Temperature difference between consecutive days per city
SELECT city, log_date, temperature,
       temperature - LAG(temperature) OVER (PARTITION BY city ORDER BY log_date) AS temp_diff
FROM weather_logs;

-- 7-day rolling average temperature per city
SELECT city, log_date, temperature,
       ROUND(AVG(temperature) OVER (PARTITION BY city ORDER BY log_date ROWS 6 PRECEDING), 2) AS rolling_avg_7d
FROM weather_logs;

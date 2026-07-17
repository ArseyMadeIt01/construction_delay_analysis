-- =========================================================================
-- 1. DATABASE CREATION & TABLES SETUP (DDL)
-- =========================================================================

-- Create Table: dim_contractors
CREATE TABLE dim_contractors (
    contractor_id SERIAL PRIMARY KEY,
    contractor_name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Table: dim_sectors
CREATE TABLE dim_sectors (
    sector_id SERIAL PRIMARY KEY,
    sector_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create Table: fact_projects
CREATE TABLE fact_projects (
    project_id VARCHAR(20) PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    sector_id INT REFERENCES dim_sectors(sector_id),
    contractor_id INT REFERENCES dim_contractors(contractor_id),
    target_budget_usd NUMERIC(15, 2),
    final_cost_usd NUMERIC(15, 2),
    planned_start DATE,
    actual_end DATE,
    planned_duration_days INT,
    actual_duration_days INT,
    cost_variance NUMERIC(15, 2),
    schedule_variance INT,
    cpi NUMERIC(5, 2),
    is_over_budget INT
);


-- =========================================================================
-- 2. BUSINESS INSIGHT QUERIES (DML)
-- =========================================================================

-- 📊 QUERY 1: The Contractor Hall of Shame (Time & Budget Overruns)
-- EXPLANATION: Identify which contractors average the worst cost and schedule overruns.
-- Hiring managers want to see that you can use GROUP BY, AVG, and mathematical aggregations.

SELECT 
    c.contractor_name,
    COUNT(p.project_id) AS total_completed_projects,
    ROUND(AVG(p.cost_variance), 2) AS avg_cost_variance, -- Negative means over budget
    ROUND(AVG(p.schedule_variance), 1) AS avg_schedule_variance, -- Negative means delayed
    ROUND(AVG(p.cpi), 2) AS avg_cost_performance_index,
    SUM(p.is_over_budget) * 100.0 / COUNT(p.project_id) AS pct_projects_over_budget
FROM fact_projects p
JOIN dim_contractors c ON p.contractor_id = c.contractor_id
GROUP BY c.contractor_name
ORDER BY avg_cost_variance ASC; -- Show worst over-budget contractors first


-- 📊 QUERY 2: Sector Risk Matrix
-- EXPLANATION: Analyze which sector is the riskiest to invest in.
-- Uses standard CASE statements to bucket performance.

SELECT 
    s.sector_name,
    COUNT(p.project_id) AS total_projects,
    SUM(p.target_budget_usd) AS total_planned_budget,
    SUM(p.final_cost_usd) AS total_actual_spend,
    ROUND(SUM(p.final_cost_usd) - SUM(p.target_budget_usd), 2) AS total_loss_usd,
    CASE 
        WHEN AVG(p.cpi) < 0.90 THEN 'High Risk / Low Efficiency'
        WHEN AVG(p.cpi) BETWEEN 0.90 AND 0.99 THEN 'Moderate Risk'
        ELSE 'On Track / Highly Efficient'
    END AS risk_classification
FROM fact_projects p
JOIN dim_sectors s ON p.sector_id = s.sector_id
GROUP BY s.sector_name
ORDER BY total_loss_usd DESC;


-- 📊 QUERY 3: Outlier Projects (Deep Dive Window Functions)
-- EXPLANATION: Rank projects by their cost overrun percentage *within* each sector.
-- This showcases advanced SQL skills (Window Functions) that impress technical interviewers.

WITH ranked_projects AS (
    SELECT 
        p.project_id,
        p.project_name,
        s.sector_name,
        p.target_budget_usd,
        p.final_cost_usd,
        ((p.final_cost_usd - p.target_budget_usd) / p.target_budget_usd) * 100 AS overrun_percentage,
        ROW_NUMBER() OVER (
            PARTITION BY p.sector_id 
            ORDER BY ((p.final_cost_usd - p.target_budget_usd) / p.target_budget_usd) DESC
        ) as overrun_rank
    FROM fact_projects p
    JOIN dim_sectors s ON p.sector_id = s.sector_id
    WHERE p.is_over_budget = 1
)
SELECT 
    sector_name,
    overrun_rank,
    project_id,
    project_name,
    target_budget_usd,
    final_cost_usd,
    ROUND(overrun_percentage, 1) AS budget_overrun_pct
FROM ranked_projects
WHERE overrun_rank <= 3 -- Get top 3 worst overrun projects for each sector
ORDER BY sector_name, overrun_rank;
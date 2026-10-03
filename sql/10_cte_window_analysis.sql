USE employee_analytics_dw;


-- 10_cte_window_analysis.sql
-- CTEs and Window Function Analysis




-- 1. Average Performance by Department and Year
--    Demonstrates: CTE


WITH yearly_department_performance AS (
    SELECT
        dd.department_name,
        dt.year_number,
        AVG(fpr.performance_score) AS avg_performance_score,
        COUNT(*) AS review_count
    FROM fact_performance_reviews fpr
    JOIN dim_department dd
        ON fpr.department_sk = dd.department_sk
    JOIN dim_date dt
        ON fpr.date_sk = dt.date_sk
    GROUP BY
        dd.department_name,
        dt.year_number
)
SELECT
    department_name,
    year_number,
    ROUND(avg_performance_score, 2) AS avg_performance_score,
    review_count
FROM yearly_department_performance
ORDER BY
    year_number,
    department_name;



-- 2. Rank Employees by Performance Within Department
--    Demonstrates: RANK()


WITH employee_performance AS (
    SELECT
        de.employee_id,
        CONCAT(de.first_name, ' ', de.last_name) AS employee_name,
        dd.department_name,
        AVG(fpr.performance_score) AS avg_performance_score
    FROM fact_performance_reviews fpr
    JOIN dim_employee de
        ON fpr.employee_sk = de.employee_sk
    JOIN dim_department dd
        ON fpr.department_sk = dd.department_sk
    WHERE de.employee_id <> 'UNKNOWN'
    GROUP BY
        de.employee_id,
        de.first_name,
        de.last_name,
        dd.department_name
)
SELECT
    employee_id,
    employee_name,
    department_name,
    ROUND(avg_performance_score, 2) AS avg_performance_score,
    RANK() OVER (
        PARTITION BY department_name
        ORDER BY avg_performance_score DESC
    ) AS department_rank
FROM employee_performance
ORDER BY
    department_name,
    department_rank;



-- 3. Dense Rank Employees by Performance
--    Demonstrates: DENSE_RANK()


WITH employee_scores AS (
    SELECT
        de.employee_id,
        CONCAT(de.first_name, ' ', de.last_name) AS employee_name,
        AVG(fpr.performance_score) AS avg_score
    FROM fact_performance_reviews fpr
    JOIN dim_employee de
        ON fpr.employee_sk = de.employee_sk
    WHERE de.employee_id <> 'UNKNOWN'
    GROUP BY
        de.employee_id,
        de.first_name,
        de.last_name
)
SELECT
    employee_id,
    employee_name,
    ROUND(avg_score, 2) AS avg_score,
    DENSE_RANK() OVER (
        ORDER BY avg_score DESC
    ) AS performance_rank
FROM employee_scores
ORDER BY
    performance_rank,
    employee_id;



-- 4. Year-over-Year Performance Analysis
--    Demonstrates: LAG()


WITH yearly_performance AS (
    SELECT
        dt.year_number,
        AVG(fpr.performance_score) AS avg_score
    FROM fact_performance_reviews fpr
    JOIN dim_date dt
        ON fpr.date_sk = dt.date_sk
    GROUP BY
        dt.year_number
),
performance_with_previous_year AS (
    SELECT
        year_number,
        avg_score,
        LAG(avg_score) OVER (
            ORDER BY year_number
        ) AS previous_year_score
    FROM yearly_performance
)
SELECT
    year_number,
    ROUND(avg_score, 2) AS avg_score,
    ROUND(previous_year_score, 2) AS previous_year_score,
    ROUND(
        avg_score - previous_year_score,
        2
    ) AS score_change
FROM performance_with_previous_year
ORDER BY
    year_number;



-- 5. Top Employees in Each Department
--    Demonstrates: ROW_NUMBER()


WITH employee_scores AS (
    SELECT
        de.employee_id,
        CONCAT(de.first_name, ' ', de.last_name) AS employee_name,
        dd.department_name,
        AVG(fpr.performance_score) AS avg_score
    FROM fact_performance_reviews fpr
    JOIN dim_employee de
        ON fpr.employee_sk = de.employee_sk
    JOIN dim_department dd
        ON fpr.department_sk = dd.department_sk
    WHERE de.employee_id <> 'UNKNOWN'
    GROUP BY
        de.employee_id,
        de.first_name,
        de.last_name,
        dd.department_name
),
ranked_employees AS (
    SELECT
        employee_id,
        employee_name,
        department_name,
        avg_score,
        ROW_NUMBER() OVER (
            PARTITION BY department_name
            ORDER BY avg_score DESC, employee_id
        ) AS row_num
    FROM employee_scores
)
SELECT
    employee_id,
    employee_name,
    department_name,
    ROUND(avg_score, 2) AS avg_score,
    row_num
FROM ranked_employees
WHERE row_num <= 5
ORDER BY
    department_name,
    row_num;



-- 6. Project Allocation Analysis
--    Demonstrates: CTE + aggregation


WITH project_allocation AS (
    SELECT
        dp.project_id,
        dp.project_name,
        dp.status,
        COUNT(ep.employee_id) AS employee_count,
        AVG(ep.allocation_percent) AS avg_allocation
    FROM dim_project dp
    LEFT JOIN employee_projects ep
        ON dp.project_id = ep.project_id
    GROUP BY
        dp.project_id,
        dp.project_name,
        dp.status
)
SELECT
    project_id,
    project_name,
    status,
    employee_count,
    ROUND(avg_allocation, 2) AS avg_allocation
FROM project_allocation
ORDER BY
    employee_count DESC,
    avg_allocation DESC;



-- 7. Department Attrition Analysis
--    Demonstrates: CTE + conditional aggregation


WITH department_employee_stats AS (
    SELECT
        dd.department_name,
        COUNT(*) AS total_employees,
        SUM(
            CASE
                WHEN de.attrition = 'Yes' THEN 1
                ELSE 0
            END
        ) AS attrition_count
    FROM dim_employee de
    JOIN dim_department dd
        ON de.department_id = dd.department_id
    WHERE de.is_current = 1
      AND de.employee_id <> 'UNKNOWN'
    GROUP BY
        dd.department_name
)
SELECT
    department_name,
    total_employees,
    attrition_count,
    ROUND(
        attrition_count * 100.0 / NULLIF(total_employees, 0),
        2
    ) AS attrition_rate_percent
FROM department_employee_stats
ORDER BY
    attrition_rate_percent DESC;



-- 8. Employees with Multiple Project Assignments


WITH employee_project_count AS (
    SELECT
        employee_id,
        COUNT(DISTINCT project_id) AS project_count
    FROM employee_projects
    GROUP BY employee_id
)
SELECT
    employee_id,
    project_count
FROM employee_project_count
WHERE project_count > 1
ORDER BY
    project_count DESC,
    employee_id;



-- 9. Monthly Performance Trend


WITH monthly_performance AS (
    SELECT
        dt.year_number,
        dt.month_number,
        dt.month_name,
        AVG(fpr.performance_score) AS avg_score,
        COUNT(*) AS review_count
    FROM fact_performance_reviews fpr
    JOIN dim_date dt
        ON fpr.date_sk = dt.date_sk
    GROUP BY
        dt.year_number,
        dt.month_number,
        dt.month_name
)
SELECT
    year_number,
    month_number,
    month_name,
    ROUND(avg_score, 2) AS avg_score,
    review_count
FROM monthly_performance
ORDER BY
    year_number,
    month_number;



-- 10. Highest Rated Employees


WITH employee_rating_summary AS (
    SELECT
        de.employee_id,
        CONCAT(de.first_name, ' ', de.last_name) AS employee_name,
        AVG(fpr.performance_rating) AS avg_rating,
        COUNT(*) AS review_count
    FROM fact_performance_reviews fpr
    JOIN dim_employee de
        ON fpr.employee_sk = de.employee_sk
    WHERE de.employee_id <> 'UNKNOWN'
    GROUP BY
        de.employee_id,
        de.first_name,
        de.last_name
)
SELECT
    employee_id,
    employee_name,
    ROUND(avg_rating, 2) AS avg_rating,
    review_count
FROM employee_rating_summary
ORDER BY
    avg_rating DESC,
    review_count DESC;

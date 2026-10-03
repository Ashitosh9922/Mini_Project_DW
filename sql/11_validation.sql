USE employee_analytics_dw;


-- 11_validation.sql
-- Final Data Warehouse Validation



-- 1. OLTP Row Counts


SELECT 'departments' AS table_name, COUNT(*) AS row_count
FROM departments

UNION ALL

SELECT 'employees', COUNT(*)
FROM employees

UNION ALL

SELECT 'employee_history', COUNT(*)
FROM employee_history

UNION ALL

SELECT 'projects', COUNT(*)
FROM projects

UNION ALL

SELECT 'employee_projects', COUNT(*)
FROM employee_projects

UNION ALL

SELECT 'performance_reviews', COUNT(*)
FROM performance_reviews;



-- 2. OLAP Dimension Row Counts


SELECT 'dim_department' AS table_name, COUNT(*) AS row_count
FROM dim_department

UNION ALL

SELECT 'dim_project', COUNT(*)
FROM dim_project

UNION ALL

SELECT 'dim_date', COUNT(*)
FROM dim_date

UNION ALL

SELECT 'dim_employee', COUNT(*)
FROM dim_employee

UNION ALL

SELECT 'fact_performance_reviews', COUNT(*)
FROM fact_performance_reviews;



-- 3. SCD2 Employee Validation


SELECT
    COUNT(*) AS total_dim_employee_rows,
    COUNT(DISTINCT employee_id) AS distinct_employees,
    SUM(
        CASE
            WHEN is_current = 1 THEN 1
            ELSE 0
        END
    ) AS current_records,
    SUM(
        CASE
            WHEN is_current = 0 THEN 1
            ELSE 0
        END
    ) AS historical_records
FROM dim_employee;



-- 4. Check for Multiple Current SCD2 Records
--    Expected result: 0 rows


SELECT
    employee_id,
    COUNT(*) AS current_record_count
FROM dim_employee
WHERE is_current = 1
GROUP BY employee_id
HAVING COUNT(*) > 1;



-- 5. Check Invalid SCD2 Date Ranges
--    Expected result: 0 rows


SELECT
    employee_id,
    employee_sk,
    effective_start_date,
    effective_end_date
FROM dim_employee
WHERE effective_start_date > effective_end_date;



-- 6. Check Fact Grain
--    One fact row per performance review
--    Expected result: 0 rows


SELECT
    review_id,
    COUNT(*) AS fact_row_count
FROM fact_performance_reviews
GROUP BY review_id
HAVING COUNT(*) > 1;



-- 7. Check Fact Row Count Against Source Reviews


SELECT
    (
        SELECT COUNT(*)
        FROM performance_reviews
    ) AS source_review_count,
    (
        SELECT COUNT(*)
        FROM fact_performance_reviews
    ) AS fact_review_count;



-- 8. Validate Employee Foreign-Key Resolution
--    Expected result: 0 rows


SELECT COUNT(*) AS invalid_employee_keys
FROM fact_performance_reviews f
LEFT JOIN dim_employee d
    ON f.employee_sk = d.employee_sk
WHERE d.employee_sk IS NULL;



-- 9. Validate Department Foreign-Key Resolution
--    Expected result: 0 rows


SELECT COUNT(*) AS invalid_department_keys
FROM fact_performance_reviews f
LEFT JOIN dim_department d
    ON f.department_sk = d.department_sk
WHERE d.department_sk IS NULL;



-- 10. Validate Date Foreign-Key Resolution
--     Expected result: 0 rows


SELECT COUNT(*) AS invalid_date_keys
FROM fact_performance_reviews f
LEFT JOIN dim_date d
    ON f.date_sk = d.date_sk
WHERE d.date_sk IS NULL;



-- 11. Validate Project Foreign-Key Resolution
--     NULL project_sk is allowed.
--     Expected result: 0 rows


SELECT COUNT(*) AS invalid_project_keys
FROM fact_performance_reviews f
LEFT JOIN dim_project d
    ON f.project_sk = d.project_sk
WHERE f.project_sk IS NOT NULL
  AND d.project_sk IS NULL;



-- 12. Fact Project Assignment Summary


SELECT
    COUNT(*) AS total_reviews,
    SUM(
        CASE
            WHEN project_sk IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS reviews_with_project,
    SUM(
        CASE
            WHEN project_sk IS NULL THEN 1
            ELSE 0
        END
    ) AS reviews_without_project
FROM fact_performance_reviews;



-- 13. Unknown Employee / Department Usage


SELECT
    SUM(
        CASE
            WHEN employee_sk = 0 THEN 1
            ELSE 0
        END
    ) AS unknown_employee_facts,
    SUM(
        CASE
            WHEN department_sk = 0 THEN 1
            ELSE 0
        END
    ) AS unknown_department_facts
FROM fact_performance_reviews;



-- 14. Validate Date Dimension Coverage


SELECT
    MIN(full_date) AS minimum_date,
    MAX(full_date) AS maximum_date,
    COUNT(*) AS date_count
FROM dim_date;



-- 15. Validate Project Attribution
--     Number of fact rows with a selected project


SELECT
    COUNT(*) AS selected_project_facts,
    COUNT(DISTINCT review_id) AS distinct_reviews
FROM fact_performance_reviews
WHERE project_sk IS NOT NULL;



-- 16. Validate Current Employee Records


SELECT
    COUNT(*) AS current_employee_records
FROM dim_employee
WHERE is_current = 1
  AND employee_id <> 'UNKNOWN';



-- 17. Validate Historical Employee Records


SELECT
    COUNT(*) AS historical_employee_records
FROM dim_employee
WHERE is_current = 0;



-- 18. Final Data Quality Summary


SELECT
    (SELECT COUNT(*) FROM employees) AS employees,
    (SELECT COUNT(*) FROM projects) AS projects,
    (SELECT COUNT(*) FROM performance_reviews) AS source_reviews,
    (SELECT COUNT(*) FROM dim_employee) AS dim_employee_rows,
    (SELECT COUNT(*) FROM dim_project) AS dim_project_rows,
    (SELECT COUNT(*) FROM dim_department) AS dim_department_rows,
    (SELECT COUNT(*) FROM dim_date) AS dim_date_rows,
    (SELECT COUNT(*) FROM fact_performance_reviews) AS fact_review_rows;

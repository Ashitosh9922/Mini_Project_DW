
-- 08_etl_scd2.sql
-- Enterprise Employee Analytics & Data Warehouse System
--
-- Purpose:
--     Load performance reviews into the OLAP fact table.
--
-- Fact Grain:
--     One row per performance review.
--


USE employee_analytics_dw;


INSERT INTO fact_performance_reviews (

    review_id,
    employee_sk,
    project_sk,
    department_sk,
    date_sk,
    performance_score,
    performance_rating,
    manager_rating,
    employee_rating
)

WITH ranked_projects AS (

    SELECT

        pr.review_id,

        ep.project_id,

        ROW_NUMBER() OVER (

            PARTITION BY pr.review_id

            ORDER BY

                ep.allocation_percent DESC,

                ep.start_date DESC,

                ep.project_id ASC

        ) AS rn

    FROM performance_reviews pr

    JOIN employee_projects ep

        ON pr.employee_id = ep.employee_id

       AND pr.review_date
           BETWEEN ep.start_date
           AND ep.end_date
),


selected_projects AS (

    SELECT

        review_id,

        project_id

    FROM ranked_projects

    WHERE rn = 1
)


SELECT

    pr.review_id,


    -- SCD Type 2 employee resolution
    COALESCE(
        de.employee_sk,
        0
    ) AS employee_sk,


    -- Selected project
    dp.project_sk,


    -- Historical department resolution
    COALESCE(
        dd.department_sk,
        0
    ) AS department_sk,


    -- Date dimension
    dt.date_sk,


    -- Performance measures
    pr.performance_score,

    pr.performance_rating,

    pr.manager_rating,

    pr.employee_rating


FROM performance_reviews pr



-- SCD2 EMPLOYEE LOOKUP


LEFT JOIN dim_employee de

    ON pr.employee_id = de.employee_id

   AND pr.review_date
       BETWEEN de.effective_start_date
       AND de.effective_end_date



-- HISTORICAL DEPARTMENT LOOKUP


LEFT JOIN dim_department dd

    ON de.department_id = dd.department_id



-- PROJECT LOOKUP


LEFT JOIN selected_projects sp

    ON pr.review_id = sp.review_id


LEFT JOIN dim_project dp

    ON sp.project_id = dp.project_id



-- DATE LOOKUP


JOIN dim_date dt

    ON pr.review_date = dt.full_date;

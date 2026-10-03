
-- 07_olap_fact.sql
-- Enterprise Employee Analytics & Data Warehouse System
--
-- Purpose:
--     Create the central fact table for performance reviews.
--
-- Fact Grain:
--     One row = one performance review.
--
-- Dimensions:
--     Dim_Employee
--     Dim_Project
--     Dim_Department
--     Dim_Date
--



USE employee_analytics_dw;



-- FACT TABLE: PERFORMANCE REVIEWS


CREATE TABLE fact_performance_reviews (

    -- Fact table surrogate key
    review_fact_sk BIGINT AUTO_INCREMENT PRIMARY KEY,

    -- Degenerate/business key from OLTP review
    review_id BIGINT NOT NULL,

    -- Dimension surrogate keys
    employee_sk BIGINT NOT NULL,

    project_sk INT NULL,

    department_sk INT NOT NULL,

    date_sk INT NOT NULL,

    -- Performance measures
    performance_score DECIMAL(5,2),

    performance_rating INT,

    manager_rating INT,

    employee_rating INT,

    -- One fact row per performance review
    UNIQUE KEY uq_fact_review
        (review_id),

    -- Employee dimension
    CONSTRAINT fk_fact_employee
        FOREIGN KEY (employee_sk)
        REFERENCES dim_employee(employee_sk),

    -- Project dimension
    CONSTRAINT fk_fact_project
        FOREIGN KEY (project_sk)
        REFERENCES dim_project(project_sk),

    -- Department dimension
    CONSTRAINT fk_fact_department
        FOREIGN KEY (department_sk)
        REFERENCES dim_department(department_sk),

    -- Date dimension
    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_sk)
        REFERENCES dim_date(date_sk)
);

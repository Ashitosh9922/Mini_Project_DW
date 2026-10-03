
-- 06_olap_dimensions.sql
-- Enterprise Employee Analytics & Data Warehouse System
--
-- Purpose:
--     Create and populate the OLAP dimension tables.
--
-- Dimensions:
--     1. Dim_Department
--     2. Dim_Project
--     3. Dim_Date
--     4. Dim_Employee (SCD Type 2)
--



USE employee_analytics_dw;



-- 1. DIMENSION: DEPARTMENT


CREATE TABLE dim_department (
    department_sk INT AUTO_INCREMENT PRIMARY KEY,

    department_id INT NOT NULL,

    department_name VARCHAR(100) NOT NULL,

    UNIQUE KEY uq_dim_department_business
        (department_id)
);


-- Load Department Dimension

INSERT INTO dim_department (
    department_id,
    department_name
)
SELECT
    department_id,
    department_name
FROM departments;


-- Add Unknown Department Member
-- Surrogate key 0 is reserved for unresolved/missing values.

SET SESSION sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

INSERT INTO dim_department (
    department_sk,
    department_id,
    department_name
)
VALUES (
    0,
    0,
    'Unknown'
);



-- 2. DIMENSION: PROJECT


CREATE TABLE dim_project (
    project_sk INT AUTO_INCREMENT PRIMARY KEY,

    project_id INT NOT NULL,

    project_name VARCHAR(255) NOT NULL,

    department_id INT,

    department_name VARCHAR(100),

    start_date DATE,

    end_date DATE,

    budget DECIMAL(15,2),

    status VARCHAR(50),

    UNIQUE KEY uq_dim_project_business
        (project_id)
);


-- Load Project Dimension

INSERT INTO dim_project (
    project_id,
    project_name,
    department_id,
    department_name,
    start_date,
    end_date,
    budget,
    status
)
SELECT
    p.project_id,
    p.project_name,
    p.department_id,
    d.department_name,
    p.start_date,
    p.end_date,
    p.budget,
    p.status
FROM projects p
JOIN departments d
    ON p.department_id = d.department_id;



-- 3. DIMENSION: DATE


CREATE TABLE dim_date (
    date_sk INT PRIMARY KEY,

    full_date DATE NOT NULL,

    day_of_month INT NOT NULL,

    month_number INT NOT NULL,

    month_name VARCHAR(20) NOT NULL,

    quarter_number INT NOT NULL,

    year_number INT NOT NULL,

    day_of_week INT NOT NULL,

    day_name VARCHAR(20) NOT NULL,

    week_of_year INT NOT NULL,

    UNIQUE KEY uq_dim_date_full_date
        (full_date)
);


-- Generate dates from 2020-01-01 through 2027-12-31

SET SESSION cte_max_recursion_depth = 5000;

INSERT INTO dim_date (
    date_sk,
    full_date,
    day_of_month,
    month_number,
    month_name,
    quarter_number,
    year_number,
    day_of_week,
    day_name,
    week_of_year
)

WITH RECURSIVE date_series AS (

    SELECT DATE('2020-01-01') AS full_date

    UNION ALL

    SELECT DATE_ADD(full_date, INTERVAL 1 DAY)
    FROM date_series
    WHERE full_date < DATE('2027-12-31')
)

SELECT

    YEAR(full_date) * 10000
        + MONTH(full_date) * 100
        + DAY(full_date) AS date_sk,

    full_date,

    DAY(full_date) AS day_of_month,

    MONTH(full_date) AS month_number,

    MONTHNAME(full_date) AS month_name,

    QUARTER(full_date) AS quarter_number,

    YEAR(full_date) AS year_number,

    DAYOFWEEK(full_date) AS day_of_week,

    DAYNAME(full_date) AS day_name,

    WEEK(full_date, 3) AS week_of_year

FROM date_series;



-- 4. DIMENSION: EMPLOYEE
-- SCD TYPE 2


CREATE TABLE dim_employee (

    employee_sk BIGINT AUTO_INCREMENT PRIMARY KEY,

    employee_id VARCHAR(20) NOT NULL,

    first_name VARCHAR(100),

    last_name VARCHAR(100),

    email VARCHAR(150),

    gender VARCHAR(20),

    age INT,

    department_id INT,

    job_role VARCHAR(100),

    education_field VARCHAR(100),

    job_level INT,

    monthly_income INT,

    daily_rate INT,

    hourly_rate INT,

    business_travel VARCHAR(50),

    distance_from_home INT,

    job_involvement INT,

    job_satisfaction INT,

    environment_satisfaction INT,

    relationship_satisfaction INT,

    performance_rating INT,

    percent_salary_hike INT,

    overtime VARCHAR(10),

    marital_status VARCHAR(50),

    stock_option_level INT,

    total_working_years INT,

    years_at_company INT,

    years_in_current_role INT,

    years_since_last_promotion INT,

    years_with_current_manager INT,

    training_times_last_year INT,

    work_life_balance INT,

    num_companies_worked INT,

    attrition VARCHAR(10),

    hire_date DATE,

    effective_start_date DATE NOT NULL,

    effective_end_date DATE NOT NULL,

    is_current TINYINT NOT NULL,

    INDEX idx_dim_employee_business_key
        (employee_id),

    INDEX idx_dim_employee_current
        (employee_id, is_current),

    INDEX idx_dim_employee_dates
        (employee_id, effective_start_date)
);


-- Load Employee SCD2 Records

INSERT INTO dim_employee (

    employee_id,

    first_name,

    last_name,

    email,

    gender,

    age,

    department_id,

    job_role,

    education_field,

    job_level,

    monthly_income,

    daily_rate,

    hourly_rate,

    business_travel,

    distance_from_home,

    job_involvement,

    job_satisfaction,

    environment_satisfaction,

    relationship_satisfaction,

    performance_rating,

    percent_salary_hike,

    overtime,

    marital_status,

    stock_option_level,

    total_working_years,

    years_at_company,

    years_in_current_role,

    years_since_last_promotion,

    years_with_current_manager,

    training_times_last_year,

    work_life_balance,

    num_companies_worked,

    attrition,

    hire_date,

    effective_start_date,

    effective_end_date,

    is_current
)

SELECT

    employee_id,

    first_name,

    last_name,

    email,

    gender,

    age,

    department_id,

    job_role,

    education_field,

    job_level,

    monthly_income,

    daily_rate,

    hourly_rate,

    business_travel,

    distance_from_home,

    job_involvement,

    job_satisfaction,

    environment_satisfaction,

    relationship_satisfaction,

    performance_rating,

    percent_salary_hike,

    overtime,

    marital_status,

    stock_option_level,

    total_working_years,

    years_at_company,

    years_in_current_role,

    years_since_last_promotion,

    years_with_current_manager,

    training_times_last_year,

    work_life_balance,

    num_companies_worked,

    attrition,

    hire_date,

    effective_start_date,

    effective_end_date,

    is_current

FROM employee_history;


-- Add Unknown Employee Member
-- Surrogate key 0 is reserved for historical/unresolved employees.

SET SESSION sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

INSERT INTO dim_employee (
    employee_sk,
    employee_id,
    first_name,
    last_name,
    effective_start_date,
    effective_end_date,
    is_current
)
VALUES (
    0,
    'UNKNOWN',
    'Unknown',
    'Unknown',
    '1900-01-01',
    '9999-12-31',
    1
);

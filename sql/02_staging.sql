
-- 02_staging.sql
-- Purpose: Create staging tables for raw/generated CSV data


USE employee_analytics_dw;



-- STAGING: EMPLOYEES


CREATE TABLE IF NOT EXISTS stg_employees (
    employee_id VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    gender VARCHAR(20),
    age INT,
    department VARCHAR(100),
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
    hire_date DATE
);



-- STAGING: DEPARTMENTS


CREATE TABLE IF NOT EXISTS stg_departments (
    department_id INT,
    department_name VARCHAR(100)
);



-- STAGING: PROJECTS


CREATE TABLE IF NOT EXISTS stg_projects (
    project_id INT,
    project_name VARCHAR(255),
    department_id INT,
    department_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    status VARCHAR(50)
);



-- STAGING: EMPLOYEE PROJECT ASSIGNMENTS


CREATE TABLE IF NOT EXISTS stg_employee_projects (
    assignment_id INT,
    employee_id VARCHAR(20),
    project_id INT,
    allocation_percent INT,
    start_date DATE,
    end_date DATE
);



-- STAGING: EMPLOYEE HISTORY


CREATE TABLE IF NOT EXISTS stg_employee_history (
    employee_id VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    gender VARCHAR(20),
    age INT,
    department VARCHAR(100),
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
    effective_start_date DATE,
    effective_end_date DATE,
    is_current TINYINT
);



-- STAGING: PERFORMANCE REVIEWS


CREATE TABLE IF NOT EXISTS stg_performance_reviews (
    review_id BIGINT,
    employee_id VARCHAR(20),
    review_date DATE,
    review_period VARCHAR(20),
    performance_score DECIMAL(5,2),
    performance_rating INT,
    manager_rating INT,
    employee_rating INT,
    comments VARCHAR(500)
);

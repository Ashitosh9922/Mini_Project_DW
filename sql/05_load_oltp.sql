
-- 05_load_oltp.sql
-- Purpose: Populate normalized OLTP tables from staging



INSERT INTO departments (
    department_id,
    department_name
)
SELECT
    department_id,
    department_name
FROM stg_departments;

SELECT COUNT(*) AS departments_loaded
FROM departments;


SELECT *
FROM departments;


    
INSERT INTO employees (
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
    hire_date
)
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    e.email,
    e.gender,
    e.age,
    d.department_id,
    e.job_role,
    e.education_field,
    e.job_level,
    e.monthly_income,
    e.daily_rate,
    e.hourly_rate,
    e.business_travel,
    e.distance_from_home,
    e.job_involvement,
    e.job_satisfaction,
    e.environment_satisfaction,
    e.relationship_satisfaction,
    e.performance_rating,
    e.percent_salary_hike,
    e.overtime,
    e.marital_status,
    e.stock_option_level,
    e.total_working_years,
    e.years_at_company,
    e.years_in_current_role,
    e.years_since_last_promotion,
    e.years_with_current_manager,
    e.training_times_last_year,
    e.work_life_balance,
    e.num_companies_worked,
    e.attrition,
    e.hire_date
FROM stg_employees e
JOIN departments d
    ON e.department = d.department_name;

SELECT COUNT(*) AS employees_loaded
FROM employees;

INSERT INTO projects (
    project_id,
    project_name,
    department_id,
    start_date,
    end_date,
    budget,
    status
)
SELECT
    project_id,
    project_name,
    department_id,
    start_date,
    end_date,
    budget,
    status
FROM stg_projects;

SELECT COUNT(*) AS projects_loaded
FROM projects;


INSERT INTO employee_history (
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
    h.employee_id,
    h.first_name,
    h.last_name,
    h.email,
    h.gender,
    h.age,
    d.department_id,
    h.job_role,
    h.education_field,
    h.job_level,
    h.monthly_income,
    h.daily_rate,
    h.hourly_rate,
    h.business_travel,
    h.distance_from_home,
    h.job_involvement,
    h.job_satisfaction,
    h.environment_satisfaction,
    h.relationship_satisfaction,
    h.performance_rating,
    h.percent_salary_hike,
    h.overtime,
    h.marital_status,
    h.stock_option_level,
    h.total_working_years,
    h.years_at_company,
    h.years_in_current_role,
    h.years_since_last_promotion,
    h.years_with_current_manager,
    h.training_times_last_year,
    h.work_life_balance,
    h.num_companies_worked,
    h.attrition,
    h.hire_date,
    h.effective_start_date,
    h.effective_end_date,
    h.is_current
FROM stg_employee_history h
JOIN departments d
    ON h.department = d.department_name;

SELECT COUNT(*) AS employee_history_loaded
FROM employee_history;

INSERT INTO employee_projects (
    assignment_id,
    employee_id,
    project_id,
    allocation_percent,
    start_date,
    end_date
)
SELECT
    assignment_id,
    employee_id,
    project_id,
    allocation_percent,
    start_date,
    end_date
FROM stg_employee_projects;

SELECT COUNT(*) AS employee_projects_loaded
FROM employee_projects;

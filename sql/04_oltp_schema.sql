-- =========================================================
-- OLTP TABLE 1: DEPARTMENTS
-- =========================================================

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


-- =========================================================
-- OLTP TABLE 2: EMPLOYEES
-- Current employee information
-- =========================================================

CREATE TABLE employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
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

    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- =========================================================
-- OLTP TABLE 3: EMPLOYEE HISTORY
-- Historical employee records / SCD-related operational data
-- =========================================================

CREATE TABLE employee_history (
    history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
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

    CONSTRAINT fk_history_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT fk_history_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- =========================================================
-- OLTP TABLE 4: PROJECTS
-- =========================================================

CREATE TABLE projects (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    status VARCHAR(50),

    CONSTRAINT fk_project_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);


-- =========================================================
-- OLTP TABLE 5: EMPLOYEE-PROJECT ASSIGNMENTS
-- =========================================================

CREATE TABLE employee_projects (
    assignment_id INT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    project_id INT NOT NULL,
    allocation_percent INT,
    start_date DATE,
    end_date DATE,

    CONSTRAINT fk_assignment_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    CONSTRAINT fk_assignment_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id)
);



CREATE TABLE performance_reviews (
    review_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(20) NOT NULL,
    review_date DATE NOT NULL,
    review_period VARCHAR(20),
    performance_score DECIMAL(5,2),
    performance_rating INT,
    manager_rating INT,
    employee_rating INT,
    comments VARCHAR(500),

    CONSTRAINT fk_review_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);


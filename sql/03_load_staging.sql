
-- 03_load_staging.sql
-- Purpose: Load generated CSV files into staging tables


USE employee_analytics_dw;



-- LOAD EMPLOYEES


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/employees_100k.csv'
INTO TABLE stg_employees
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- LOAD DEPARTMENTS


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/departments.csv'
INTO TABLE stg_departments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- LOAD PROJECTS


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/projects.csv'
INTO TABLE stg_projects
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- LOAD EMPLOYEE PROJECT ASSIGNMENTS


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/employee_projects.csv'
INTO TABLE stg_employee_projects
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- LOAD EMPLOYEE HISTORY


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/employee_history.csv'
INTO TABLE stg_employee_history
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



-- LOAD PERFORMANCE REVIEWS


LOAD DATA INFILE
'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/performance_reviews.csv'
INTO TABLE stg_performance_reviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

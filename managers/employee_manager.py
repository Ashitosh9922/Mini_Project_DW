from db.db_manager import DatabaseConnection


class EmployeeManager:
    """
    Manager class for employee-related database operations.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    # ------------------------------------------------------------------
    # EMPLOYEE CREATION
    # ------------------------------------------------------------------

    def add_employee(self, employee):
        """Add a complete employee using the stored procedure."""

        query = """
            CALL sp_add_employee(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        params = (
            employee.employee_id,
            employee.first_name,
            employee.last_name,
            employee.email,
            employee.gender,
            employee.age,
            employee.department_id,
            employee.job_role,
            employee.education_field,
            employee.job_level,
            employee.monthly_income,
            employee.daily_rate,
            employee.hourly_rate,
            employee.business_travel,
            employee.distance_from_home,
            employee.job_involvement,
            employee.job_satisfaction,
            employee.environment_satisfaction,
            employee.relationship_satisfaction,
            employee.performance_rating,
            employee.percent_salary_hike,
            employee.overtime,
            employee.marital_status,
            employee.stock_option_level,
            employee.total_working_years,
            employee.years_at_company,
            employee.years_in_current_role,
            employee.years_since_last_promotion,
            employee.years_with_current_manager,
            employee.training_times_last_year,
            employee.work_life_balance,
            employee.num_companies_worked,
            employee.attrition,
            employee.hire_date,
        )

        return self.db.execute(query, params)

    # ------------------------------------------------------------------
    # EMPLOYEE READ
    # ------------------------------------------------------------------

    def get_employee(self, employee_id):
        """Fetch one employee by employee ID."""

        query = """
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                gender,
                age,
                department_id,
                job_role,
                monthly_income,
                hire_date,
                attrition
            FROM employees
            WHERE employee_id = %s
        """

        result = self.db.fetch(query, (employee_id,))

        return result[0] if result else None

    def get_employees(self, limit=100):
        """Fetch employees with a configurable display limit."""

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 100

        limit = max(1, min(limit, 1000))

        query = f"""
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                department_id,
                job_role,
                monthly_income,
                hire_date,
                attrition
            FROM employees
            ORDER BY employee_id
            LIMIT {limit}
        """

        return self.db.fetch(query)

    def search_employees(self, search_term):
        """Search employees by ID, name, email, or job role."""

        query = """
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                department_id,
                job_role,
                monthly_income,
                hire_date,
                attrition
            FROM employees
            WHERE
                employee_id LIKE %s
                OR first_name LIKE %s
                OR last_name LIKE %s
                OR email LIKE %s
                OR job_role LIKE %s
            ORDER BY employee_id
            LIMIT 100
        """

        pattern = f"%{search_term}%"

        params = (
            pattern,
            pattern,
            pattern,
            pattern,
            pattern,
        )

        return self.db.fetch(query, params)

    # ------------------------------------------------------------------
    # DEPARTMENT / SCD2
    # ------------------------------------------------------------------

    def update_department(
        self,
        employee_id,
        department_id,
        change_date
    ):
        """
        Update employee department using the SCD2-aware procedure.
        """

        query = """
            CALL sp_update_employee_department(
                %s,
                %s,
                %s
            )
        """

        params = (
            employee_id,
            department_id,
            change_date,
        )

        return self.db.execute(query, params)

    def get_employee_history(self, employee_id):
        """Return OLTP employee history records."""

        query = """
            SELECT
                history_id,
                employee_id,
                department_id,
                job_role,
                monthly_income,
                effective_start_date,
                effective_end_date,
                is_current
            FROM employee_history
            WHERE employee_id = %s
            ORDER BY effective_start_date
        """

        return self.db.fetch(query, (employee_id,))

    # ------------------------------------------------------------------
    # DEPARTMENTS
    # ------------------------------------------------------------------

    def get_departments(self):
        """Return all departments."""

        query = """
            SELECT
                department_id,
                department_name
            FROM departments
            ORDER BY department_name
        """

        return self.db.fetch(query)
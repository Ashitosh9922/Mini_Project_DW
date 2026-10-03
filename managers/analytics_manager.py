from db.db_manager import DatabaseConnection


class AnalyticsManager:
    """
    Manager class responsible for OLAP and dashboard analytics.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    # ------------------------------------------------------------------
    # PERFORMANCE
    # ------------------------------------------------------------------

    def get_average_performance_by_year(self):
        """Return average performance score by year."""

        query = """
            SELECT
                d.year_number AS year,
                ROUND(AVG(f.performance_score), 2) AS average_score,
                COUNT(*) AS review_count
            FROM fact_performance_reviews f
            JOIN dim_date d
                ON f.date_sk = d.date_sk
            GROUP BY d.year_number
            ORDER BY d.year_number
        """

        return self.db.fetch(query)

    def get_monthly_performance(self):
        """Return monthly average performance."""

        query = """
            SELECT
                d.year_number AS year,
                d.month_number AS month,
                d.month_name AS month_name,
                ROUND(AVG(f.performance_score), 2) AS average_score,
                COUNT(*) AS review_count
            FROM fact_performance_reviews f
            JOIN dim_date d
                ON f.date_sk = d.date_sk
            GROUP BY
                d.year_number,
                d.month_number,
                d.month_name
            ORDER BY
                d.year_number,
                d.month_number
        """

        return self.db.fetch(query)

    def get_department_performance(self):
        """Return average performance by department."""

        query = """
            SELECT
                d.department_name,
                ROUND(AVG(f.performance_score), 2) AS average_score,
                COUNT(*) AS review_count
            FROM fact_performance_reviews f
            JOIN dim_department d
                ON f.department_sk = d.department_sk
            GROUP BY
                d.department_sk,
                d.department_name
            ORDER BY average_score DESC
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # EMPLOYEE ANALYTICS
    # ------------------------------------------------------------------

    def get_employee_rankings(self):
        """
        Return employee performance rankings.

        Uses a CTE and DENSE_RANK window function.
        """

        query = """
            WITH employee_scores AS (
                SELECT
                    e.employee_id,
                    e.first_name,
                    e.last_name,
                    ROUND(
                        AVG(f.performance_score),
                        2
                    ) AS average_score,
                    COUNT(*) AS review_count
                FROM fact_performance_reviews f
                JOIN dim_employee e
                    ON f.employee_sk = e.employee_sk
                WHERE e.is_current = 1
                GROUP BY
                    e.employee_id,
                    e.first_name,
                    e.last_name
            )

            SELECT
                employee_id,
                first_name,
                last_name,
                average_score,
                review_count,

                DENSE_RANK() OVER (
                    ORDER BY average_score DESC
                ) AS ranking

            FROM employee_scores

            ORDER BY ranking, employee_id

            LIMIT 100
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # PROJECT ANALYTICS
    # ------------------------------------------------------------------

    def get_project_workload(self):
        """Return employee workload by project."""

        query = """
            SELECT
                p.project_id,
                p.project_name,
                p.status,
                COUNT(a.assignment_id) AS employee_count,
                COALESCE(
                    ROUND(AVG(a.allocation_percent), 2),
                    0
                ) AS average_allocation
            FROM projects p
            LEFT JOIN employee_projects a
                ON p.project_id = a.project_id
            GROUP BY
                p.project_id,
                p.project_name,
                p.status
            ORDER BY employee_count DESC
        """

        return self.db.fetch(query)

    def get_active_project_workload(self):
        """Return currently active employee-project assignments."""

        query = """
            SELECT
                p.project_id,
                p.project_name,
                COUNT(a.assignment_id) AS employee_count,
                ROUND(
                    AVG(a.allocation_percent),
                    2
                ) AS average_allocation
            FROM projects p
            LEFT JOIN employee_projects a
                ON p.project_id = a.project_id
            WHERE
                a.start_date <= CURDATE()
                AND (
                    a.end_date IS NULL
                    OR a.end_date >= CURDATE()
                )
            GROUP BY
                p.project_id,
                p.project_name
            ORDER BY employee_count DESC
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # ATTRITION
    # ------------------------------------------------------------------

    def get_attrition_analysis(self):
        """Return employee attrition distribution."""

        query = """
            SELECT
                attrition,
                COUNT(*) AS employee_count,
                ROUND(
                    COUNT(*) * 100.0 /
                    SUM(COUNT(*)) OVER (),
                    2
                ) AS percentage
            FROM employees
            GROUP BY attrition
            ORDER BY employee_count DESC
        """

        return self.db.fetch(query)

    def get_attrition_by_department(self):
        """Return attrition distribution by department."""

        query = """
            SELECT
                d.department_name,
                e.attrition,
                COUNT(*) AS employee_count
            FROM employees e
            JOIN departments d
                ON e.department_id = d.department_id
            GROUP BY
                d.department_name,
                e.attrition
            ORDER BY
                d.department_name,
                e.attrition
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # HEADCOUNT
    # ------------------------------------------------------------------

    def get_employee_headcount_by_department(self):
        """Return employee headcount by department."""

        query = """
            SELECT
                d.department_name,
                COUNT(e.employee_id) AS employee_count
            FROM departments d
            LEFT JOIN employees e
                ON d.department_id = e.department_id
            GROUP BY
                d.department_id,
                d.department_name
            ORDER BY employee_count DESC
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # SALARY
    # ------------------------------------------------------------------

    def get_salary_by_department(self):
        """Return salary statistics by department."""

        query = """
            SELECT
                d.department_name,
                ROUND(AVG(e.monthly_income), 2) AS average_salary,
                MIN(e.monthly_income) AS minimum_salary,
                MAX(e.monthly_income) AS maximum_salary
            FROM employees e
            JOIN departments d
                ON e.department_id = d.department_id
            GROUP BY
                d.department_id,
                d.department_name
            ORDER BY average_salary DESC
        """

        return self.db.fetch(query)

    # ------------------------------------------------------------------
    # SCD2
    # ------------------------------------------------------------------

    def get_scd2_employee_history(self, employee_id):
        """Return complete SCD Type 2 history for an employee."""

        query = """
            SELECT
                employee_sk,
                employee_id,
                first_name,
                last_name,
                department_id,
                job_role,
                monthly_income,
                effective_start_date,
                effective_end_date,
                is_current
            FROM dim_employee
            WHERE employee_id = %s
            ORDER BY effective_start_date
        """

        return self.db.fetch(query, (employee_id,))
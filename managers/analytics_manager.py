from db.db_manager import DatabaseConnection


class AnalyticsManager:
    """Manager class for OLAP analytics."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_average_performance_by_year(self):
        """Return average performance score by year."""

        query = """
            SELECT
                d.year_number AS year,
                ROUND(AVG(f.performance_score), 2) AS average_score
            FROM fact_performance_reviews f
            JOIN dim_date d
                ON f.date_sk = d.date_sk
            GROUP BY d.year_number
            ORDER BY d.year_number
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

    def get_employee_rankings(self):
        """
        Rank employees by performance within each department
        using CTE + DENSE_RANK().
        """

        query = """
            WITH employee_scores AS (
                SELECT
                    e.employee_id,
                    e.first_name,
                    e.last_name,
                    d.department_name,
                    ROUND(
                        AVG(f.performance_score), 2
                    ) AS average_score
                FROM fact_performance_reviews f
                JOIN dim_employee e
                    ON f.employee_sk = e.employee_sk
                JOIN dim_department d
                    ON f.department_sk = d.department_sk
                WHERE e.is_current = 1
                  AND e.employee_id <> 'UNKNOWN'
                GROUP BY
                    e.employee_id,
                    e.first_name,
                    e.last_name,
                    d.department_name
            )
            SELECT
                employee_id,
                first_name,
                last_name,
                department_name,
                average_score,
                DENSE_RANK() OVER (
                    PARTITION BY department_name
                    ORDER BY average_score DESC
                ) AS ranking
            FROM employee_scores
            ORDER BY
                department_name,
                ranking
        """

        return self.db.fetch(query)

    def get_project_workload(self):
        """Return project assignment workload."""

        query = """
            SELECT
                p.project_id,
                p.project_name,
                COUNT(a.assignment_id) AS employee_count
            FROM projects p
            LEFT JOIN employee_projects a
                ON p.project_id = a.project_id
            GROUP BY
                p.project_id,
                p.project_name
            ORDER BY employee_count DESC
        """

        return self.db.fetch(query)

    def get_year_over_year_performance(self):
        """
        Return yearly performance and year-over-year change
        using CTE + LAG().
        """

        query = """
            WITH yearly_performance AS (
                SELECT
                    d.year_number,
                    AVG(f.performance_score) AS average_score
                FROM fact_performance_reviews f
                JOIN dim_date d
                    ON f.date_sk = d.date_sk
                GROUP BY d.year_number
            ),
            performance_with_previous_year AS (
                SELECT
                    year_number,
                    average_score,
                    LAG(average_score) OVER (
                        ORDER BY year_number
                    ) AS previous_year_score
                FROM yearly_performance
            )
            SELECT
                year_number,
                ROUND(average_score, 2) AS average_score,
                ROUND(previous_year_score, 2)
                    AS previous_year_score,
                ROUND(
                    average_score - previous_year_score,
                    2
                ) AS score_change
            FROM performance_with_previous_year
            ORDER BY year_number
        """

        return self.db.fetch(query)

    def get_employee_360(self, employee_id):
        """Return employee profile information."""

        query = """
            SELECT
                e.employee_id,
                e.first_name,
                e.last_name,
                e.email,
                e.job_role,
                e.department_id,
                d.department_name,
                e.age,
                e.job_level,
                e.monthly_income,
                e.hire_date,
                e.attrition
            FROM employees e
            LEFT JOIN departments d
                ON e.department_id = d.department_id
            WHERE e.employee_id = %s
            LIMIT 1
        """

        return self.db.fetch(query, (employee_id,))

    def get_employee_performance_summary(self, employee_id):
        """Return performance summary for one employee."""

        query = """
            SELECT
                COUNT(*) AS review_count,
                ROUND(AVG(performance_score), 2) AS average_score,
                MAX(performance_score) AS best_score,
                MIN(performance_score) AS lowest_score
            FROM performance_reviews
            WHERE employee_id = %s
        """

        return self.db.fetch(query, (employee_id,))

    def get_employee_performance_trend(self, employee_id):
        """Return year-wise performance from the OLAP warehouse."""

        query = """
            SELECT
                d.year_number AS year,
                ROUND(AVG(f.performance_score), 2)
                    AS average_score
            FROM fact_performance_reviews f
            JOIN dim_employee e
                ON f.employee_sk = e.employee_sk
            JOIN dim_date d
                ON f.date_sk = d.date_sk
            WHERE e.employee_id = %s
            GROUP BY d.year_number
            ORDER BY d.year_number
        """

        return self.db.fetch(query, (employee_id,))

    def get_employee_projects(self, employee_id):
        """Return projects assigned to an employee."""

        query = """
            SELECT
                p.project_name,
                ep.allocation_percent,
                ep.start_date,
                ep.end_date,
                p.status
            FROM employee_projects ep
            JOIN projects p
                ON ep.project_id = p.project_id
            WHERE ep.employee_id = %s
            ORDER BY ep.start_date DESC
        """

        return self.db.fetch(query, (employee_id,))

    def get_employee_department_history(self, employee_id):
        """Return SCD Type 2 department history."""

        query = """
            SELECT
                d.department_name,
                e.effective_start_date,
                e.effective_end_date,
                e.is_current
            FROM dim_employee e
            JOIN dim_department d
                ON e.department_id = d.department_id
            WHERE e.employee_id = %s
            ORDER BY e.effective_start_date
        """

        return self.db.fetch(query, (employee_id,))
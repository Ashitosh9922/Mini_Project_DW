from db.db_manager import DatabaseConnection


class ProjectManager:
    """Manager class for project and assignment operations."""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_project(self, project):
        """Create a project using the stored procedure."""

        query = """
            CALL sp_add_project(
                %s, %s, %s, %s, %s, %s, %s
            )
        """

        params = (
            project.project_id,
            project.project_name,
            project.department_id,
            project.start_date,
            project.end_date,
            project.budget,
            project.status
        )

        return self.db.execute(query, params)

    def assign_employee(
        self,
        employee_id,
        project_id,
        allocation_percent,
        start_date,
        end_date
    ):
        """Assign an employee using the stored procedure."""

        query = """
            CALL sp_assign_employee_to_project(
                %s, %s, %s, %s, %s
            )
        """

        params = (
            employee_id,
            project_id,
            allocation_percent,
            start_date,
            end_date
        )

        return self.db.execute(query, params)

    def get_projects(self):
        """Return available projects."""

        query = """
            SELECT
                p.project_id,
                p.project_name,
                d.department_name,
                p.start_date,
                p.end_date,
                p.budget,
                p.status
            FROM projects p
            JOIN departments d
                ON p.department_id = d.department_id
            ORDER BY p.project_id
        """

        return self.db.fetch(query)
class Project:
    """
    Entity class representing a project.
    """

    def __init__(
        self,
        project_id,
        project_name,
        department_id=None,
        start_date=None,
        end_date=None,
        budget=None,
        status=None,
    ):
        self.project_id = project_id
        self.project_name = project_name
        self.department_id = department_id
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.status = status

    def get_data(self):
        """Return project attributes as a dictionary."""

        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "department_id": self.department_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "status": self.status,
        }

    def __repr__(self):
        return (
            f"Project("
            f"project_id={self.project_id}, "
            f"project_name='{self.project_name}', "
            f"department_id={self.department_id}, "
            f"status='{self.status}'"
            f")"
        )
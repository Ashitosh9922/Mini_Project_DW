from db.db_manager import DatabaseConnection


class ReviewManager:
    """Manager class for performance review operations."""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_review(self, review):
        """Add a performance review using the stored procedure."""

        query = """
            CALL sp_add_performance_review(
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        params = (
            review.employee_id,
            review.review_date,
            review.review_period,
            review.performance_score,
            review.performance_rating,
            review.manager_rating,
            review.employee_rating,
            review.comments
        )

        return self.db.execute(query, params)

    def get_employee_reviews(self, employee_id):
        """Return reviews for an employee."""

        query = """
            SELECT
                review_id,
                review_date,
                review_period,
                performance_score,
                performance_rating,
                manager_rating,
                employee_rating,
                comments
            FROM performance_reviews
            WHERE employee_id = %s
            ORDER BY review_date DESC
        """

        return self.db.fetch(query, (employee_id,))
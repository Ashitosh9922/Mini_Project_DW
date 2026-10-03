class Review:
    """
    Entity class representing a performance review.
    """

    def __init__(
        self,
        review_id=None,
        employee_id=None,
        review_date=None,
        review_period=None,
        performance_score=None,
        performance_rating=None,
        manager_rating=None,
        employee_rating=None,
        comments=None,
    ):
        self.review_id = review_id
        self.employee_id = employee_id
        self.review_date = review_date
        self.review_period = review_period
        self.performance_score = performance_score
        self.performance_rating = performance_rating
        self.manager_rating = manager_rating
        self.employee_rating = employee_rating
        self.comments = comments

    def get_data(self):
        """Return review attributes as a dictionary."""

        return {
            "review_id": self.review_id,
            "employee_id": self.employee_id,
            "review_date": self.review_date,
            "review_period": self.review_period,
            "performance_score": self.performance_score,
            "performance_rating": self.performance_rating,
            "manager_rating": self.manager_rating,
            "employee_rating": self.employee_rating,
            "comments": self.comments,
        }

    def __repr__(self):
        return (
            f"Review("
            f"review_id={self.review_id}, "
            f"employee_id='{self.employee_id}', "
            f"review_date={self.review_date}, "
            f"performance_score={self.performance_score}"
            f")"
        )
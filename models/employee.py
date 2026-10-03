class Employee:
    """Entity class representing an employee."""

    def __init__(
        self,
        employee_id,
        first_name,
        last_name,
        email,
        gender=None,
        age=None,
        department_id=None,
        job_role=None,
        education_field=None,
        job_level=None,
        monthly_income=None,
        daily_rate=None,
        hourly_rate=None,
        business_travel=None,
        distance_from_home=None,
        job_involvement=None,
        job_satisfaction=None,
        environment_satisfaction=None,
        relationship_satisfaction=None,
        performance_rating=None,
        percent_salary_hike=None,
        overtime=None,
        marital_status=None,
        stock_option_level=None,
        total_working_years=None,
        years_at_company=None,
        years_in_current_role=None,
        years_since_last_promotion=None,
        years_with_current_manager=None,
        training_times_last_year=None,
        work_life_balance=None,
        num_companies_worked=None,
        attrition=None,
        hire_date=None
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age
        self.department_id = department_id
        self.job_role = job_role
        self.education_field = education_field
        self.job_level = job_level
        self.monthly_income = monthly_income
        self.daily_rate = daily_rate
        self.hourly_rate = hourly_rate
        self.business_travel = business_travel
        self.distance_from_home = distance_from_home
        self.job_involvement = job_involvement
        self.job_satisfaction = job_satisfaction
        self.environment_satisfaction = environment_satisfaction
        self.relationship_satisfaction = relationship_satisfaction
        self.performance_rating = performance_rating
        self.percent_salary_hike = percent_salary_hike
        self.overtime = overtime
        self.marital_status = marital_status
        self.stock_option_level = stock_option_level
        self.total_working_years = total_working_years
        self.years_at_company = years_at_company
        self.years_in_current_role = years_in_current_role
        self.years_since_last_promotion = years_since_last_promotion
        self.years_with_current_manager = years_with_current_manager
        self.training_times_last_year = training_times_last_year
        self.work_life_balance = work_life_balance
        self.num_companies_worked = num_companies_worked
        self.attrition = attrition
        self.hire_date = hire_date

    def get_full_name(self):
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_data(self):
        """Return employee data as a dictionary."""
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": self.gender,
            "age": self.age,
            "department_id": self.department_id,
            "job_role": self.job_role,
            "education_field": self.education_field,
            "job_level": self.job_level,
            "monthly_income": self.monthly_income,
            "daily_rate": self.daily_rate,
            "hourly_rate": self.hourly_rate,
            "business_travel": self.business_travel,
            "distance_from_home": self.distance_from_home,
            "job_involvement": self.job_involvement,
            "job_satisfaction": self.job_satisfaction,
            "environment_satisfaction": self.environment_satisfaction,
            "relationship_satisfaction": self.relationship_satisfaction,
            "performance_rating": self.performance_rating,
            "percent_salary_hike": self.percent_salary_hike,
            "overtime": self.overtime,
            "marital_status": self.marital_status,
            "stock_option_level": self.stock_option_level,
            "total_working_years": self.total_working_years,
            "years_at_company": self.years_at_company,
            "years_in_current_role": self.years_in_current_role,
            "years_since_last_promotion": self.years_since_last_promotion,
            "years_with_current_manager": self.years_with_current_manager,
            "training_times_last_year": self.training_times_last_year,
            "work_life_balance": self.work_life_balance,
            "num_companies_worked": self.num_companies_worked,
            "attrition": self.attrition,
            "hire_date": self.hire_date
        }
from models.employee import Employee
from models.project import Project
from models.review import Review


print("===== EMPLOYEE TEST =====")

employee = Employee(
    employee_id="E000001",
    first_name="Test",
    last_name="Employee",
    email="test.employee@example.com",
    department_id=1,
    job_role="Developer",
    monthly_income=5000,
    hire_date="2024-01-15"
)

print("Full Name:", employee.get_full_name())
print("Employee Data:", employee.get_data())


print("\n===== PROJECT TEST =====")

project = Project(
    project_id=1,
    project_name="Test Project",
    department_id=1,
    start_date="2024-01-01",
    end_date="2024-12-31",
    budget=100000,
    status="Active"
)

print("Project Data:", project.get_data())


print("\n===== REVIEW TEST =====")

review = Review(
    review_id=1,
    employee_id="E000001",
    review_date="2024-12-31",
    review_period="2024",
    performance_score=85.50,
    performance_rating=4,
    manager_rating=4,
    employee_rating=5,
    comments="Good performance"
)

print("Review Data:", review.get_data())


print("\n===== PHASE 3 ENTITY TEST COMPLETE =====")
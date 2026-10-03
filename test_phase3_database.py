from managers.employee_manager import EmployeeManager
from managers.analytics_manager import AnalyticsManager
from models.employee import Employee


print("===== EMPLOYEE MANAGER TEST =====")

manager = EmployeeManager()

result = manager.get_employee("E000001")

if result:
    print("Employee found:")
    print(result)
else:
    print("Employee not found.")


print("\n===== EMPLOYEE LIST TEST =====")

result = manager.get_employees()

print("Number of employees returned:", len(result))

if result:
    print("First employee:")
    print(result[0])


print("\n===== ANALYTICS: YEARLY PERFORMANCE =====")

analytics = AnalyticsManager()

result = analytics.get_average_performance_by_year()

for item in result:
    print(item)


print("\n===== ANALYTICS: DEPARTMENT PERFORMANCE =====")

result = analytics.get_department_performance()

for item in result:
    print(item)


print("\n===== ANALYTICS: EMPLOYEE RANKINGS =====")

result = analytics.get_employee_rankings()

for item in result[:10]:
    print(item)


print("\n===== ANALYTICS: PROJECT WORKLOAD =====")

result = analytics.get_project_workload()

for item in result[:10]:
    print(item)


print("\n===== EMPLOYEE ADD TEST =====")

employee = Employee(
    employee_id="TEST001",
    first_name="Test",
    last_name="User",
    email="test001@example.com",
    gender="Male",
    age=30,
    department_id=1,
    job_role="Developer",
    education_field="Computer Science",
    job_level=2,
    monthly_income=5000,
    daily_rate=800,
    hourly_rate=100,
    business_travel="Travel_Rarely",
    distance_from_home=10,
    job_involvement=3,
    job_satisfaction=3,
    environment_satisfaction=3,
    relationship_satisfaction=3,
    performance_rating=3,
    percent_salary_hike=12,
    overtime="No",
    marital_status="Single",
    stock_option_level=0,
    total_working_years=5,
    years_at_company=2,
    years_in_current_role=1,
    years_since_last_promotion=1,
    years_with_current_manager=1,
    training_times_last_year=3,
    work_life_balance=3,
    num_companies_worked=1,
    attrition="No",
    hire_date="2025-01-01"
)

result = manager.add_employee(employee)

print("Employee insert result:", result)


print("\n===== EMPLOYEE DEPARTMENT UPDATE TEST =====")

result = manager.update_department(
    "TEST001",
    2,
    "2025-06-01"
)
print("Department update result:", result)


print("\n===== TEST001 VERIFICATION =====")

result = manager.get_employee("TEST001")

if result:
    print("TEST001 found:")
    print(result)
else:
    print("TEST001 not found.")


print("\n===== PHASE 3 DATABASE TEST COMPLETE =====")
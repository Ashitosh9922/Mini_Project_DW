import streamlit as st

from models.employee import Employee
from managers.employee_manager import EmployeeManager


st.set_page_config(
    page_title="Employee Onboarding",
    page_icon="👤",
    layout="wide"
)


@st.cache_resource
def get_manager():
    return EmployeeManager()


manager = get_manager()


st.title("👤 Employee Onboarding")

st.write(
    "Add a new employee to the OLTP employee database."
)


with st.form("employee_form"):

    col1, col2 = st.columns(2)

    with col1:

        employee_id = st.text_input(
            "Employee ID"
        )

        first_name = st.text_input(
            "First Name"
        )

        last_name = st.text_input(
            "Last Name"
        )

        email = st.text_input(
            "Email"
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        age = st.number_input(
            "Age",
            18,
            70,
            30
        )

        departments = manager.db.fetch("""
            SELECT department_id, department_name
            FROM departments
            ORDER BY department_name
        """)

        department_options = {
            row["department_name"]: row["department_id"]
            for row in departments
        }

        selected_department = st.selectbox(
            "Department",
            list(department_options.keys())
        )

        department_id = department_options[selected_department]

        job_role = st.text_input(
            "Job Role"
        )

        education_field = st.text_input(
            "Education Field"
        )

        job_level = st.number_input(
            "Job Level",
            1,
            5,
            1
        )

    with col2:

        monthly_income = st.number_input(
            "Monthly Income",
            0,
            100000,
            5000
        )

        daily_rate = st.number_input(
            "Daily Rate",
            0,
            10000,
            500
        )

        hourly_rate = st.number_input(
            "Hourly Rate",
            0,
            1000,
            50
        )

        business_travel = st.selectbox(
            "Business Travel",
            [
                "Travel_Rarely",
                "Travel_Frequently",
                "Non-Travel"
            ]
        )

        distance_from_home = st.number_input(
            "Distance From Home",
            0,
            100,
            10
        )

        overtime = st.selectbox(
            "Overtime",
            ["Yes", "No"]
        )

        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Divorced"]
        )

        attrition = st.selectbox(
            "Attrition",
            ["No", "Yes"]
        )

        hire_date = st.date_input(
            "Hire Date"
        )

    st.subheader("Employee Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        job_involvement = st.number_input(
            "Job Involvement",
            1,
            4,
            3
        )

        job_satisfaction = st.number_input(
            "Job Satisfaction",
            1,
            4,
            3
        )

        environment_satisfaction = st.number_input(
            "Environment Satisfaction",
            1,
            4,
            3
        )

    with col2:

        relationship_satisfaction = st.number_input(
            "Relationship Satisfaction",
            1,
            4,
            3
        )

        performance_rating = st.number_input(
            "Performance Rating",
            1,
            5,
            3
        )

        percent_salary_hike = st.number_input(
            "Percent Salary Hike",
            0,
            100,
            10
        )

    with col3:

        stock_option_level = st.number_input(
            "Stock Option Level",
            0,
            3,
            0
        )

        total_working_years = st.number_input(
            "Total Working Years",
            0,
            50,
            5
        )

        years_at_company = st.number_input(
            "Years At Company",
            0,
            50,
            2
        )

    with col4:

        years_in_current_role = st.number_input(
            "Years In Current Role",
            0,
            50,
            1
        )

        years_since_last_promotion = st.number_input(
            "Years Since Last Promotion",
            0,
            50,
            1
        )

        years_with_current_manager = st.number_input(
            "Years With Current Manager",
            0,
            50,
            1
        )

    training_times_last_year = st.number_input(
        "Training Times Last Year",
        0,
        20,
        3
    )

    work_life_balance = st.number_input(
        "Work Life Balance",
        1,
        4,
        3
    )

    num_companies_worked = st.number_input(
        "Number Of Companies Worked",
        0,
        20,
        1
    )

    submitted = st.form_submit_button(
        "Add Employee"
    )


if submitted:

    if not employee_id or not first_name or not last_name or not email:

        st.error(
            "Employee ID, first name, last name and email are required."
        )

    else:

        employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            age=age,
            department_id=department_id,
            job_role=job_role,
            education_field=education_field,
            job_level=job_level,
            monthly_income=monthly_income,
            daily_rate=daily_rate,
            hourly_rate=hourly_rate,
            business_travel=business_travel,
            distance_from_home=distance_from_home,
            job_involvement=job_involvement,
            job_satisfaction=job_satisfaction,
            environment_satisfaction=environment_satisfaction,
            relationship_satisfaction=relationship_satisfaction,
            performance_rating=performance_rating,
            percent_salary_hike=percent_salary_hike,
            overtime=overtime,
            marital_status=marital_status,
            stock_option_level=stock_option_level,
            total_working_years=total_working_years,
            years_at_company=years_at_company,
            years_in_current_role=years_in_current_role,
            years_since_last_promotion=years_since_last_promotion,
            years_with_current_manager=years_with_current_manager,
            training_times_last_year=training_times_last_year,
            work_life_balance=work_life_balance,
            num_companies_worked=num_companies_worked,
            attrition=attrition,
            hire_date=hire_date
        )

        result = manager.add_employee(employee)

        if result:

            st.success(
                f"Employee {employee_id} added successfully."
            )

        else:

            st.error(
                "Employee could not be added."
            )
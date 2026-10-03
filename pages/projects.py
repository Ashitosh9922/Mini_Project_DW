import streamlit as st
import pandas as pd
from datetime import date

from db.db_manager import DatabaseConnection


st.set_page_config(
    page_title="Project Assignment",
    page_icon="📁",
    layout="wide"
)


@st.cache_resource
def get_db():
    return DatabaseConnection()


db = get_db()


st.title("📁 Project Assignment")

st.write(
    "Assign an employee to a project and manage project allocation."
)

st.divider()


# LOAD EMPLOYEES

employees = db.fetch(
    """
    SELECT
        employee_id,
        first_name,
        last_name,
        department_id,
        job_role
    FROM employees
    ORDER BY employee_id
    """
)


# LOAD PROJECTS

projects = db.fetch(
    """
    SELECT
        project_id,
        project_name,
        department_id,
        start_date,
        end_date,
        budget,
        status
    FROM projects
    ORDER BY project_id
    """
)


if not employees:
    st.error("No employees found.")
    st.stop()

if not projects:
    st.error("No projects found.")
    st.stop()


employee_options = {
    f"{row['employee_id']} - {row['first_name']} {row['last_name']}": row["employee_id"]
    for row in employees
}

project_options = {
    f"{row['project_id']} - {row['project_name']}": row["project_id"]
    for row in projects
}


# ASSIGNMENT FORM

st.subheader("➕ Assign Employee to Project")


with st.form("project_assignment_form"):

    employee_name = st.selectbox(
        "Employee",
        list(employee_options.keys())
    )

    project_name = st.selectbox(
        "Project",
        list(project_options.keys())
    )

    allocation_percent = st.slider(
        "Allocation Percentage",
        min_value=10,
        max_value=100,
        value=100,
        step=10
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Assignment Start Date"
        )

    with col2:
        end_date = st.date_input(
            "Assignment End Date"
        )

    submitted = st.form_submit_button(
        "Assign Employee"
    )


if submitted:

    employee_id = employee_options[employee_name]
    project_id = project_options[project_name]

    if end_date < start_date:
        st.error(
            "Assignment end date cannot be before the start date."
        )

    else:

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

        result = db.execute(query, params)

        if result:
            st.success(
                f"Employee {employee_id} assigned successfully "
                f"to project {project_id}."
            )

            st.cache_resource.clear()

        else:
            st.error(
                "Unable to assign employee. "
                "Check the database error message."
            )


st.divider()


# CREATE PROJECT


st.subheader("Create New Project")

with st.form("create_project_form"):

    col1, col2 = st.columns(2)

    with col1:
        project_id = st.number_input(
            "Project ID",
            min_value=1,
            step=1
        )

        project_name = st.text_input(
            "Project Name"
        )

        department_options = {
            row["department_name"]: row["department_id"]
            for row in db.fetch("""
                SELECT department_id, department_name
                FROM departments
                ORDER BY department_name
            """)
        }

        selected_department = st.selectbox(
            "Department",
            options=list(department_options.keys())
        )

        start_date = st.date_input(
            "Start Date",
            value=date.today()
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            value=date.today()
        )

        budget = st.number_input(
            "Budget",
            min_value=0.0,
            step=1000.0,
            format="%.2f"
        )

        status = st.selectbox(
            "Status",
            [
                "Planned",
                "Active",
                "Completed",
                "On Hold"
            ]
        )

    submitted = st.form_submit_button(
        "Create Project"
    )

    if submitted:

        if not project_name.strip():
            st.error("Project name is required.")

        elif end_date < start_date:
            st.error("End date cannot be before start date.")

        elif not selected_department:
            st.error("Please select a department.")

        else:

            selected_department_id = department_options[
                selected_department
            ]

            query = """
                CALL sp_add_project(
                    %s, %s, %s, %s, %s, %s, %s
                )
            """

            success = db.execute(
                query,
                (
                    int(project_id),
                    project_name.strip(),
                    selected_department_id,
                    start_date,
                    end_date,
                    budget,
                    status
                )
            )

            if success:
                st.success(
                    f"Project '{project_name}' created successfully."
                )

                st.cache_resource.clear()
                st.rerun()

            else:
                st.error(
                    "Unable to create project. "
                    "Check whether the Project ID already exists."
                )

# CURRENT ASSIGNMENTS

st.subheader("📋 Current Project Assignments")


assignments = db.fetch(
    """
    SELECT
        ep.assignment_id,
        ep.employee_id,
        CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
        ep.project_id,
        p.project_name,
        ep.allocation_percent,
        ep.start_date,
        ep.end_date
    FROM employee_projects ep
    JOIN employees e
        ON ep.employee_id = e.employee_id
    JOIN projects p
        ON ep.project_id = p.project_id
    ORDER BY ep.assignment_id DESC
    LIMIT 200
    """
)


if assignments:

    assignment_df = pd.DataFrame(assignments)

    st.dataframe(
        assignment_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No project assignments found.")


st.divider()


# PROJECT SUMMARY

st.subheader("📊 Project Allocation Summary")


summary = db.fetch(
    """
    SELECT
        p.project_id,
        p.project_name,
        COUNT(ep.assignment_id) AS employee_count,
        COALESCE(SUM(ep.allocation_percent), 0) AS total_allocation
    FROM projects p
    LEFT JOIN employee_projects ep
        ON p.project_id = ep.project_id
    GROUP BY
        p.project_id,
        p.project_name
    ORDER BY employee_count DESC
    LIMIT 20
    """
)


if summary:

    summary_df = pd.DataFrame(summary)

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(
            summary_df.set_index("project_name")[
                "employee_count"
            ]
        )

    with col2:
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )



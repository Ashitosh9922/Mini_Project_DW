import streamlit as st
import pandas as pd
from datetime import date

from models.project import Project
from managers.project_manager import ProjectManager


st.set_page_config(
    page_title="Project Assignment",
    page_icon="📁",
    layout="wide"
)


@st.cache_resource
def get_manager():
    return ProjectManager()


manager = get_manager()


# PAGE HEADER

st.title("📁 Project Management")

st.write(
    "Create projects, assign employees, and monitor project allocation."
)

st.divider()


# LOAD EMPLOYEES

employees = manager.db.fetch(
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


# LOAD DEPARTMENTS

departments = manager.db.fetch(
    """
    SELECT
        department_id,
        department_name
    FROM departments
    ORDER BY department_name
    """
)


# SUCCESS / ERROR MESSAGES

if "project_success_message" in st.session_state:

    st.success(
        st.session_state["project_success_message"]
    )

    del st.session_state["project_success_message"]


if "assignment_success_message" in st.session_state:

    st.success(
        st.session_state["assignment_success_message"]
    )

    del st.session_state["assignment_success_message"]


# CREATE PROJECT

st.subheader("➕ Create New Project")


if not departments:

    st.warning(
        "No departments are available. "
        "A project cannot be created until at least one department exists."
    )

else:

    department_options = {
        row["department_name"]: row["department_id"]
        for row in departments
    }

    with st.form("create_project_form"):

        col1, col2 = st.columns(2)

        with col1:

            project_id = st.number_input(
                "Project ID",
                min_value=1,
                step=1,
                value=1
            )

            project_name = st.text_input(
                "Project Name",
                placeholder="Enter project name"
            )

            selected_department = st.selectbox(
                "Department",
                options=list(department_options.keys())
            )

            project_start_date = st.date_input(
                "Project Start Date",
                value=date.today()
            )

        with col2:

            project_end_date = st.date_input(
                "Project End Date",
                value=date.today()
            )

            budget = st.number_input(
                "Budget",
                min_value=0.0,
                step=1000.0,
                value=0.0,
                format="%.2f"
            )

            status = st.selectbox(
                "Project Status",
                [
                    "Planned",
                    "Active",
                    "Completed",
                    "On Hold"
                ]
            )

        create_project_submitted = st.form_submit_button(
            "Create Project"
        )


    # -----------------------------------------------------
    # CREATE PROJECT ACTION
    # -----------------------------------------------------

    if create_project_submitted:

        if not project_name.strip():

            st.error(
                "Project name is required."
            )

        elif project_end_date < project_start_date:

            st.error(
                "Project end date cannot be before project start date."
            )

        else:

            selected_department_id = department_options[
                selected_department
            ]

            # Check whether Project ID already exists.

            existing_project = manager.db.fetch(
                """
                SELECT project_id
                FROM projects
                WHERE project_id = %s
                """,
                (int(project_id),)
            )

            if existing_project:

                st.error(
                    f"Project ID {int(project_id)} already exists. "
                    "Please use a different Project ID."
                )

            else:

                project = Project(
                    project_id=int(project_id),
                    project_name=project_name.strip(),
                    department_id=selected_department_id,
                    start_date=project_start_date,
                    end_date=project_end_date,
                    budget=budget,
                    status=status
                )

                success = manager.add_project(project)

                if success:

                    # Store message before rerun.
                    st.session_state[
                        "project_success_message"
                    ] = (
                        f"Project '{project_name.strip()}' "
                        f"created successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to create project. "
                        "Please check the database error message."
                    )


st.divider()


# ASSIGN EMPLOYEE TO PROJECT

st.subheader("➕ Assign Employee to Project")


# Reload projects so newly created projects appear.

projects = manager.get_projects()


if not employees:

    st.error(
        "No employees found. Please onboard an employee first."
    )

elif not projects:

    st.error(
        "No projects found. Please create a project first."
    )

else:

    employee_options = {
        f"{row['employee_id']} - "
        f"{row['first_name']} {row['last_name']}":
        row["employee_id"]
        for row in employees
    }

    project_options = {
        f"{row['project_id']} - {row['project_name']}":
        row["project_id"]
        for row in projects
    }

    with st.form("project_assignment_form"):

        employee_name = st.selectbox(
            "Employee",
            list(employee_options.keys())
        )

        project_name_selection = st.selectbox(
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

            assignment_start_date = st.date_input(
                "Assignment Start Date",
                value=date.today()
            )

        with col2:

            assignment_end_date = st.date_input(
                "Assignment End Date",
                value=date.today()
            )

        assign_submitted = st.form_submit_button(
            "Assign Employee"
        )


    # -----------------------------------------------------
    # ASSIGNMENT ACTION
    # -----------------------------------------------------

    if assign_submitted:

        employee_id = employee_options[
            employee_name
        ]

        project_id = project_options[
            project_name_selection
        ]

        if assignment_end_date < assignment_start_date:

            st.error(
                "Assignment end date cannot be before "
                "assignment start date."
            )

        else:

            success = manager.assign_employee(
                employee_id=employee_id,
                project_id=project_id,
                allocation_percent=allocation_percent,
                start_date=assignment_start_date,
                end_date=assignment_end_date
            )

            if success:

                st.session_state[
                    "assignment_success_message"
                ] = (
                    f"Employee {employee_id} assigned successfully "
                    f"to project {project_id}."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to assign employee. "
                    "Please check the database error message."
                )


st.divider()


# CURRENT PROJECT ASSIGNMENTS

st.subheader("📋 Current Project Assignments")


assignments = manager.db.fetch(
    """
    SELECT
        ep.assignment_id,
        ep.employee_id,
        CONCAT(
            e.first_name,
            ' ',
            e.last_name
        ) AS employee_name,
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

    st.info(
        "No project assignments found."
    )


st.divider()


# PROJECT ALLOCATION SUMMARY

st.subheader("📊 Project Allocation Summary")

st.write(
    "Overview of employee assignments and total allocation "
    "across projects."
)


summary = manager.db.fetch(
    """
    SELECT
        p.project_id,
        p.project_name,
        COUNT(ep.assignment_id) AS employee_count,
        COALESCE(
            SUM(ep.allocation_percent),
            0
        ) AS total_allocation
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

    col1, col2 = st.columns(
        [2, 1],
        gap="large"
    )

    with col1:

        st.bar_chart(
            summary_df.set_index(
                "project_name"
            )["employee_count"]
        )

    with col2:

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info(
        "No project allocation data available."
    )
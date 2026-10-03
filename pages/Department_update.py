import streamlit as st
import pandas as pd

from db.db_manager import DatabaseConnection


st.set_page_config(
    page_title="Department Update",
    page_icon="🔄",
    layout="wide"
)


@st.cache_resource
def get_db():
    return DatabaseConnection()


db = get_db()


st.title("🔄 Department Update & SCD Type 2")

st.write(
    "Update an employee's department while preserving "
    "the employee's historical department records."
)

st.divider()


# ---------------------------------------------------------
# LOAD EMPLOYEES
# ---------------------------------------------------------

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

departments = db.fetch(
    """
    SELECT
        department_id,
        department_name
    FROM departments
    ORDER BY department_id
    """
)


if not employees:
    st.error("No employees found.")
    st.stop()

if not departments:
    st.error("No departments found.")
    st.stop()


# ---------------------------------------------------------
# EMPLOYEE SELECTION
# ---------------------------------------------------------

employee_options = {
    f"{row['employee_id']} - "
    f"{row['first_name']} {row['last_name']}":
        row
    for row in employees
}

department_options = {
    f"{row['department_id']} - {row['department_name']}":
        row["department_id"]
    for row in departments
}


st.subheader("👤 Select Employee")


selected_employee_name = st.selectbox(
    "Employee",
    list(employee_options.keys())
)

selected_employee = employee_options[
    selected_employee_name
]

employee_id = selected_employee["employee_id"]

current_department_id = selected_employee[
    "department_id"
]


# ---------------------------------------------------------
# CURRENT DEPARTMENT
# ---------------------------------------------------------

current_department = db.fetch(
    """
    SELECT department_name
    FROM departments
    WHERE department_id = %s
    """,
    (current_department_id,)
)


if current_department:
    st.info(
        f"Current Department: "
        f"{current_department[0]['department_name']}"
    )


st.divider()


# ---------------------------------------------------------
# DEPARTMENT UPDATE
# ---------------------------------------------------------

st.subheader("🏢 Change Department")


with st.form("department_update_form"):

    new_department_name = st.selectbox(
        "New Department",
        list(department_options.keys())
    )

    change_date = st.date_input(
        "Effective Change Date"
    )

    submitted = st.form_submit_button(
        "Update Department"
    )


if submitted:

    new_department_id = department_options[
        new_department_name
    ]

    if new_department_id == current_department_id:

        st.warning(
            "The selected department is already "
            "the employee's current department."
        )

    else:

        query = """
            CALL sp_update_employee_department(
                %s, %s, %s
            )
        """

        params = (
            employee_id,
            new_department_id,
            change_date
        )

        result = db.execute(query, params)

        if result:

            st.success(
                f"Department updated successfully "
                f"for employee {employee_id}."
            )

            st.info(
                "The previous employee version should "
                "remain available as historical data."
            )

            st.cache_resource.clear()

        else:

            st.error(
                "Unable to update department."
            )


st.divider()


# ---------------------------------------------------------
# OLTP HISTORY
# ---------------------------------------------------------

st.subheader("📜 Employee History")


history = db.fetch(
    """
    SELECT
        history_id,
        employee_id,
        department_id,
        effective_start_date,
        effective_end_date,
        is_current
    FROM employee_history
    WHERE employee_id = %s
    ORDER BY effective_start_date
    """,
    (employee_id,)
)


if history:

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No employee history records found."
    )


st.divider()


# ---------------------------------------------------------
# OLAP SCD TYPE 2 HISTORY
# ---------------------------------------------------------

st.subheader("⭐ OLAP Employee SCD Type 2 History")


dimension_history = db.fetch(
    """
    SELECT
        employee_sk,
        employee_id,
        first_name,
        last_name,
        department_id,
        effective_start_date,
        effective_end_date,
        is_current
    FROM dim_employee
    WHERE employee_id = %s
    ORDER BY effective_start_date
    """,
    (employee_id,)
)


if dimension_history:

    dimension_df = pd.DataFrame(
        dimension_history
    )

    st.dataframe(
        dimension_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No SCD Type 2 dimension record found "
        "for this employee."
    )
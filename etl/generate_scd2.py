import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_FILE = Path(
    "data/generated/employees_100k.csv"
)

OUTPUT_DIR = Path(
    "data/generated"
)

OUTPUT_FILE = (
    OUTPUT_DIR / "employee_history.csv"
)

SEED = 42

# Percentage of employees who will receive
# historical changes
HISTORICAL_PERCENTAGE = 0.20

# Date used as the end date for the current record
CURRENT_END_DATE = pd.Timestamp("9999-12-31")


np.random.seed(SEED)


# --------------------------------------------------
# LOAD EMPLOYEE DATA
# --------------------------------------------------

def load_employees():

    print("Loading employee dataset...")

    df = pd.read_csv(
        INPUT_FILE,
        parse_dates=["hire_date"]
    )

    print(
        f"Employees loaded: {len(df):,}"
    )

    return df


# --------------------------------------------------
# GENERATE DEPARTMENTS
# --------------------------------------------------

def get_departments():

    return [
        "Sales",
        "Research & Development",
        "Human Resources"
    ]


# --------------------------------------------------
# SELECT HISTORICAL EMPLOYEES
# --------------------------------------------------

def select_historical_employees(df):

    number_of_employees = int(
        len(df) * HISTORICAL_PERCENTAGE
    )

    historical_ids = np.random.choice(
        df["employee_id"],
        size=number_of_employees,
        replace=False
    )

    print(
        f"Employees selected for historical changes: "
        f"{number_of_employees:,}"
    )

    return set(historical_ids)


# --------------------------------------------------
# CREATE HISTORICAL RECORDS
# --------------------------------------------------

def generate_history(df, historical_ids):

    print("\nGenerating SCD Type 2 history...")

    records = []

    departments = get_departments()

    for _, employee in df.iterrows():

        employee_id = employee["employee_id"]

        # --------------------------------------------------
        # EMPLOYEES WITHOUT HISTORY
        # --------------------------------------------------

        if employee_id not in historical_ids:

            record = employee.to_dict()

            record["effective_start_date"] = (
                employee["hire_date"]
            )

            record["effective_end_date"] = (
                CURRENT_END_DATE
            )

            record["is_current"] = 1

            records.append(record)

            continue

        # --------------------------------------------------
        # HISTORICAL EMPLOYEE
        # --------------------------------------------------

        hire_date = pd.Timestamp(
            employee["hire_date"]
        )

        # We need at least some time between
        # hire date and the historical change.
        days_since_hire = (
            pd.Timestamp("2025-01-01")
            - hire_date
        ).days

        if days_since_hire < 365:

            # If employee was hired too recently,
            # don't create an artificial history.
            record = employee.to_dict()

            record["effective_start_date"] = hire_date
            record["effective_end_date"] = (
                CURRENT_END_DATE
            )
            record["is_current"] = 1

            records.append(record)

            continue

        # --------------------------------------------------
        # CHANGE DATE
        # --------------------------------------------------

        max_days = max(
            365,
            days_since_hire
        )

        change_days = np.random.randint(
            180,
            max_days
        )

        change_date = (
            hire_date
            + pd.Timedelta(
                days=int(change_days)
            )
        )

        # Make sure change date isn't in the future
        if change_date >= pd.Timestamp("2025-01-01"):

            change_date = (
                pd.Timestamp("2025-01-01")
                - pd.Timedelta(days=30)
            )

        # --------------------------------------------------
        # OLD VERSION
        # --------------------------------------------------

        old_record = employee.to_dict()

        old_record["effective_start_date"] = (
            hire_date
        )

        old_record["effective_end_date"] = (
            change_date - pd.Timedelta(days=1)
        )

        old_record["is_current"] = 0

        records.append(old_record)

        # --------------------------------------------------
        # NEW VERSION
        # --------------------------------------------------

        new_record = employee.to_dict()

        new_record["effective_start_date"] = (
            change_date
        )

        new_record["effective_end_date"] = (
            CURRENT_END_DATE
        )

        new_record["is_current"] = 1

        # --------------------------------------------------
        # CHOOSE TYPE OF CHANGE
        # --------------------------------------------------

        change_type = np.random.choice(
            [
                "department_change",
                "promotion",
                "salary_increase"
            ]
        )

        # --------------------------------------------------
        # DEPARTMENT CHANGE
        # --------------------------------------------------

        if change_type == "department_change":

            current_department = (
                employee["department"]
            )

            available_departments = [
                d
                for d in departments
                if d != current_department
            ]

            new_department = np.random.choice(
                available_departments
            )

            new_record["department"] = (
                new_department
            )

            print(
                f"{employee_id}: "
                f"Department change "
                f"{current_department} -> "
                f"{new_department}"
            )

        # --------------------------------------------------
        # PROMOTION
        # --------------------------------------------------

        elif change_type == "promotion":

            old_job_level = int(
                employee["job_level"]
            )

            new_job_level = min(
                old_job_level + 1,
                5
            )

            new_record["job_level"] = (
                new_job_level
            )

            # Increase salary after promotion
            old_salary = int(
                employee["monthly_income"]
            )

            new_salary = int(
                old_salary *
                np.random.uniform(
                    1.10,
                    1.25
                )
            )

            new_record["monthly_income"] = (
                new_salary
            )

            print(
                f"{employee_id}: "
                f"Promotion "
                f"Level {old_job_level} -> "
                f"Level {new_job_level}"
            )

        # --------------------------------------------------
        # SALARY INCREASE
        # --------------------------------------------------

        elif change_type == "salary_increase":

            old_salary = int(
                employee["monthly_income"]
            )

            increase_percentage = (
                np.random.uniform(
                    1.05,
                    1.20
                )
            )

            new_salary = int(
                old_salary *
                increase_percentage
            )

            new_record["monthly_income"] = (
                new_salary
            )

            print(
                f"{employee_id}: "
                f"Salary increase "
                f"{old_salary} -> "
                f"{new_salary}"
            )

        records.append(new_record)

    history_df = pd.DataFrame(records)

    return history_df


# --------------------------------------------------
# SORT DATA
# --------------------------------------------------

def sort_history(df):

    df = df.sort_values(
        [
            "employee_id",
            "effective_start_date"
        ]
    ).reset_index(drop=True)

    return df


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

def save_history(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n================================")
    print("SCD TYPE 2 GENERATION COMPLETE")
    print("================================")

    print(
        f"Output file: {OUTPUT_FILE}"
    )

    print(
        f"Total SCD records: {len(df):,}"
    )

    print(
        f"Unique employees: "
        f"{df['employee_id'].nunique():,}"
    )

    print(
        f"Current records: "
        f"{(df['is_current'] == 1).sum():,}"
    )

    print(
        f"Historical records: "
        f"{(df['is_current'] == 0).sum():,}"
    )


# --------------------------------------------------
# VALIDATION
# --------------------------------------------------

def validate_scd2(df):

    print("\nRunning SCD Type 2 validation...")

    # --------------------------------------------------
    # CHECK 1
    # Exactly one current record per employee
    # --------------------------------------------------

    current_counts = (
        df[df["is_current"] == 1]
        .groupby("employee_id")
        .size()
    )

    invalid_current = (
        current_counts[current_counts != 1]
    )

    if len(invalid_current) == 0:

        print(
            "✓ Exactly one current record "
            "per employee"
        )

    else:

        print(
            "✗ Current-record validation failed"
        )

    # --------------------------------------------------
    # CHECK 2
    # Historical records have is_current = 0
    # --------------------------------------------------

    historical_records = df[
        df["is_current"] == 0
    ]

    if (
        historical_records[
            "effective_end_date"
        ]
        < historical_records[
            "effective_start_date"
        ]
    ).all():

        print(
            "✓ Historical date ranges are valid"
        )

    else:

        print(
            "✗ Invalid historical date ranges"
        )

    # --------------------------------------------------
    # CHECK 3
    # Current records end in 9999-12-31
    # --------------------------------------------------

    current_records = df[
        df["is_current"] == 1
    ]

    if (
        current_records[
            "effective_end_date"
        ]
        == CURRENT_END_DATE
    ).all():

        print(
            "✓ Current records have "
            "9999-12-31 end date"
        )

    else:

        print(
            "✗ Current end-date validation failed"
        )

    # --------------------------------------------------
    # CHECK 4
    # Historical records actually exist
    # --------------------------------------------------

    if len(historical_records) > 0:

        print(
            "✓ Historical records exist"
        )

    else:

        print(
            "✗ No historical records generated"
        )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\nValidation complete.")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    employees_df = load_employees()

    historical_ids = (
        select_historical_employees(
            employees_df
        )
    )

    history_df = generate_history(
        employees_df,
        historical_ids
    )

    history_df = sort_history(
        history_df
    )

    validate_scd2(
        history_df
    )

    save_history(
        history_df
    )


if __name__ == "__main__":
    main()
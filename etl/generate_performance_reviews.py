import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
NUM_REVIEWS = 300_000
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
fake = Faker()
Faker.seed(RANDOM_SEED)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

EMPLOYEE_FILE = BASE_DIR / "data" / "generated" / "employees_100k.csv"
OUTPUT_FILE = BASE_DIR / "data" / "generated" / "performance_reviews.csv"

# -----------------------------
# Load employees
# -----------------------------
employees = pd.read_csv(EMPLOYEE_FILE)

employee_ids = employees["employee_id"].values

print(f"Employees available: {len(employee_ids):,}")

# -----------------------------
# Generate employee IDs
# -----------------------------
review_employee_ids = np.random.choice(
    employee_ids,
    size=NUM_REVIEWS,
    replace=True
)

# -----------------------------
# Generate review dates
# -----------------------------
start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2025-12-31")

date_range_days = (end_date - start_date).days

review_dates = (
    start_date
    + pd.to_timedelta(
        np.random.randint(
            0,
            date_range_days + 1,
            size=NUM_REVIEWS
        ),
        unit="D"
    )
)

# -----------------------------
# Review periods
# -----------------------------
review_periods = np.random.choice(
    ["Annual", "Mid-Year", "Quarterly"],
    size=NUM_REVIEWS,
    p=[0.50, 0.30, 0.20]
)

# -----------------------------
# Performance scores
# -----------------------------
performance_scores = np.round(
    np.random.normal(
        loc=75,
        scale=12,
        size=NUM_REVIEWS
    ).clip(40, 100),
    2
)

# -----------------------------
# Ratings
# -----------------------------
performance_ratings = np.clip(
    np.round(performance_scores / 20),
    1,
    5
).astype(int)

manager_ratings = np.clip(
    performance_ratings + np.random.choice(
        [-1, 0, 0, 0, 1],
        size=NUM_REVIEWS
    ),
    1,
    5
).astype(int)

employee_ratings = np.clip(
    performance_ratings + np.random.choice(
        [-1, 0, 0, 0, 1],
        size=NUM_REVIEWS
    ),
    1,
    5
).astype(int)

# -----------------------------
# Comments
# -----------------------------
comments = np.random.choice(
    [
        "Meets expectations",
        "Exceeds expectations",
        "Strong performance",
        "Needs improvement",
        "Outstanding contribution",
        "Consistent performance",
        "Good progress",
        "Excellent teamwork",
        "Requires additional development",
        "Demonstrates strong technical skills"
    ],
    size=NUM_REVIEWS
)

# -----------------------------
# Build DataFrame
# -----------------------------
reviews = pd.DataFrame({
    "employee_id": review_employee_ids,
    "review_date": review_dates,
    "review_period": review_periods,
    "performance_score": performance_scores,
    "performance_rating": performance_ratings,
    "manager_rating": manager_ratings,
    "employee_rating": employee_ratings,
    "comments": comments
})

# -----------------------------
# Sort records
# -----------------------------
reviews = reviews.sort_values(
    ["employee_id", "review_date"]
).reset_index(drop=True)

# -----------------------------
# Add review ID
# -----------------------------
reviews.insert(
    0,
    "review_id",
    np.arange(1, len(reviews) + 1)
)

# -----------------------------
# Save
# -----------------------------
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

reviews.to_csv(
    OUTPUT_FILE,
    index=False
)

# -----------------------------
# Validation
# -----------------------------
print("\nPerformance review generation complete.")
print(f"Rows generated: {len(reviews):,}")
print(f"Columns: {len(reviews.columns)}")
print(f"Output: {OUTPUT_FILE}")

print("\nSample:")
print(reviews.head())

print("\nReview period distribution:")
print(reviews["review_period"].value_counts())

print("\nPerformance rating distribution:")
print(reviews["performance_rating"].value_counts().sort_index())

print("\nUnique employees reviewed:")
print(reviews["employee_id"].nunique())
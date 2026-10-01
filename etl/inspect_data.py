import pandas as pd

FILE_PATH = "data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv"

df = pd.read_csv(FILE_PATH)

print("\n===== SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
for column in df.columns:
    print(column)

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== UNIQUE VALUES =====")
for column in df.columns:
    print(f"\n{column}:")
    print(df[column].unique()[:20])

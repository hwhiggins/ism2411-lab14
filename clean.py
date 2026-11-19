import pandas as pd

# Self Assessment Questions:
#
#
#

print("--- Exercise 1 ---")

df = pd.read_csv("data/messy_sales.csv")

print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("--- Exercise 2 ---")

df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns.tolist())

print("--- Exercise 3 ---")

print("Shape before dropping rows:", df.shape)
df = df.dropna(subset=["order_id", "order_date"])

print("Shape after dropping rows:", df.shape)
df["unit_price"] = pd.to_numeric(
    df["unit_price"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False),
    errors="coerce"
)
df["quantity_sold"] = pd.to_numeric(
    df["quantity_sold"]
    .astype("string")
    .str.replace(",", "", regex=False),
    errors="coerce"
)
numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].mean())

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("--- Exercise 4 ---")

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

print("Number of dates that became NaT:", df["order_date"].isna().sum())
df["unit_price"] = (
    df["unit_price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)
df["quantity_sold"] = df["quantity_sold"].astype(int)
df["revenue"] = (
    df["unit_price"] * df["quantity_sold"]
).round(2)

print("\nUpdated data types:")
print(df.dtypes)
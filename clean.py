import pandas as pd

# Self Assessment Questions:
# 1. 
# Filling missing values feels most ambiguous because using
# the mean assumes that the missing value is similar to the
# other values. Before doing this with real business data, I
# would want to know why the information is missing and whether
# the average is a reasonable estimate.
# 2. 
# Yes. I included comments explaining why I dropped rows with
# missing order IDs or dates, why I filled numeric missing
# values with the mean, and why I removed the 9,999 quantity.
# These comments explain the reasoning behind the decisions.
# 3.
# The most important thing I noticed was how high the maximum quantity
# sold was compared to the other orders. I did not expect to find a 
# quantity of 9,999, which turned out to be a placeholder and not a real
# sale. This showed me how important it is to look at the statistics and 
# check for unusual values before using data for a business decision. I 
# also learned that negative revenue is not always an error because it can 
# represent customer returns.

print("--- Exercise 1 ---")

df = pd.read_csv("data/messy_sales.csv")

print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

# Data quality issues to look for:
# 1. Some columns have missing values.
# 2. Order dates may have inconsistent formats or invalid text.
# 3. Unit prices may contain dollar signs and commas.
# 4. Some columns may have object data types instead of numeric types.

print("--- Exercise 2 ---")

df.columns = df.columns.str.lower().str.replace(" ", "_")
print(df.columns.tolist())

print("--- Exercise 3 ---")

print("Shape before dropping rows:", df.shape)

# Order IDs and order dates are essential for identifying
# and understanding a sale. Rows missing either are dropped
# instead of guessing what their information should be.
df = df.dropna(subset=["order_id", "order_date"])

print("Shape after dropping rows:", df.shape)

# Clean the numeric-looking columns so their means can
# be calculated even though the original data contains symbols.
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

# Fill missing numeric values with the column mean.
# This keeps the rows instead of deleting potentially useful
# sales records. The mean is used because the assignment
# specifically asks for mean imputation.
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

print("--- Exercise 5 ---")

print("Number of duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)

print("--- Exercise 6 ---")

# 1. A quantity_sold maximum of 9,999 is a placeholder,
#    not a realistic sales quantity. These rows are removed.
#
# 2. Negative revenue can appear unusual, but it represents
#    returns where money was given back to customers.
#    These values are legitimate and should be kept.
# Look at the describe() results for another statistic that
# stands out, such as a high maximum unit price or a large
# difference between the mean and median.

# Remove rows with a quantity of 9,999 because this is a
# known placeholder rather than a real customer order.

print(df.describe())
df = df[df["quantity_sold"] != 9999]

print("\nShape after removing placeholder quantities:")
print(df.shape)

print("--- Exercise 7 ---")

df.to_csv("data/clean_sales.csv", index=False)
print("Cleaned CSV file saved successfully!")
df_check = pd.read_csv("data/clean_sales.csv")

print("\nReloaded data without parse_dates:")
print(df_check.info())
df_check = pd.read_csv(
    "data/clean_sales.csv",
    parse_dates=["order_date"]
)

print("\nReloaded data with parse_dates:")
print(df_check.info())
print("\nFinal cleaned data shape:")
print(df_check.shape)
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
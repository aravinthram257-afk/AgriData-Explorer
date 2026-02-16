import pandas as pd
df = pd.read_csv("data/raw/icrisat_agri_data.csv")
df.dropna(inplace=True)
df.columns = df.columns.str.lower().str.replace(" ", "_")
df.to_csv("data/cleaned/cleaned_agri_data.csv", index=False)
print("✅ Data cleaning completed and saved.")

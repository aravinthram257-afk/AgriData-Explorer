import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("data/cleaned/cleaned_agri_data.csv")
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[numeric_cols] = df[numeric_cols].replace(-1, pd.NA)
pd.set_option('future.no_silent_downcasting', True)
print("✅ All -1 values replaced with NaN")
rice_state = (
    df.groupby("state_name", dropna=True)["rice_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(7)
)
plt.figure(figsize=(9,5))
rice_state.plot(kind="bar")
plt.title("Top 7 Rice Producing States in India")
plt.xlabel("State")
plt.ylabel("Production (1000 tons)")
plt.tight_layout()
plt.show()
wheat_state = (
    df.groupby("state_name")["wheat_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
# Bar
plt.figure(figsize=(8,5))
wheat_state.plot(kind="bar")
plt.title("Top 5 Wheat Producing States")
plt.ylabel("Production (1000 tons)")
plt.tight_layout()
plt.show()
# Pie
plt.figure(figsize=(6,6))
wheat_state.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Wheat Production Share (%)")
plt.ylabel("")
plt.show()
oilseed_state = (
    df.groupby("state_name")["oilseeds_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
plt.figure(figsize=(8,5))
oilseed_state.plot(kind="bar")
plt.title("Top Oilseed Producing States")
plt.ylabel("Production (1000 tons)")
plt.tight_layout()
plt.show()
sugarcane_year = (
    df.groupby("year")["sugarcane_production_(1000_tons)"]
    .sum()
)
plt.figure(figsize=(10,5))
plt.plot(sugarcane_year.index, sugarcane_year.values, marker="o")
plt.title("Sugarcane Production Trend in India")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.grid(True)
plt.tight_layout()
plt.show()
rice_year = df.groupby("year")["rice_production_(1000_tons)"].sum()
wheat_year = df.groupby("year")["wheat_production_(1000_tons)"].sum()
plt.figure(figsize=(10,5))
plt.plot(rice_year.index, rice_year, label="Rice")
plt.plot(wheat_year.index, wheat_year, label="Wheat")
plt.title("Rice vs Wheat Production Trend")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
df["total_millet_production"] = (
    df["pearl_millet_production_(1000_tons)"] +
    df["finger_millet_production_(1000_tons)"]
)
millet_year = (
    df.groupby("year")["total_millet_production"]
    .sum()
)
millet_year = millet_year[millet_year > 0]
plt.figure(figsize=(9,5))
plt.plot(millet_year.index, millet_year, marker="o", linewidth=2)
plt.title("Millet Production Trend in India")
plt.xlabel("Year")
plt.ylabel("Production (1000 tons)")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.figure(figsize=(9,6))
scatter_df = df[[
    "rice_area_(1000_ha)", "rice_production_(1000_tons)",
    "wheat_area_(1000_ha)", "wheat_production_(1000_tons)",
    "maize_area_(1000_ha)", "maize_production_(1000_tons)"
]].dropna()
plt.figure(figsize=(9,6))
plt.scatter(
    scatter_df["rice_area_(1000_ha)"],
    scatter_df["rice_production_(1000_tons)"],
    alpha=0.5,
    label="Rice"
)
plt.scatter(
    scatter_df["wheat_area_(1000_ha)"],
    scatter_df["wheat_production_(1000_tons)"],
    alpha=0.5,
    label="Wheat"
)
plt.scatter(
    scatter_df["maize_area_(1000_ha)"],
    scatter_df["maize_production_(1000_tons)"],
    alpha=0.5,
    label="Maize"
)
plt.title("Area vs Production Relationship")
plt.xlabel("Area (1000 ha)")
plt.ylabel("Production (1000 tons)")
plt.legend()
plt.tight_layout()
plt.show()
top_states = yield_state = (
    df.groupby("state_name")[[
        "rice_yield_(kg_per_ha)",
        "wheat_yield_(kg_per_ha)"
    ]]
    .mean()
    .dropna()
)
yield_state.sort_values(
    by="rice_yield_(kg_per_ha)",
    ascending=False
).head(10)
plt.figure(figsize=(12,6))
top_states.plot(kind="bar")
plt.title("Top 10 States: Rice vs Wheat Yield")
plt.xlabel("State")
plt.ylabel("Yield (Kg per ha)")
plt.xticks(rotation=40)
plt.tight_layout()
plt.show()
df.to_csv("data/cleaned/agri_final_dataset.csv", index=False)
print("✅ Final dataset exported for SQL & Power BI")

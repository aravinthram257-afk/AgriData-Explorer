import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AgriData Explorer", layout="wide")
st.title("🌾 AgriData Explorer – Analytical Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/cleaned_agri_data.csv")
    df.replace(-1, pd.NA, inplace=True)
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filters")
selected_state = st.sidebar.multiselect(
    "Select State",
    df["state_name"].dropna().unique()
)

if selected_state:
    df = df[df["state_name"].isin(selected_state)]

# =========================================================
# 1️⃣ Year-wise Trend of Rice Production Across Top 3 States
# =========================================================
st.subheader("1️⃣ Rice Production Trend – Top 3 States")

top3 = (
    df.groupby("state_name")["rice_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .index
)

trend = (
    df[df["state_name"].isin(top3)]
    .groupby(["year", "state_name"])["rice_production_(1000_tons)"]
    .sum()
    .reset_index()
)

fig1 = px.line(trend, x="year",
               y="rice_production_(1000_tons)",
               color="state_name")

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 2️⃣ Top 5 Districts by Wheat Yield Increase (Last 5 Years)
# =========================================================
st.subheader("2️⃣ Top 5 Districts by Wheat Yield Growth")

max_year = df["year"].max()
last5 = df[df["year"] >= max_year - 5]

growth = (
    last5.groupby("dist_name")["wheat_yield_(kg_per_ha)"]
    .agg(["max", "min"])
)

growth["growth"] = growth["max"] - growth["min"]

top_growth = growth.sort_values("growth", ascending=False).head(5)

st.dataframe(top_growth)

# =========================================================
# 3️⃣ States with Highest Oilseed Growth (5-Year)
# =========================================================
st.subheader("3️⃣ Oilseed Production Growth (5 Years)")

latest = df[df["year"] == max_year]
previous = df[df["year"] == max_year - 5]

growth_oil = (
    latest.groupby("state_name")["oilseeds_production_(1000_tons)"].sum()
    - previous.groupby("state_name")["oilseeds_production_(1000_tons)"].sum()
)

top_oil = growth_oil.sort_values(ascending=False).head(5)

st.bar_chart(top_oil)

# =========================================================
# 4️⃣ District-wise Area vs Production (Rice)
# =========================================================
st.subheader("4️⃣ Area vs Production (Rice)")

fig4 = px.scatter(df,
                  x="rice_area_(1000_ha)",
                  y="rice_production_(1000_tons)",
                  color="state_name",
                  opacity=0.5)

st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# 5️⃣ Cotton Production Growth (Top 5 States)
# =========================================================
st.subheader("5️⃣ Cotton Production Trend (Top 5 States)")

top5_cotton = (
    df.groupby("state_name")["cotton_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

cotton_trend = (
    df[df["state_name"].isin(top5_cotton)]
    .groupby(["year", "state_name"])["cotton_production_(1000_tons)"]
    .sum()
    .reset_index()
)

fig5 = px.line(cotton_trend,
               x="year",
               y="cotton_production_(1000_tons)",
               color="state_name")

st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# 6️⃣ Highest Groundnut Production (2017)
# =========================================================
st.subheader("6️⃣ Highest Groundnut Production – 2017")

groundnut_2017 = (
    df[df["year"] == 2017]
    .groupby("dist_name")["groundnut_production_(1000_tons)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(groundnut_2017)

# =========================================================
# 7️⃣ Annual Average Maize Yield
# =========================================================
st.subheader("7️⃣ Annual Average Maize Yield")

maize_avg = (
    df.groupby("year")["maize_yield_(kg_per_ha)"]
    .mean()
)

st.line_chart(maize_avg)

# =========================================================
# 8️⃣ Total Oilseed Area per State
# =========================================================
st.subheader("8️⃣ Total Oilseed Area by State")

oil_area = (
    df.groupby("state_name")["oilseeds_area_(1000_ha)"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(oil_area)

# =========================================================
# 9️⃣ Districts with Highest Rice Yield
# =========================================================
st.subheader("9️⃣ Top Districts by Rice Yield")

top_rice_yield = (
    df.groupby("dist_name")["rice_yield_(kg_per_ha)"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_rice_yield)

# =========================================================
# 🔟 Rice vs Wheat Production (Top 5 States, 10 Years)
# =========================================================
st.subheader("🔟 Rice vs Wheat Production Comparison")
last10 = df[df["year"] >= max_year - 10]
top5 = (
    last10.groupby("state_name")[[
        "rice_production_(1000_tons)",
        "wheat_production_(1000_tons)"
    ]]
    .sum()
    .sum(axis=1)
    .sort_values(ascending=False)
    .head(5)
    .index
)
comparison = (
    last10[last10["state_name"].isin(top5)]
    .groupby(["year", "state_name"])[
        ["rice_production_(1000_tons)",
         "wheat_production_(1000_tons)"]
    ]
    .sum()
    .reset_index()
)
fig10 = px.line(comparison,
                x="year",
                y=["rice_production_(1000_tons)",
                   "wheat_production_(1000_tons)"],
                color="state_name")
st.plotly_chart(fig10, use_container_width=True)

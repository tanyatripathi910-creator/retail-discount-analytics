import streamlit as st, pandas as pd, plotly.express as px

st.set_page_config(page_title="Retail Discount Analytics", layout="wide")
df = pd.read_csv("summary.csv")
st.title("Retail Discount Strategy & Profitability Dashboard")

depts = st.sidebar.multiselect("Department", sorted(df.DEPARTMENT.unique()), default=sorted(df.DEPARTMENT.unique()))
wmin, wmax = int(df.WEEK_NO.min()), int(df.WEEK_NO.max())
weeks = st.sidebar.slider("Week range", wmin, wmax, (wmin, wmax))
d = df[df.DEPARTMENT.isin(depts) & df.WEEK_NO.between(*weeks)]

if d.empty:
    st.warning("No data for this selection.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Net Revenue", f"${d.SALES_VALUE.sum():,.0f}")
c2.metric("Total Discounts", f"${d.TOTAL_DISC.sum():,.0f}")
c3.metric("Discount Rate", f"{d.TOTAL_DISC.sum()/d.GROSS_SALES.sum()*100:.1f}%")

wk = d.groupby("WEEK_NO")[["TOTAL_DISC","GROSS_SALES"]].sum().reset_index()
wk["Discount Rate (%)"] = wk.TOTAL_DISC / wk.GROSS_SALES * 100
st.plotly_chart(px.line(wk, x="WEEK_NO", y="Discount Rate (%)", title="Weekly Discount Rate (%)"), use_container_width=True)

dp = d.groupby("DEPARTMENT")[["SALES_VALUE","TOTAL_DISC","GROSS_SALES"]].sum().reset_index()
dp["Discount Rate (%)"] = dp.TOTAL_DISC / dp.GROSS_SALES * 100
st.plotly_chart(px.bar(dp.sort_values("Discount Rate (%)"), x="Discount Rate (%)", y="DEPARTMENT", orientation="h",
                title="Discount Rate by Department (%)"), use_container_width=True)
st.plotly_chart(px.scatter(dp, x="Discount Rate (%)", y="SALES_VALUE", hover_name="DEPARTMENT",
                title="Discount Rate vs Net Revenue"), use_container_width=True)

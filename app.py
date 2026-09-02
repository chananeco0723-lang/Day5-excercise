import streamlit as st
import pandas as pd
import plotly.express as px

# ===== 1. 设置页面 =====
st.set_page_config(page_title="房地产行业监测仪表盘", layout="wide")
st.title("🏠 美国房地产宏观监测")

# ===== 2. 读入数据 =====
df = pd.read_csv("data/macro_monthly.csv", parse_dates=["observation_date"], index_col="observation_date")

# ===== 3. 侧边栏：时间范围选择 =====
st.sidebar.header("设置")
min_date = df.index.min()
max_date = df.index.max()
start_date, end_date = st.sidebar.slider(
    "选择时间范围",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
    format="YYYY-MM-DD"
)

# 筛选数据
df_filtered = df.loc[start_date:end_date]

# ===== 4. 展示最新数值 =====
st.subheader("最新数据概览")
col1, col2, col3, col4 = st.columns(4)
latest = df.iloc[-1]
prev = df.iloc[-2]

col1.metric("10年期国债收益率", f"{latest['US_10Y_Treasury']:.2f}%", f"{latest['US_10Y_Treasury'] - prev['US_10Y_Treasury']:.2f}")
col2.metric("30年房贷利率", f"{latest['US_30Y_Mortgage']:.2f}%", f"{latest['US_30Y_Mortgage'] - prev['US_30Y_Mortgage']:.2f}")
col3.metric("新屋销售（千户）", f"{latest['US_New_Home_Sales']:.0f}", f"{latest['US_New_Home_Sales'] - prev['US_New_Home_Sales']:.0f}")
col4.metric("CPI指数", f"{latest['US_CPI']:.1f}", f"{latest['US_CPI'] - prev['US_CPI']:.1f}")

# ===== 5. 画图 =====
st.subheader("趋势图")

tab1, tab2 = st.tabs(["利率走势", "销售与通胀"])

with tab1:
    fig_rate = px.line(df_filtered, y=["US_10Y_Treasury", "US_30Y_Mortgage"], 
                       title="美国利率走势", labels={"value": "利率(%)", "variable": "指标"})
    st.plotly_chart(fig_rate, use_container_width=True)

with tab2:
    fig_sales = px.line(df_filtered, y="US_New_Home_Sales", title="美国新屋销售", labels={"US_New_Home_Sales": "千户"})
    st.plotly_chart(fig_sales, use_container_width=True)
    
    fig_cpi = px.line(df_filtered, y="US_CPI", title="美国CPI指数", labels={"US_CPI": "指数"})
    st.plotly_chart(fig_cpi, use_container_width=True)
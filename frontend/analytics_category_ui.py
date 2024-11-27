from datetime import datetime, timedelta
import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

current_date = datetime.now().date()
date_30_days_ago = current_date - timedelta(days=30)


def analytics_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date_30_days_ago)
    with col2:
        end_date = st.date_input("End Date", current_date)
    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response = response.json()

        # data = {
        #     "Category": list(response.keys()),
        #     "Total": [response[category]["total"] for category in response],
        #     "Percentage": [response[category]["percentage"] for category in response]
        # }

        data = [{"Category": category, "Total": values["total"], "Percentage": values["percentage"]}
                for category, values in response.items()]
        #st.write(data)
        #st.write(df)
        #st.write(response)
        #st.table(df)
        df = pd.DataFrame(data)
        if df.empty:
            st.warning("No data available to display.")
        else:
            df["Percentage"] = pd.to_numeric(df["Percentage"], errors="coerce")
            df_sorted = df.sort_values(by="Percentage", ascending=False)
            df_sorted.set_index("Category", inplace=True)
            st.title("Expense Breakdown By Category")

            df_sorted["Total"] = df_sorted["Total"].round(2)
            df_sorted["Percentage"] = df_sorted["Percentage"].round(2)
            st.bar_chart(data=df_sorted["Percentage"], width=0, height=0, use_container_width=True)
            st.dataframe(df_sorted)

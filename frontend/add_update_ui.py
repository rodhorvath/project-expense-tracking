# The original solution did not work correctly.  When adding an Amount and selecting a
# different date, the system did not initialize Amount back to 0.0.  Removed the original
# initialization code and made certain that st.session_state was used to override the key
# value.  The original code tried to initialize the value but the key overrode it.
#main branch
from datetime import datetime
import streamlit as st
import requests

API_URL = "http://localhost:8000"

now = datetime.now().date()


def add_update_tab():
    selected_date = st.date_input("Enter Date", now, label_visibility="collapsed")

    if "last_selected_date" not in st.session_state:
        st.session_state.last_selected_date = selected_date
    # Reset session state values when the date changes
    if selected_date != st.session_state.last_selected_date:
        st.session_state.last_selected_date = selected_date
        for i in range(5):  # Reset widgets for up to 5 expenses
            st.session_state[f"amount_{i}"] = 0.0
            st.session_state[f"category_{i}"] = "Shopping"
            st.session_state[f"notes_{i}"] = ""

    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []
    st.write(existing_expenses)

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
    with st.form(key="expense_form"):

        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                # Load existing expense data into session state
                st.session_state[f"amount_{i}"] = existing_expenses[i].get("amount", 0.0)
                st.session_state[f"category_{i}"] = existing_expenses[i].get("category", "Shopping")
                st.session_state[f"notes_{i}"] = existing_expenses[i].get("notes", "")

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0,
                                               key= f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options = categories,
                                              key= f"category_{i}",label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes",
                                            key=f"notes_{i}",label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
        submit_button = st.form_submit_button()
        if submit_button:
            st.write(expenses)
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses")


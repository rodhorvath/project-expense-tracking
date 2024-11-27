from datetime import datetime, timedelta
import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

current_date = datetime.now().date()
date_30_days_ago = current_date - timedelta(days=30)


def analytics_month_tab():
    pass
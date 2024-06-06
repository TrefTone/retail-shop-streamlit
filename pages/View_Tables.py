import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import mysql.connector
import numpy as np
import time

from streamlit.errors import StreamlitAPIException, DuplicateWidgetID
from mysql.connector import IntegrityError

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="retail_shop",
    user="root",
    password=""
)

st.set_page_config(page_title="Tables", page_icon=":bar_chart:", layout="wide")

st.title("Schema tables")

query_cust = 'select * from customer'
query_emp = 'select * from employee'
query_prod = 'select * from product'
query_sale = 'select * from sale'
query_saleProd = 'select * from saleProduct'

df_cust = pd.read_sql(query_cust, mydb)
df_emp = pd.read_sql(query_emp, mydb)
df_prod = pd.read_sql(query_prod, mydb)
df_sale = pd.read_sql(query_sale, mydb)
df_saleProduct = pd.read_sql(query_saleProd, mydb)

st.write("Customer Table")
st.dataframe(df_cust, hide_index=True, use_container_width=True)

st.write("Employee Table")
st.dataframe(df_emp, hide_index=True, use_container_width=True)

st.write("Product Table")
st.dataframe(df_prod, hide_index=True, use_container_width=True)

st.write("Sale Table")
st.dataframe(df_sale, hide_index=True, use_container_width=True)

st.write("Product Sales Table")
st.dataframe(df_saleProduct, hide_index=True, use_container_width=True)

import mysql.connector
import pandas as pd
import streamlit as st

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
query_branch = 'select * from branch'
query_emp = 'select * from employee'
query_prod = 'select * from product'
query_sale = 'select * from sale'
query_saleProd = 'select * from saleProduct'

df_cust = pd.read_sql(query_cust, mydb)
df_branch = pd.read_sql(query_branch, mydb)
df_emp = pd.read_sql(query_emp, mydb)
df_prod = pd.read_sql(query_prod, mydb)
df_sale = pd.read_sql(query_sale, mydb)
df_saleProduct = pd.read_sql(query_saleProd, mydb)

def show_table(df):
    st.dataframe(df, hide_index=True, use_container_width=True)

st.write("Customer Table")
show_table(df_cust)

st.write("Branch Table")
show_table(df_branch)

st.write("Employee Table")
show_table(df_emp)

st.write("Product Table")
show_table(df_prod)

st.write("Sale Table")
show_table(df_sale)

st.write("Product Sales Table")
show_table(df_saleProduct)

st.write("Apply query operations")
with st.form(key="form1"):
    str1 = st.text_area("Enter the query here:")
    submit = st.form_submit_button("Submit")
    if submit:
        try:
            df = pd.read_sql(str1,mydb)
            show_table(df)
        except mysql.connector.Error as e:
            st.warning(e)
        except TypeError as e:
            pass

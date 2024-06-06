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

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")


queryProd = ("""SELECT s.SaleID, s.Date, s.CustomerID, s.EmployeeID,
         p.Name, sp.ProductID, sp.Quantity,p.price
         FROM sale s 
         LEFT JOIN saleproduct sp ON s.SaleID = sp.SaleID
         LEFT JOIN product p ON p.ProductID = sp.ProductID;""")

querySale = 'SELECT * from sale'

dfSale = pd.read_sql(querySale, mydb)
dfProd = pd.read_sql(queryProd, mydb)

st.title("Sales Dashboard")
st.write("View sales data from the MySQL database")

# Display the sales data
st.dataframe(dfSale,hide_index=True,use_container_width=True)
st.dataframe(dfProd,hide_index=True,use_container_width=True)

# Example: Display a bar chart of total sales by product
st.subheader("Total Sales by Product")
total_sales_by_ID = dfProd.groupby("Name")["price"].sum()
st.bar_chart(total_sales_by_ID)

# Visualization: Total Sales by Date
st.header('Total Sales by Date')
dfSale['Date'] = pd.to_datetime(dfSale['Date'])
# Group by date and calculate total sales
total_sales_by_date = dfSale.groupby(dfSale['Date'].dt.strftime('%d/%m/%y'))['TotalAmount'].sum().reset_index()
# Create a bar chart
fig1 = px.bar(total_sales_by_date, x='Date', y='TotalAmount', title='Total Sales by Date')
# Display the chart using Streamlit
st.plotly_chart(fig1)

# Visualization: Quantity Sold per Product
st.header('Quantity Sold per Product')
quantity_per_product = dfProd.groupby('Name')['Quantity'].sum().reset_index()
fig2 = px.scatter(quantity_per_product, x='Name', y='Quantity', size='Quantity', title='Quantity Sold per Product')
st.plotly_chart(fig2)

# Create a pie chart
fig_pie = px.pie(quantity_per_product, values='Quantity', names='Name', title='Quantity Sold per Product (Pie Chart)')
st.plotly_chart(fig_pie)

earning_per_product = dfProd.groupby('Name')['price'].sum().reset_index()
fig_pie = px.pie(earning_per_product, values='price', names='Name', title='Earning per Product (Pie Chart)')
st.plotly_chart(fig_pie)

# Additional Visualization: Total Sales by Customer
st.header('Total Sales by Employee')
total_sales_by_customer = dfSale.groupby('EmployeeID')['TotalAmount'].sum().reset_index()
fig3 = px.bar(total_sales_by_customer, x='EmployeeID', y='TotalAmount', title='Total Sales by Employee (in dollars)')
st.plotly_chart(fig3)
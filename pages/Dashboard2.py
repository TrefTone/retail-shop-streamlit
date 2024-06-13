import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Establish connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="retail_shop",
    user="root",
    password=""
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SQL queries to fetch data from the database
queryProd = """
SELECT s.SaleID, s.Date, s.CustomerID, s.EmployeeID,
       p.ProdName, sp.ProductID, sp.Quantity, p.price
FROM sale s 
LEFT JOIN saleproduct sp ON s.SaleID = sp.SaleID
LEFT JOIN product p ON p.ProductID = sp.ProductID;
"""

queryEmp = """
SELECT s.SaleID, s.BranchID, s.Date, s.TotalAmount, s.CustomerID, s.EmployeeID,
       e.EmpName
FROM sale s 
LEFT JOIN employee e ON s.EmployeeID = e.EmployeeID;
"""

# Load data into pandas DataFrame
dfEmp = pd.read_sql(queryEmp, mydb)

querySale = 'SELECT s.SaleID, s.BranchID, s.Date, s.TotalAmount, s.CustomerID, s.EmployeeID from sale s'

# Load data into pandas DataFrames
dfSale = pd.read_sql(querySale, mydb)
dfProd = pd.read_sql(queryProd, mydb)

st.title('Sales Dashboard')
# Sidebar configuration
col1, col2, col3 = st.columns(3)

with col1:
    # Year selection
    year_list = pd.to_datetime(dfSale['Date']).dt.year.unique().tolist()
    selected_year = st.selectbox('Select a year', year_list)

    # Filter data based on the selected year
    dfSale['Date'] = pd.to_datetime(dfSale['Date'])
    dfSale_filtered = dfSale[dfSale['Date'].dt.year == selected_year]
    dfProd['Date'] = pd.to_datetime(dfProd['Date'])
    dfProd_filtered = dfProd[dfProd['Date'].dt.year == selected_year]

# Dashboard Main Panel
col1, col2 = st.columns(2)

with col1:
    # Create subplot with two pie charts vertically aligned
    st.markdown('### Sales and Earnings by Product')

    # Quantity Sold per Product (Pie Chart)
    quantity_per_product = dfProd_filtered.groupby('ProdName')['Quantity'].sum().reset_index()
    fig_pie_quantity = px.pie(quantity_per_product, values='Quantity', names='ProdName',
                              title='Quantity Sold per Product',
                              width=400, height=400)

    # Earning per Product (Pie Chart)
    earning_per_product = dfProd_filtered.groupby('ProdName')['price'].sum().reset_index()
    fig_pie_earning = px.pie(earning_per_product, values='price', names='ProdName',
                             title='Earning per Product',
                             width=400, height=400)

    # Display pie charts side by side
    st.plotly_chart(fig_pie_quantity)
    st.plotly_chart(fig_pie_earning)

with col2:
    st.markdown(f'#### Total Sales {selected_year}')
    total_sales_by_date = dfSale_filtered.groupby(dfSale_filtered['Date'].dt.date)['TotalAmount'].sum().reset_index()
    total_sales_by_date['TotalAmount'] = total_sales_by_date['TotalAmount'].round(2)  # Round to 2 decimal places
    line_chart = px.line(total_sales_by_date, x='Date', y='TotalAmount',
                         title=f'Total Sales by Date for {selected_year}',
                         color_discrete_sequence=px.colors.sequential.Blues)

    # Highlight points with red circles
    line_chart.update_traces(mode='markers+lines', marker=dict(color='red', size=8, symbol='circle'),
                             line=dict(color='blue', width=2))

    line_chart.update_xaxes(type='category')  # Ensures x-axis treats dates as categories
    st.plotly_chart(line_chart, use_container_width=False)

    colO1, colO2 = st.columns(2)

    with colO1:
        st.markdown('#### Top Products')
        top_products = dfProd_filtered.groupby('ProdName')['price'].sum().reset_index().sort_values(by="price",
                                                                                                    ascending=False)
        st.dataframe(top_products, hide_index=True, use_container_width=True)

    with colO2:
        st.markdown('#### Top Employees')
        top_employees = dfEmp.groupby('EmpName')['TotalAmount'].sum().reset_index().sort_values(by="TotalAmount",
                                                                                                ascending=False)
        st.dataframe(top_employees, hide_index=True, use_container_width=True)

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

# Title
st.title(":bar_chart: Sales Dashboard")

# Selection configuration
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
    dfEmp['Date'] = pd.to_datetime(dfEmp['Date'])
    dfEmp_filtered = dfEmp[dfEmp['Date'].dt.year == selected_year]

# Calculate the total sales, total products sold, and average sales per transaction
total_sales = int(dfSale_filtered["TotalAmount"].sum())
total_prod = int(dfProd_filtered["Quantity"].sum())
avg_transaction = int(dfSale_filtered["TotalAmount"].sum()/len(dfSale_filtered.columns))

# Dashboard Main Panel
left_column, middle_column, right_column = st.columns(3)

# Use markdown to create a box with a background color and center align the text
with left_column:
    st.markdown(f"""
    <div style="background-color:#ebd2b9;padding:10px;border-radius:5px;">
        <h5 style="text-align:center;">Total Sales:</h5>
        <h3 style="text-align:center;">US $ {total_sales:,}</h3>
    </div>
    """, unsafe_allow_html=True)

with middle_column:
    st.markdown(f"""
    <div style="background-color:#ebd2b9;padding:10px;border-radius:5px;">
        <h5 style="text-align:center;">Products sold:</h5>
        <h3 style="text-align:center;">{total_prod}</h3>
    </div>
    """, unsafe_allow_html=True)

with right_column:
    st.markdown(f"""
    <div style="background-color:#ebd2b9;padding:10px;border-radius:5px;">
        <h5 style="text-align:center;">Average Sales Per Transaction:</h5>
        <h3 style="text-align:center;">US $ {avg_transaction}</h3>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""---""")

st.subheader(f'Total Sales {selected_year}')
total_sales_by_date = dfSale_filtered.groupby(dfSale_filtered['Date'].dt.date)['TotalAmount'].sum().reset_index()
total_sales_by_date['TotalAmount'] = total_sales_by_date['TotalAmount'].round(2)  # Round to 2 decimal places
line_chart = px.line(total_sales_by_date, x='Date', y='TotalAmount',
                     color_discrete_sequence=px.colors.sequential.Blues)

# Highlight points with red circles
line_chart.update_traces(mode='markers+lines', marker=dict(color='red', size=8, symbol='circle'),
                         line=dict(color='blue', width=2))

line_chart.update_xaxes(type='category')  # Ensures x-axis treats dates as categories
st.plotly_chart(line_chart, use_container_width=False)


totalQuan = dfProd['Quantity'].sum()
# Quantity Sold per Product (Pie Chart)
quantity_per_product = dfProd_filtered.groupby('ProdName')['Quantity'].sum().reset_index()
fig_pie_quantity = px.pie(quantity_per_product,title='Sales per product', values='Quantity', names='ProdName',
                          width=300, height=300)

# Calculate total earnings by multiplying price and quantity bought
dfProd_filtered.loc[:, 'total_earnings'] = dfProd_filtered.loc[:, 'price'] * dfProd_filtered.loc[:, 'Quantity']
# Group by product name and sum the total earnings
earning_per_product = dfProd_filtered.groupby('ProdName')['total_earnings'].sum().reset_index()
# Create a pie chart for earnings per product
fig_pie_earning = px.pie(earning_per_product,title='Earning per product', values='total_earnings', names='ProdName',
                         width=300, height=300)

fig_pie_quantity.update_layout(
    title={
        'text': "Sales per product",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            size=24
        )
    }
)

# Assuming you have a plotly figure named fig_pie_earning
fig_pie_earning.update_layout(
    title={
        'text': "Earning per product",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(

            family = 'Source sans pro',
            size=24,
        )
    }
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.plotly_chart(fig_pie_quantity,use_container_width=False)

with col2:
    st.plotly_chart(fig_pie_earning)

with col3:
    st.markdown('#### Top Products')
    top_products = dfProd_filtered.groupby('ProdName')['total_earnings'].sum().reset_index().sort_values(
        by="total_earnings",
        ascending=False)
    st.dataframe(top_products, hide_index=True, use_container_width=True)

with col4:
    st.markdown('#### Top Employees')
    top_employees = dfEmp_filtered.groupby('EmpName')['TotalAmount'].sum().reset_index().sort_values(by="TotalAmount",
                                                                                                     ascending=False)
    st.dataframe(top_employees, hide_index=True, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
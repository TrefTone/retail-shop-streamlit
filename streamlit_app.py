import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import mysql.connector
import numpy as np
import time

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="retail_shop",
    user="root",
    password=""
)

mycursor = mydb.cursor()
print("connection established")


def get_product_price(prod_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT price FROM product WHERE ProductID = %s", (prod_id,))
    result = mycursor.fetchone()
    return result[0] if result else 0


def main():
    st.title("Retail store management");

    option = st.sidebar.selectbox("Select an operation", ("Create", "Delete", "Show", "Update", "Visualize"))

    if option == "Create":
        st.subheader("Create record")

        option_create = st.selectbox("Select option", ("New Purchase", "New Employee", "New Product", "Product Restock"
                                                       , "New Supplier"))
        if option_create == "New Purchase":
            emp_id = st.number_input("Employee ID", min_value=0, step=1, format='%d')
            date = st.date_input("Today's date")

            cust_id = np.random.randint(10000, 100000)
            cust_name = st.text_input("Customer name")
            cust_email = st.text_input("Customer email")
            cust_phone = st.text_input("Customer Phone number")
            cust_addr = st.text_input("Customer Address")

            sale_id = np.random.randint(10000, 100000)

            unique_items = st.number_input("Total unique items", min_value=0, step=1, format='%d')
            total_price = 0

            for i in range(int(unique_items)):
                prod_id = st.number_input(f"Product {i + 1} ID", min_value=0, step=1, format='%d')
                prod_quantity = st.number_input(f"Product {i + 1} quantity", min_value=0, step=1, format='%d')

                product_price = get_product_price(prod_id)
                total_price += product_price * prod_quantity

            st.write(f"Total purchase amount: ${total_price}")

            if st.button("Submit record"):
                sql_cust = "insert into customer values(%s,%s,%s,%s,%s)"
                val_cust = (cust_id, cust_name, cust_email, cust_phone, cust_addr)
                mycursor.execute(sql_cust, val_cust)

                sql_sale = "insert into sale values(%s,%s,%s,%s,%s)"
                val_sale = (sale_id, date, total_price, cust_id, emp_id)
                mycursor.execute(sql_sale, val_sale)

                sql_saleProd = "insert into saleproduct values(%s,%s,%s)"
                val_saleProd = (sale_id, prod_id, prod_quantity)
                mycursor.execute(sql_saleProd, val_saleProd)

                mydb.commit()
                success_message = st.empty()
                success_message.success("Record created")
                time.sleep(5)
                success_message.empty()

        elif option_create == "New Employee":
            emp_id = st.number_input("Employee ID", min_value=0, step=1, format='%d')
            emp_name = st.text_input("Employee name")
            hire_date = st.date_input("Hire date")
            position = st.text_input("Position")
            salary = st.number_input("Salary (in dollars)", step=1000)

            if st.button("Submit record"):
                sql_emp = "insert into employee values(%s,%s,%s,%s,%s)"
                val_emp = (emp_id, emp_name, position, salary, hire_date)
                mycursor.execute(sql_emp, val_emp)

                mydb.commit()
                success_message = st.empty()
                success_message.success("Record created")
                time.sleep(5)
                success_message.empty()

        elif option_create == "New Product":
            prod_id = st.number_input("Product ID", min_value=0, step=1, format='%d')
            prod_name = st.text_input("Product name")
            price = st.number_input("Price", min_value=0)
            desc = st.text_input("Product description")
            quantity = st.number_input("Stock quantity", min_value=0, step=1)

            if st.button("Submit record"):
                sql_prod = "insert into product values(%s,%s,%s,%s,%s)"
                val_prod = (prod_id, prod_name, price, desc, quantity)
                mycursor.execute(sql_prod, val_prod)

                mydb.commit()
                success_message = st.empty()
                success_message.success("Record created")
                time.sleep(5)
                success_message.empty()




    elif option == "Delete":
        st.subheader("Delete record")
        option_delete = st.selectbox("Select option", ("Return purchase", "Remove Employee", "Delete Product"
                                                       , "Remove Supplier"))

    elif option == "Show":
        st.subheader("Show records")
        option_show = st.selectbox("Select option", ("Customer", "Employee", "Product", "Sale"
                                                     , "Saleproduct", "Supplier"))

    elif option == "Update":
        st.subheader("Update record")
        option_update = st.selectbox("Select option", ("Employee details", "Product details"
                                                       , "Supplier details"))

    elif option == "Visualize":
        st.subheader("Get Visualizations")


if __name__ == "__main__":
    main()

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

mycursor = mydb.cursor()
print("connection established")

st.set_page_config(page_title="Store manager", page_icon=":shopping_bags:", layout="wide")


def get_product_price(prod_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT price FROM product WHERE ProductID = %s", (prod_id,))
    result = mycursor.fetchone()
    return float(result[0]) if result else 0  # Remove float() if error occurs


def get_product_quantity(prod_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT stockquantity FROM product WHERE ProductID = %s", (prod_id,))
    result = mycursor.fetchone()
    return result[0] if result else 0


def get_employee_id(emp_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT employeeid FROM employee WHERE employeeid = %s", (emp_id,))
    result = mycursor.fetchone()
    return result[0] if result else 0


def get_customer_id(cust_phone):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT customerid FROM customer WHERE phone = %s", (cust_phone,))
    result = mycursor.fetchone()
    if result:
        # If customer exists, return the existing ID
        return result[0], 0
    else:
        # If customer does not exist, generate a random ID
        cust_id = np.random.randint(10000, 100000)
        return cust_id, 1


def main():
    st.title("Retail store management")

    option = st.sidebar.radio("Select an operation", ("Create", "Delete", "Update"))

    # Create record
    if option == "Create":
        st.subheader("Create record")

        option_create = st.selectbox("Select option",
                                     ("New Purchase", "New Employee", "New Product"))

        # New Purchase
        if option_create == "New Purchase":
            emp_id = st.number_input("Employee ID", min_value=0, step=1, format='%d')
            date = st.date_input("Today's date")
            cust_name = st.text_input("Customer name")
            cust_email = st.text_input("Customer email")
            cust_phone = st.text_input("Customer Phone number")
            cust_addr = st.text_input("Customer Address")

            cust_id, flag = get_customer_id(cust_phone)

            sale_id = np.random.randint(10000, 100000)

            unique_items = st.number_input("Total unique items", min_value=0, step=1, format='%d')
            total_price = 0

            prod_dict = {}
            for i in range(int(unique_items)):
                prod_id = st.number_input(f"Product {i + 1} ID", min_value=0, step=1, format='%d')
                if get_product_quantity(prod_id) > 0:
                    try:
                        prod_quantity = st.slider(f"Product {i + 1} quantity", 0, get_product_quantity(prod_id), 1)
                    except StreamlitAPIException as e:
                        st.error("Enter correct amount")
                else:
                    st.warning("Product out of stock")
                    continue
                prod_dict[prod_id] = prod_quantity

                product_price = get_product_price(prod_id)
                total_price += product_price * prod_quantity

            st.write(f"Total purchase amount: ${total_price:.2f}")

            if st.button("Submit record"):
                try:
                    if flag == 1:
                        sql_cust = "insert into customer values(%s,%s,%s,%s,%s)"
                        val_cust = (cust_id, cust_name, cust_email, cust_phone, cust_addr)
                        mycursor.execute(sql_cust, val_cust)

                    sql_sale = "insert into sale values(%s,%s,%s,%s,%s)"
                    val_sale = (sale_id, date, total_price, cust_id, emp_id)
                    mycursor.execute(sql_sale, val_sale)

                    for prod_id, prod_quantity in prod_dict.items():
                        sql_saleProd = "insert into saleproduct values(%s,%s,%s)"
                        val_saleProd = (sale_id, prod_id, prod_quantity)
                        mycursor.execute(sql_saleProd, val_saleProd)

                        sql_saleProd = ("UPDATE product SET stockquantity = stockquantity - %s "
                                        "WHERE ProductID = %s;")
                        val_saleProd = (prod_quantity, prod_id)
                        mycursor.execute(sql_saleProd, val_saleProd)

                        mydb.commit()
                        success_message = st.empty()
                        success_message.success("Record created")
                        time.sleep(5)
                        success_message.empty()

                except IntegrityError as e:
                    st.error("Invalid input")

        # New Employee
        elif option_create == "New Employee":
            emp_id = st.number_input("EmployeeID", min_value=0, step=1, format='%d')
            emp_name = st.text_input("Name")
            hire_date = st.date_input("Hire date")
            position = st.text_input("Position")
            salary = st.number_input("Salary (in dollars)", min_value=1000, step=1000)

            if st.button("Submit record"):
                try:
                    sql_emp = "insert into employee values(%s,%s,%s,%s,%s)"
                    val_emp = (emp_id, emp_name, position, salary, hire_date)
                    mycursor.execute(sql_emp, val_emp)

                    mydb.commit()
                    success_message = st.empty()
                    success_message.success("Record created")
                    time.sleep(5)
                    success_message.empty()
                except IntegrityError as e:
                    st.error("Employee ID already exists")

        # Add new product
        elif option_create == "New Product":

            prod_id = st.number_input("Product ID", min_value=0, step=1, format='%d')

            prod_name = st.text_input("Name")
            price = st.number_input("Price", min_value=0.0)
            desc = st.text_input("Product description")
            quantity = st.number_input("Stock quantity", min_value=0, step=1)

            if st.button("Submit record"):

                try:
                    sql_prod = "insert into product values(%s,%s,%s,%s,%s)"
                    val_prod = (prod_id, prod_name, price, desc, quantity)
                    mycursor.execute(sql_prod, val_prod)

                    mydb.commit()
                    success_message = st.empty()
                    success_message.success("Record created")
                    time.sleep(5)
                    success_message.empty()
                except IntegrityError as e:
                    st.error("Product ID already exists")

    # Delete record operations
    elif option == "Delete":
        st.subheader("Delete record")
        option_delete = st.selectbox("Select option", ("Return purchase", "Remove Employee", "Delete Product"))

        if option_delete == "Return purchase":
            st.warning("To be implemented")

        # Remove Employee
        if option_delete == "Remove Employee":
            emp_id = st.number_input("Enter employee ID", step=1)

            if st.button("Delete record"):

                if get_employee_id(emp_id) == 0:
                    st.error("No such Employee")

                else:
                    sql_emp = "delete from employee where employeeid = %s"
                    val_emp = (emp_id,)
                    mycursor.execute(sql_emp, val_emp)

                    mydb.commit()
                    message = st.empty()
                    message.success("Record deleted")
                    time.sleep(5)
                    message.empty()

        # Delete product
        if option_delete == "Delete Product":
            prod_id = st.number_input("Enter product ID", step=1)

            if st.button("Delete record"):

                if get_product_price(prod_id) == 0:
                    message = st.empty()
                    message.error("No such product")
                    time.sleep(5)
                    message.empty()

                else:
                    sql_prod = "delete from product where productid = %s"
                    val_prod = (prod_id,)
                    mycursor.execute(sql_prod, val_prod)

                    mydb.commit()
                    message = st.empty()
                    message.success("Record deleted")
                    time.sleep(5)
                    message.empty()

    elif option == "Update":
        st.subheader("Update record")
        option_update = st.selectbox("Select option", ("Product Restock", "Employee details", "Product details"))

        # Restock product
        if option_update == "Product Restock":
            prod_id = st.number_input("Product ID", min_value=0, step=1, format='%d')
            prod_quantity = st.number_input("Product Quantity", min_value=0, step=5, format='%d')

            if st.button("Submit record"):
                sql_prodRestock = ("UPDATE product SET stockquantity = stockquantity + %s "
                                   "WHERE ProductID = %s;")
                val_prodRestock = (prod_quantity, prod_id)
                mycursor.execute(sql_prodRestock, val_prodRestock)

                mydb.commit()
                success_message = st.empty()
                success_message.success("Record created")
                time.sleep(5)
                success_message.empty()

        elif option_update == "Employee details":
            emp_id = st.number_input("EmployeeID", min_value=0, step=1, format='%d')

            update_name = st.checkbox("Update Name")
            update_position = st.checkbox("Update Position")
            update_salary = st.checkbox("Update Salary")
            update_hire_date = st.checkbox("Update Hire Date")

            # Display selected details
            if update_name:
                st.write("Name")
            if update_position:
                st.write("Position")
            if update_salary:
                st.write("Salary")
            if update_hire_date:
                st.write("Hire Date")

        elif option_update == "Product details":

            prod_id = st.number_input("Product ID", min_value=0, step=1, format='%d')

            if get_product_quantity(prod_id) > 0:

                # Create checkboxes for details to update
                update_name = st.checkbox("Update Name")
                update_price = st.checkbox("Update Price")
                update_description = st.checkbox("Update Description")
                update_stock_quantity = st.checkbox("Update Stock Quantity")

                # Display selected details
                st.write("Selected details to update:")
                if update_name:
                    prod_name = st.text_input("Name")

                if update_price:
                    price = st.number_input("Price", min_value=0.0, step=1.0, value=get_product_price(prod_id))

                if update_description:
                    desc = st.text_input("Product description")

                if update_stock_quantity:
                    quantity = st.number_input("Stock quantity", min_value=0, step=1, value=get_product_quantity(prod_id))

                if st.button("Update record"):
                    if update_name:
                        query_name = 'update product set name = %s where productid = %s'
                        val_name = (prod_name, prod_id)
                        mycursor.execute(query_name, val_name)

                    if update_price:
                        query_price = 'update product set price = %s where productid = %s'
                        val_price = (price, prod_id)
                        mycursor.execute(query_price, val_price)

                    if update_description:
                        query_desc = 'update product set description = %s where productid = %s'
                        val_desc = (desc, prod_id)
                        mycursor.execute(query_desc, val_desc)

                    if update_stock_quantity:
                        query_quan = 'update product set name = %s where productid = %s'
                        val_quan = (quantity, prod_id)
                        mycursor.execute(query_quan, val_quan)

                    mydb.commit()
                    success_message = st.empty()
                    success_message.success("Record updated")
                    time.sleep(5)
                    success_message.empty()

            else:
                st.warning("Product does not exist")


if __name__ == "__main__":
    main()

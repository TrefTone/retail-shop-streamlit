import csv
import json
import time
from json import JSONDecodeError

import streamlit as st
import pandas as pd
import mysql.connector
from collections import defaultdict

from streamlit_app import *

from streamlit.errors import StreamlitAPIException, DuplicateWidgetID
from mysql.connector import IntegrityError

from streamlit_app import mycursor

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="retail_shop",
    user="root",
    password=""
)

mycursor = mydb.cursor()

st.set_page_config(page_title="File processing", page_icon=":clipboard:", layout="wide")

st.title("Upload CSV or JSON")


def get_customer_id(cust_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT customerid FROM customer WHERE customerid = %s", (cust_id,))
    result = mycursor.fetchone()
    if result:
        # If customer exists, return the existing ID
        return result[0], 0
    else:
        # If customer does not exist, generate a random ID
        return cust_id, 1


def is_valid_file_extension(filename):
    valid_extensions = ['.csv', '.json']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)


file = st.file_uploader("Upload file", type=["csv", "json"])

if file:
    if is_valid_file_extension(file.name):
        st.success(f"File '{file.name}' is a valid .csv or .json file.")

        # Process the file (e.g., read CSV or JSON)

        # CSV file processing
        if file.name.lower().endswith(".csv"):
            df = pd.read_csv(file)
            st.write("CSV data:")
            st.write(df)

        # JSON file processing
        elif file.name.lower().endswith(".json"):
            try:
                json_data = json.load(file)
                st.write("JSON data:")
                st.write(json_data)

            except JSONDecodeError as e:
                file.seek(0)
                json_data = []
                for line in file:
                    json_data.append(json.loads(line))
                st.write("JSON data:")
                st.write(json_data)

            # Convert JSON data to CSV with dynamic fieldnames
            fieldnames = set()
            for entry in json_data:
                fieldnames.update(entry.keys())
            fieldnames = list(fieldnames)  # Convert to list for DictWriter

            # Handle additional metadata
            processed_data = []
            for entry in json_data:
                metadata = {}
                row = {}
                for key in fieldnames:
                    if key in entry:
                        row[key] = entry[key]
                    else:
                        metadata[key] = entry.get(key, None)
                row['Metadata'] = json.dumps(metadata) if metadata else None
                processed_data.append(row)

            flattened_json = "output.csv"
            with open(flattened_json, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames.append('Metadata')  # Add Metadata column to fieldnames
                csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerows(processed_data)

            df = pd.read_csv(flattened_json)
            df.columns = map(str.lower, df.columns)
            st.write("Flattened JSON data:")
            st.dataframe(df, hide_index=True, use_container_width=True)

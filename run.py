# Import libraries
import gspread                                                  # Python client for Google Sheets.
from google.oauth2.service_account import Credentials           # This imports the Credentials class from the google.oauth2.service_account module. This class is used to authenticate and authorize your Python script to access Google services,
from pprint import pprint

# 
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",             # Access and manage Google Sheets in your Google Drive.
    "https://www.googleapis.com/auth/drive.file",               # View and manage files in your Google Drive.
    "https://www.googleapis.com/auth/drive"                     # View and manage the entirety of your Google Drive.
    ]

CREDS = Credentials.from_service_account_file('creds.json')     # Authenticating and authorizing: Creates an object that contains credentials.
SCOPED_CREDS = CREDS.with_scopes(SCOPE)                         # Applying scope to credentials:  This takes the credentials you loaded and applies the permissions (or "scopes") you defined earlier. This tells Google, "Hey, I want to use these credentials, and I'm requesting these specific permissions."
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)                # Authorizing with gspread: This uses the gspread library to authorize your script with the scoped credentials. If successful, you'll get a client that can be used to interact with Google Sheets.
SHEET = GSPREAD_CLIENT.open('love_sandwiches')                  # Opening a Specific Google Sheet: This uses the authorized client to open a Google Sheet named "love_sandwiches". The SHEET object can now be used to read or modify this specific Google Sheet.

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string od data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
        # print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
             print("Data is valid!")
             break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
               raise ValueError(
                   f"Exactly 6 values required, you provided {len(values)}"
               )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

# Refactored into update_worksheet()
# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")

# Refactored into update_worksheet()
# def update_surplus_worksheet(data):
#     """
#     Update the surplus worksheet, add new row with the list data provided
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    Stock - Sales = Surplus
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches Data Automation")
main()
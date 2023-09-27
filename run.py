# Import libraries
import gspread                                                  # Python client for Google Sheets.
from google.oauth2.service_account import Credentials           # This imports the Credentials class from the google.oauth2.service_account module. This class is used to authenticate and authorize your Python script to access Google services,

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
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10, 20, 30, 40, 50, 60\n")

    data_str = input("Enter your data here: ")
    # print(f"The data provided is {data_str}")

    sales_data = data_str.split(",")
    validate_data(sales_data)

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


get_sales_data()
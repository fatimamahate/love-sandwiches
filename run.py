# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales data input from the user
    run a while loop to collect a valid string of
    data from the user via the terminal, which must
    be a string of 6 numbers seperated by commas, the
    loop will repeatedly request data until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers seperated by commas.")
        print("Example,12,20,30,40,50,60\n")

        data_str=input("Enter your data here: ")
        sales_data = data_str.split(',')
        validate_data(sales_data)

        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):

    """
    Inside the try, converts all stiring to integers.
    Raises ValueError if strings cannot be converted to int
    or if there isnt exactly 6 values
    """
    
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_sales_worksheet(data):
    """
    update sales workseet, add new row with the list data provided
    """
    print('updating sales worksheet...\n')
    sales_worksheet=SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('sales worksheet updated successfully. \n')

def calculate_surplus_data(data):
    """
    Compare sales with stock and calculate the surplus for each item type.

    the surplus is defined as the dales figure subtracted from the stock:
    * positive surplus indicates waste
    * negative surplus indicates extra made after stock was sold out
    """
    print('calculating surplus data ...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row=stock[-1]
    print(stock_row)
    
def main():
    """
    Run all program functions
    """
    data=get_sales_data()
    sales_data=[int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print('welcome to love sandwichs data automation')
main()
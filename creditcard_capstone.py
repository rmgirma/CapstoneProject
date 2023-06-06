import os
import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable

# function to clear the screen between menu change
def clear_screen():  
        _ = os.system('cls')
        
# connection to the database
conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='creditcard_capstone'
)

# Create a cursor object to load data
cursor = conn.cursor()
nav = "Press Enter key to continue..." # navigation prompt

# function to display transactions by zipcode
def zipcode_transactions():
    try:  # Start of try block
        clear_screen()
        print("\n" + "=" * 60)
        print("Report By Zip Code".center(60))
        print("=" * 60)
        zipcode = input("Enter Zip Code: ")
        month = input("Enter Month as 2 digits: ")
        year = input("Enter Year as YYYY: ")

        query = """SELECT ccard.TIMEID, cust.FIRST_NAME, cust.LAST_NAME, cust.cust_zip, cust.CREDIT_CARD_NO,
                ccard.TRANSACTION_TYPE, ccard.TRANSACTION_VALUE
                FROM cdw_sapp_customer cust join cdw_sapp_credit_card ccard on ccard.CUST_SSN = cust.SSN
                where cust.CUST_ZIP =  %s and MONTH(ccard.TIMEID) = %s AND YEAR(ccard.TIMEID) = %s
                order by ccard.TIMEID desc"""
        cursor.execute(query, (zipcode, month, year))
        results = cursor.fetchall()
        pretty = PrettyTable()  # create a PrettyTable object to display result in tabular manner
        pretty.field_names = ['DATE', 'FIRST_NAME', 'LAST_NAME', 'ZIP', 'CREDIT_CARD_NO', 'TRANSACTION_TYPE', 'TRANSACTION_VALUE']
        for result in results:
            pretty.add_row(result)
        print(pretty)
        input(nav)
    except Exception as err:  # Catch all other errors
        print(f"An error occurred: {err}")

def sum_by_type():
    clear_screen()
    while True:
        print("\n" + "=" * 60)
        print("Select Transaction Type".center(60))
        print("=" * 60)
        print("     1. Education")
        print("     2. Entertainment")
        print("     3. Healthcare")
        print("     4. Grocery")
        print("     5. Test")
        print("     6. Gas")
        print("     7. Bills")
        print("=" * 60)
        print("     8. Return to Main Menu")
        print("=" * 60)
        choice = input("Select Transaction Type: ")
        if choice == '1':
            print('Education')
            input(nav)
            clear_screen()
        elif choice == '2':
            print('Entertainment')
            input(nav)
            clear_screen()
        elif choice == '3':
            print('Healthcare')  
            input(nav)
            clear_screen()
        elif choice == '4':
            print('Grocery')
            input(nav)
            clear_screen()
        elif choice == '5':
            print('Test')
            input(nav)
            clear_screen()
        elif choice == '6':
            print('Gas')
            input(nav)
            clear_screen()
        elif choice == '7':
            print('Bills') 
            input(nav)
            clear_screen()  
        elif choice == '8':
            print("Returning to Main MENU...")     
            break
        else:
            print("Invalid choice. Please enter a valid Transaction Type.")

 
# Main Menu function        
def main_menu():
    while True:
        clear_screen()
        print("\n" + "=" * 60)
        print("Loan Application Console Menu".center(60))
        print("=" * 60)
        print("\nPlease make your selection and press ENTER:")
        print(" ")
        print("     1. Display transactions for a given zip code")
        print("     2. Display number and total values for a given type")
        print("     3. Display total number and values for branches in a given state ")
        print("     4. Check existing account details of a customer")
        print("     5. Modify existing account details of a customer")
        print("     6. Generate monthly bill for a given card number")
        print("     7. Display customer transactions between two dates")
        print("     8. Exit")
        print("=" * 60)
        choice = input("Enter your choice (1-8): ")
        if choice == '1':
            zipcode_transactions()
        elif choice == '2':
            sum_by_type()             
        elif choice == '3':
            clear_screen()
            print("\n" + "=" * 60)
            print(" Branch Report for a given state".center(60))
            print("=" * 60)
            state = input("Enter State: ")
            print("\nYou entered State: {}".format(state))
            input(nav)
        elif choice == '4':
            clear_screen()
            print("\n" + "=" * 60)
            print("View customer account details".center(60))
            print("=" * 60)
            ssn = input("Enter customer's SSN: ")
            print("\nYou entered SSN: {}".format(ssn))
            input(nav)
        elif choice == '5':
            clear_screen()
            print("\n" + "=" * 60)
            print("Modify customer account details".center(60))
            print("=" * 60)
            ssn = input("Enter customer's SSN: ")
            print("\nYou entered SSN: {}".format(ssn))
            input(nav)
        elif choice == '6':
            clear_screen()
            print("\n" + "=" * 60)
            print("Generate monthly bill for a given card number".center(60))
            print("=" * 60)
            cust_ccn = input("Enter credit card number: ")
            cust_mo =  input("Enter month as 2 digits: ")
            cust_yr =  input("Enter year as 4 digits: ")
            print("\nYou entered credit card number: {}".format(cust_ccn))
            print("\nYou entered the month as: {}".format(cust_mo))
            print("\nYou entered the year as : {}".format(cust_yr))
            input(nav)
        elif choice == '7':
            clear_screen()
            print("\n" + "=" * 60)
            print("Display transactions between two dates".center(60))
            print("=" * 60)
            ssn = input("Enter customer's SSN: ")
            dt_start = input("Enter Start date: ")
            dt_end = input("Enter End date: ")
            print("\nYou entered SSN: {}".format(ssn))
            print("\nYou entered start date: {}".format(dt_start))
            print("\nYou entered end date: {}".format(dt_end))
            input(nav)
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")

#close the cursor and connection to the database
    cursor.close()
    conn.close()

# Run the Main Menu 
if __name__ == "__main__":
    main_menu()

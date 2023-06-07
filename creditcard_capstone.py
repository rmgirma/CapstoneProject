import os
import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable

def clear_screen():  # function to clear the screen between menu change
        _ = os.system('cls')
        
conn = mysql.connector.connect(   # connection to the database
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='creditcard_capstone'
)
cursor = conn.cursor() # Create a cursor object to load data
nav = "Press Enter key to continue..." # navigation prompt
padding = 65 # length of character for padding 

# function to display transactions by zipcode for Question 2.1.1
def zipcode_transactions():
    try:  # Start of try block
        clear_screen()
        print("\n" + "=" * padding)
        print("Report By Zip Code".center(padding))
        print("=" * padding)
        zipcode = input("Enter Zip Code: ")
        month = input("Enter Month as 2 digits: ")
        year = input("Enter Year as YYYY: ")
        query = """SELECT ccard.TIMEID, cust.FIRST_NAME, cust.LAST_NAME, cust.cust_phone, cust.FULL_STREET_ADDRESS,
                cust.cust_zip, cust.CREDIT_CARD_NO, ccard.TRANSACTION_TYPE, ccard.TRANSACTION_VALUE
                FROM cdw_sapp_customer cust join cdw_sapp_credit_card ccard on ccard.CUST_SSN = cust.SSN
                where cust.CUST_ZIP =  %s and MONTH(ccard.TIMEID) = %s AND YEAR(ccard.TIMEID) = %s
                order by ccard.TIMEID desc"""
        cursor.execute(query, (zipcode, month, year))
        results = cursor.fetchall()  # to return all rows
        pretty = PrettyTable()  # create a PrettyTable object to display result in tabular manner
        pretty.field_names = ['Date', 'First Name', 'Last Name', 'Phone Number', 'Street Address', 'Zip Code', 'Credit Card Number', 'Transaction Type', 'Amount']
        for result in results:
            pretty.add_row(result)
        print(pretty)
        input(nav)
    except Exception as err:  # end of try block
        print(err)

def sum_by_type():  # display the number and total value for a given Type . Question 2.1.2
    try:
        clear_screen()
        while True:
            print("\n" + "=" * padding)
            print("Select Transaction Type".center(60))
            print("=" * padding)
            print("     1. Education")
            print("     2. Entertainment")
            print("     3. Healthcare")
            print("     4. Grocery")
            print("     5. Test")
            print("     6. Gas")
            print("     7. Bills")
            print("=" * padding)
            print("     8. Return to Main Menu")
            print("=" * padding)
            choice = input("Select Transaction Type: ")
            ttype =''
            if choice == '1':
                ttype ='Education'
            elif choice == '2':
                ttype = 'Entertainment'
            elif choice == '3':
                ttype = 'Healthcare'
            elif choice == '4':
                ttype = 'Grocery'
            elif choice == '5':
                ttype = 'Test'
            elif choice == '6':
                ttype = 'Gas'
            elif choice == '7':
                ttype = 'Bills'  
            elif choice == '8':
                print("Returning to Main MENU...")     
                break
            else:
                print("Invalid choice. Please enter a valid Transaction Type.")
            query = """SELECT TRANSACTION_TYPE,  count(TRANSACTION_TYPE) total_num, sum(TRANSACTION_VALUE) tot_amount from CDW_SAPP_CREDIT_CARD
                            group by TRANSACTION_TYPE
                            having TRANSACTION_TYPE= %s """
            cursor.execute(query, (ttype,))
            results = cursor.fetchall()  # to return all rows
            pretty = PrettyTable()  # create a PrettyTable object to display result in tabular manner
            pretty.field_names = ['Transaction Type', 'Total Number', 'Total Amount']
            for result in results:
                pretty.add_row(result)
            print(pretty)
            input(nav)
            clear_screen()
    except Exception as err:
        print(err)  
              
def branch_transactions():  # display total number and values for branches in a given state for Question 2.1.3
    try:
        clear_screen()
        print("\n" + "=" * padding)
        print("Branch Transaction Report By State".center(padding))
        print("=" * padding)
        state = input("Enter State: ")
        query = """SELECT branch.BRANCH_NAME, branch.BRANCH_CODE, count(ccard.TRANSACTION_VALUE) as cnt,  
                    sum(ccard.TRANSACTION_VALUE) as amount 
                    FROM cdw_sapp_credit_card ccard 
                    JOIN cdw_sapp_branch branch ON branch.BRANCH_CODE = ccard.BRANCH_CODE
                    WHERE branch.BRANCH_STATE = %s
                    GROUP BY branch.BRANCH_NAME, branch.BRANCH_CODE"""
        cursor.execute(query, (state,)) # parameter expects a tupple so the need for , if only 1 param is passed
        results = cursor.fetchall()  # to return all rows
        pretty = PrettyTable()  # create a PrettyTable object to display result in tabular manner
        pretty.field_names = ['Branch Name', 'Branch Code', 'Transaction Count', 'Total Amount']

        total_count = 0    # for grand total use
        total_amount = 0
        for result in results:
            pretty.add_row(result)
            total_count += result[2]  # 3rd element for total count of the results dataset
            total_amount += result[3] # 4th element for total amount
        pretty.add_row(['------------', '--', '----', '------------'])
        pretty.add_row(['Grand Total', '', total_count, total_amount])
        
        print(pretty)
        input(nav)
    except Exception as err:  
        print(err)

def check_account_details():  # Check existing account details of a customer for Question 2.2.1
    try:
        clear_screen()
        print("\n" + "=" * padding)
        print("Check Customer Account Details".center(padding))
        print("=" * padding)
        ssn = input("Enter customer's SSN: ")
        query = """SELECT * 
                   FROM cdw_sapp_customer
                   WHERE SSN = %s"""
        cursor.execute(query, (ssn,))
        result = cursor.fetchone()
        
        field_names = [fname[0] for fname in cursor.description] # getting the field names
        pretty = PrettyTable()  
        pretty.field_names = ['Field Name', 'Value']  # structure for the 2 columns table as 'Field Name' and 'Value'
        
        for field, value in zip(field_names, result): # here using the  Python zip() function to add rows to the PrettyTable object
            pretty.add_row([field, value])  # adding a row for each field-value pair
        print(pretty)
        YN = input("\nEnter Y to modify the record or any key to ignore:  ")
        if YN.upper() == 'Y':
            modify_account_details(ssn)  # call this function to modify records for Question 2.2.2
    except Exception as err:
        print(err)

def modify_account_details(ssn):  # Modify existing account details of a customer for Question 2.2.2. parameter ssn passed from above
    try:
        print("Please provide the new updates. Leave blank and hit Enter if you do not want to make changes ")
        phone_number = input("Enter new phone number: ")
        email = input("Enter new email: ")
        if phone_number or email: 
        # COALESCE() to return non null values of parameter if entered else will return the existing value and no change is recorded
            update_query = """UPDATE cdw_sapp_customer
                              SET CUST_PHONE = COALESCE(%s, CUST_PHONE),
                                  CUST_EMAIL = COALESCE(%s, CUST_EMAIL)
                              WHERE SSN = %s"""
            cursor.execute(update_query, (phone_number or None, email or None, ssn,))
            conn.commit()
            print("Customer updated successfully.")
        else:
            print("No change recorded.")
        input(nav)
    except Exception as err: 
        print(err)


def main_menu():  # Main Menu function        
    while True:
        clear_screen()
        print("\n" + "=" * padding)
        print("Loan Application Console Menu".center(60))
        print("=" * padding)
        print("\nPlease make your selection and press ENTER:")
        print(" ")
        print("     1. Display transactions for a given zip code")
        print("     2. Display number and total values for a given type")
        print("     3. Display total number and values for branches in a given state ")
        print("     4. View or Modify existing account details of a customer")
        print("     5. Generate monthly bill for a given card number")
        print("     6. Display customer transactions between two dates")
        print("     7. Exit")
        print("=" * padding)
        choice = input("Enter your choice (1-8): ")
        if choice == '1':
            zipcode_transactions()
        elif choice == '2':
            sum_by_type()             
        elif choice == '3':
            branch_transactions()
        elif choice == '4':
            check_account_details()
        elif choice == '5':
            clear_screen()
            print("\n" + "=" * padding)
            print("Generate monthly bill for a given card number".center(60))
            print("=" * padding)
            cust_ccn = input("Enter credit card number: ")
            cust_mo =  input("Enter month as 2 digits: ")
            cust_yr =  input("Enter year as 4 digits: ")
            print("\nYou entered credit card number: {}".format(cust_ccn))
            print("\nYou entered the month as: {}".format(cust_mo))
            print("\nYou entered the year as : {}".format(cust_yr))
            input(nav)
        elif choice == '6':
            clear_screen()
            print("\n" + "=" * padding)
            print("Display transactions between two dates".center(60))
            print("=" * padding)
            ssn = input("Enter customer's SSN: ")
            dt_start = input("Enter Start date: ")
            dt_end = input("Enter End date: ")
            print("\nYou entered SSN: {}".format(ssn))
            print("\nYou entered start date: {}".format(dt_start))
            print("\nYou entered end date: {}".format(dt_end))
            input(nav)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")

    cursor.close() #close the cursor and connection to the database once done
    conn.close()

# program starts here . Run the Main Menu 
main_menu()

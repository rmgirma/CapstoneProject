import os
import mysql.connector
from mysql.connector import Error
from prettytable import PrettyTable
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine  # create sqlalchemy engine as the mysql.connector did not work for Pandas
import requests 
import json
import webbrowser # for Tableau charts


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

engine = create_engine("mysql+mysqlconnector://{user}:{pw}@localhost/{db}" # sqlalchemy engine needed to work for Pandas
                       .format(user="root", pw="password", db="creditcard_capstone"))

# constant declarations:
nav = "\nPress Enter key to continue..." # used to pause the flow
padding = 75 # length of character for padding 
# df_global = pd.DataFrame()  # Initialize an empty DataFrame

def zipcode_transactions(): # function to display transactions by zipcode (2.1.1)
    try:  # Start of try block
        clear_screen()
        print("=" * padding)
        print("Report By Zip Code".center(padding))
        print("=" * padding)
        zipcode = input("Enter Zip Code: ")
        month = input("Enter Month as 2 digits: ")
        year = input("Enter Year as YYYY: ")
        query = """SELECT CONCAT(SUBSTRING(ccard.TIMEID, 5, 2), '/', SUBSTRING(ccard.TIMEID, 7, 2), '/', SUBSTRING(ccard.TIMEID, 1, 4)) AS FTIMEID,
                cust.FIRST_NAME, cust.MIDDLE_NAME, cust.LAST_NAME, cust.cust_phone, cust.FULL_STREET_ADDRESS,
                cust.cust_zip, cust.CREDIT_CARD_NO, ccard.TRANSACTION_TYPE, ccard.TRANSACTION_VALUE
                FROM cdw_sapp_customer cust join cdw_sapp_credit_card ccard on ccard.CUST_SSN = cust.SSN
                where cust.CUST_ZIP =  %s and MONTH(ccard.TIMEID) = %s AND YEAR(ccard.TIMEID) = %s
                order by ccard.TIMEID desc"""
        cursor.execute(query, (zipcode, month, year))
        results = cursor.fetchall()  # to return all rows
        pretty = PrettyTable()  # create a PrettyTable object to display result in tabular manner
        pretty.field_names = ['Date', 'First Name', 'Middle', 'Last Name', 'Phone Number', 'Street Address', 'Zip Code', 'Credit Card Number', 'Transaction-Type', 'Amount']
        for result in results:
            pretty.add_row(result)
        print(pretty)
        input(nav)
    except Exception as err:  # end of try block
        print(err)
        input(nav)

def sum_by_type():  # display the number and total value for a given Type . (2.1.2)
    try:
        clear_screen()
        while True:
            print("\n" + "=" * padding)
            print("Select Transaction Type".center(padding))
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
            query = """SELECT TRANSACTION_TYPE,  count(TRANSACTION_TYPE) total_num, ROUND(sum(TRANSACTION_VALUE),2) tot_amount from CDW_SAPP_CREDIT_CARD
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
        input(nav)  
              
def branch_transactions():  # display total number and values for branches in a given state (2.1.3)
    try:
        clear_screen()
        print("\n" + "=" * padding)
        print("Branch Transaction Report By State".center(padding))
        print("=" * padding)
        state = input("Enter State: ")
        query = """SELECT branch.BRANCH_NAME, branch.BRANCH_CODE, count(ccard.TRANSACTION_VALUE) as cnt,  
                    round(sum(ccard.TRANSACTION_VALUE),2) as amount 
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
        formated_total_amount = "{:,.2f}".format(total_amount)
        pretty.add_row(['Grand Total', '', total_count, formated_total_amount])
        print(pretty)
        
        input(nav)
    except Exception as err:  
        print(err)
        input(nav)

def view_account_details():  # Check existing account details of a customer (2.2.1)
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
        modify = input("\nEnter Y to modify the record or any key to ignore:  ")
        if modify.upper() == 'Y':
            modify_account_details(ssn)  # call this function to modify records (2.2.2)
    except Exception:
        print("SSN not found. Please Try again")
        input(nav)

def modify_account_details(ssn):  # Modify account for Question 2.2.2. parameter ssn passed from view_account_details()
    try:
        print("Please provide the new updates. Leave blank and hit Enter if you do not want to make changes ")
        first_name = input("Enter new First Name: ")
        middle_name = input("Enter new Middle Name: ")
        last_name = input("Enter new Last Name: ")
        cc_number = input("Enter new Credit Card Number: ")
        full_street_add = input("Enter new Full Street Address: ")
        city = input("Enter new City: ")
        state = input("Enter new State: ")
        country = input("Enter new Country: ")
        while True:                                             # to enforce digit only input for zip code
            zipcode = input("Enter new Zip Code: ")
            if zipcode.isdigit() or zipcode == '':
                break
            else:
                print("Invalid entry. Please enter numbers only.")
        phone_number = input("Enter new phone number: ")
        email = input("Enter new email: ")
        if first_name or middle_name or last_name or cc_number or full_street_add or city or state or country or zipcode or phone_number or email: 
        # COALESCE() to return non null values of parameter if entered, else will return the existing value and no change is recorded
            update_query = """UPDATE cdw_sapp_customer
                            SET 
                            FIRST_NAME = COALESCE(%s, FIRST_NAME),
                            MIDDLE_NAME = COALESCE(%s, MIDDLE_NAME),
                            LAST_NAME = COALESCE(%s, LAST_NAME),
                            CREDIT_CARD_NO = COALESCE(%s, CREDIT_CARD_NO),
                            FULL_STREET_ADDRESS = COALESCE(%s, FULL_STREET_ADDRESS),
                            CUST_CITY = COALESCE(%s, CUST_CITY),
                            CUST_STATE = COALESCE(%s, CUST_STATE),
                            CUST_COUNTRY = COALESCE(%s, CUST_COUNTRY),
                            CUST_ZIP = COALESCE(%s, CUST_ZIP),
                            CUST_PHONE = COALESCE(%s, CUST_PHONE),
                            CUST_EMAIL = COALESCE(%s, CUST_EMAIL),
                            LAST_UPDATED = CURRENT_TIMESTAMP
                              WHERE SSN = %s"""
            cursor.execute(update_query, (first_name or None, middle_name or None, last_name or None, cc_number or None, full_street_add or None,
                            city or None, state or None, country or None, zipcode or None, phone_number or None, email or None, ssn,))
            conn.commit()
            print("\nCustomer updated successfully.")
        else:
            print("\nNo update made")
        input(nav)
    except Exception as err: 
        print(err)
        input(nav)

def monthly_bill(): # generate monthly bill for a cc number for a given month and year (2.2.3)
    try:
        clear_screen()
        print("\n" + "=" * padding)
        print("Generate monthly bill for a given credit card number".center(padding))
        print("=" * padding)
        cust_ccn = input("\nEnter credit card number: ")
        cust_mo =  input("Enter month as 2 digits: ")
        cust_yr =  input("Enter year as 4 digits: ")
        query = """SELECT CONCAT(SUBSTRING(ccard.TIMEID, 5, 2), '/', SUBSTRING(ccard.TIMEID, 7, 2), '/', SUBSTRING(ccard.TIMEID, 1, 4)) AS FTIMEID,
                cust.FIRST_NAME, cust.LAST_NAME, ccard.TRANSACTION_TYPE, ccard.TRANSACTION_VALUE
                FROM cdw_sapp_customer cust join cdw_sapp_credit_card ccard on ccard.CUST_SSN = cust.SSN
                where cust.CREDIT_CARD_NO = %s and MONTH(ccard.TIMEID) = %s AND YEAR(ccard.TIMEID) = %s
                order by ccard.TIMEID desc"""
        cursor.execute(query, (cust_ccn, cust_mo, cust_yr))
        results = cursor.fetchall()
        pretty = PrettyTable()
        pretty.field_names = ['Date', 'First Name', 'Last Name', 'Transaction Type', 'Amount']
        total_amount = 0
        for result in results:
            pretty.add_row(result)
            total_amount += result[4] # total amount on 5th column
        print(pretty)
        print("\nTotal Monthly Bill Amount: ", total_amount)
        input(nav)
    except Exception as err:
        print(err)
        input(nav)
        
def transactions_between_dates():  # display the transactions made by a customer between two dates. (2.2.4)
    try: 
        clear_screen()
        print("\n" + "=" * padding)
        print("Display transactions between two dates".center(padding))
        print("=" * padding)
        ssn = input("Enter customer's SSN: ")
        dt_start = input("Enter Start date (YYYY-MM-DD): ")
        dt_end = input("Enter End date (YYYY-MM-DD): ")
        dt_start = dt_start.replace("-", "")  # remove the - to so that format 'YYYYMMDD' matchs the TIMEID format
        dt_end = dt_end.replace("-", "")
        query = """SELECT CONCAT(SUBSTRING(ccard.TIMEID, 5, 2), '/', SUBSTRING(ccard.TIMEID, 7, 2), '/', SUBSTRING(ccard.TIMEID, 1, 4)) AS FTIMEID, 
                cust.FIRST_NAME, cust.LAST_NAME, ccard.TRANSACTION_TYPE, ccard.TRANSACTION_VALUE
                FROM cdw_sapp_customer cust join cdw_sapp_credit_card ccard on ccard.CUST_SSN = cust.SSN
                where cust.SSN = %s and ccard.TIMEID BETWEEN %s AND %s
                order by ccard.TIMEID desc"""
        cursor.execute(query, (ssn, dt_start, dt_end))
        results = cursor.fetchall()
        pretty = PrettyTable()
        pretty.field_names = ['Date', 'First Name', 'Last Name', 'Transaction Type', 'Amount']
        for result in results:
            pretty.add_row(result)
        print(pretty)
        input(nav)
    except Exception as err:
        print(err)
        input(nav)
 
def plot_transaction_type(): # Data Analysis and Visualization (3.3.1)
    try:
        query = "SELECT TRANSACTION_TYPE FROM CDW_SAPP_CREDIT_CARD"
        df = pd.read_sql_query(query, engine)
        counts = df['TRANSACTION_TYPE'].value_counts()  # Count the transaction types
        plt.figure(figsize=(15, 6)) 
        counts.plot(kind='line', marker='o') #line plot of the transaction types
        plt.title('Transaction Type Counts')
        plt.xlabel('Transaction Type')
        plt.ylabel('Transaction Count')
        plt.show()
    except Exception as err: 
        print(err)
        input(nav)

# if conn.is_connected():  # debugging
#     print("Connection is open")
# else:
#     print("Connection is not open")
# input(nav)

def plot_customer_states(): # Find and plot which state has a high number of customers (3.3.2)
    # input("start")
    try:
        # if conn.is_connected():
            query = """SELECT cust.CUST_STATE, COUNT(cust.SSN) as NUM_CUSTOMERS
                FROM cdw_sapp_customer cust
                GROUP BY cust.CUST_STATE ORDER BY cust.CUST_STATE"""
            df = pd.read_sql_query(query, engine)
            plt.figure(figsize=(15, 6))
            counts = df.set_index('CUST_STATE')['NUM_CUSTOMERS']
            counts.plot(kind='bar', color='green')
            plt.xlabel('State')
            plt.ylabel('Number of Customers')
            plt.title('Number of Customers Per State')
            plt.show()
        # else:
        #     print("Connection is not open")
        #     input(nav)
    except Exception as err:
        print(err)
        input(nav)

def plot_top_customers(): # sum of all transactions for the top 10 customers (3.3.3)
    try:
        # if conn.is_connected():
            query = """
                SELECT ccard.CUST_SSN, SUM(ccard.TRANSACTION_VALUE) as TOTAL_VALUE
                FROM cdw_sapp_credit_card ccard
                GROUP BY ccard.CUST_SSN
                ORDER BY TOTAL_VALUE DESC
                LIMIT 10"""
            df = pd.read_sql_query(query, engine)
            counts = df.set_index('CUST_SSN')['TOTAL_VALUE']
            plt.figure(figsize=(15, 6))
            counts.plot(kind='barh')
            plt.ylabel('Customer')
            plt.xlabel('Total Transaction Value')
            plt.title('Top 10 Customers by Total Transaction Value')
            plt.xlim(left=5100, right=5700)  # in order to make the difference visible 
            plt.show()
        # else:
            # print("Connection not avaialble")
    except Exception as err:
        print(err)
        input(nav)

def load_loan_data(): #  Loan Application Data API (4.4.1) (4.4.2) & (4.4.3)
    try:
        url = 'https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json'
        response = requests.get(url)
        print("Status Code: ", response.status_code)
        input(nav)                          #  4.2
        if response.status_code == 200:
            data = json.loads(response.text)
            df = pd.DataFrame(data)
            df.to_sql('cdw_sapp_loan_application', con=engine, if_exists='append', index=False)  # appends record into the loan table. Drop table manually
            print("Loan application data loaded successfully.")
            input(nav)
        else:
            print("problem:", response.status_code)
            input(nav)
    except Exception as err:
        print(err)
        input(nav)
        
def plot_self_employed_approval(): # to find and plot the percentage of applications approved for self-employed applicants. (5.5.1)

    try:
        df = pd.read_sql_table('cdw_sapp_loan_application', engine)  # Load data from database 
        self_employed_df = df[df['Self_Employed'] == 'Yes']
        total_applications = len(self_employed_df)
        approved_applications = len(self_employed_df[self_employed_df['Application_Status'] == 'Y'])
        approval_rate = approved_applications / total_applications
        notapproval_rate = 1 - approval_rate  # Disapproval rate is the remainder
        
        plt.figure(figsize=(10, 6))
        plt.pie([approval_rate, notapproval_rate], labels=['Approved', 'Not Approved'], 
                autopct='%1.1f%%', colors=['green', 'grey'], startangle=90)
        plt.title('Percentage of Applications Approved for Self-Employed Applicants')
        plt.show()
    except Exception as err:
        print(err)
        input(nav)

def plot_rejection_of_married_male(): # to find the percentage of rejection for married male applicants. (5.5.2)
    try:
        df = pd.read_sql_table('cdw_sapp_loan_application', engine)  # Load data from database 
        married_male_df = df[(df['Gender'] == 'Male') & (df['Married'] == 'Yes')]
        total_married_male = len(married_male_df)
        rejected_applications = len(married_male_df[married_male_df['Application_Status'] == 'N'])
        
        rejection_rate = rejected_applications / total_married_male
        acceptance_rate = 1 - rejection_rate  
        plt.figure(figsize=(10, 6))
        plt.pie([rejection_rate, acceptance_rate], labels=['Rejected', 'Accepted'], 
            autopct='%.2f%%', colors=['red', 'green'], startangle=90)
        plt.title('Percentage of Applications Rejected for Married Male Applicants')
        print("\nTotal Married Male: ", total_married_male)
        print("Total Rejections  : ", rejected_applications)
        print("Rejection Rate %  : ", rejection_rate*100)
        input(nav)
        plt.show()
    except Exception as err:
        print(err)
        input(nav)
 
def show_tableau():
    try:
        clear_screen()
        while True:
            print("\n" + "=" * padding)
            print("Select Tableau Visualization".center(padding))
            print("=" * padding)
            print("     1. Number and Amount of Customer's Transactions by State")
            print("     2. Total Transaction Amount by Type")
            print("     3. Heatmap Number of Customer by State")
            print("     4. Dashboard - Example")
            print("=" * padding)
            print("     5. Return to Main Menu")
            print("=" * padding)
            choice = input("Select your choice: ")
            sheet =''
            if choice == "1":
                sheet ="TransByState"
            elif choice == "2":
                sheet = "TransactionByType"
            elif choice == "3":
                sheet = "CustomerByState"
            elif choice == "4":
                sheet = "ExamleBankDashboard"
            elif choice == "5":
                print("Returning to Main MENU...")     
                break
            else:
                print("Invalid choice. Please choose between 1 and 5.")   
            base_url = "https://public.tableau.com/views/"
            workbook = "ExampleBankTransactionsbyState"
            url = base_url + workbook + "/" + sheet
            webbrowser.open_new_tab(url)
            clear_screen()
    except Exception as err:
        print(err)
        input(nav)
      
def main_menu():  # Main Menu function        
    while True:
        clear_screen()
        print("\n" + "=" * padding)
        print("Application Console Menu".center(padding))
        print("=" * padding)
        print("\nPlease make your selection and press ENTER:")
        print(" ")
        print("     1. Display transactions for a given zip code")
        print("     2. Display number and total values for a given type")
        print("     3. Display total number and values for branches in a given state ")
        print("     4. View or Modify existing account details of a customer")
        print("     5. Generate monthly bill for a given card number")
        print("     6. Display customer transactions between two dates")
        print("     7. Data Visualization - Transaction count by Type")
        print("     8. Data Visualization - Number of Customer by State")
        print("     9. Data Visualization - Top Ten Customeers by Transaction Amount")
        print("     10. Load Loan Application Dataset")
        print("     11. Data Visualization - Approved Self-Employed Applicants")
        print("     12. Data Visualization - Rejected Married Male Applicants")
        print("     13. Data Visualization - Top Three Months Largest Transactions")
        print("     14. Data Visualization - Highest Healthcare Transaction Branch")
        print("     15. Tableau Data Visualizations")
        print("     16. Exit")
        print("=" * padding)
        choice = input("Enter your choice (1-16): ")
        if choice == '1':
            zipcode_transactions()
        elif choice == '2':
            sum_by_type()             
        elif choice == '3':
            branch_transactions()
        elif choice == '4':
            view_account_details()
        elif choice == '5':
           monthly_bill()
        elif choice == '6':
            transactions_between_dates()
        elif choice == '7':
            plot_transaction_type()
        elif choice == '8':
            plot_customer_states()
        elif choice == '9':
            plot_top_customers()
        elif choice == '10':
            load_loan_data()
        elif choice == '11':
            plot_self_employed_approval()
        elif choice == '12':
            plot_rejection_of_married_male()
        elif choice == '13':
            clear_screen()
        elif choice == '14':
            clear_screen()
        elif choice == '15':
            show_tableau()
        elif choice == '16':
            print("Exiting...")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 16.")   # end of menu function
            
    cursor.close() #close the cursor and connection to the database once done
    conn.close()
# program starts here . Run the Main Menu 
main_menu()

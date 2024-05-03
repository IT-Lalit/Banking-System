import mysql.connector
import random
from datetime import datetime
from tabulate import tabulate

class DatabaseHandler:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kumar@111",
            database="mybank"
        )
        self.cursor = self.db.cursor()

#### Bank Information Table Creation-----------------------------------------------------------------
    def create_my_bank_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS account_info (
                account_number VARCHAR(11) PRIMARY KEY,
                aadhaar_number VARCHAR(12) NOT NULL,
                name VARCHAR(255) NOT NULL,
                dob DATE NOT NULL,
                contact VARCHAR(10) NOT NULL,
                email VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                kyc varchar(255)
            )
            """
            self.cursor.execute(query)
            print("Table 'account_info' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

        try:
            query = """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id VARCHAR(250) PRIMARY KEY,
                account_number VARCHAR(11) NOT NULL,
                transaction_type VARCHAR(10) NOT NULL,
                transaction_amount DECIMAL(10, 2) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                transaction_date DATETIME NOT NULL,
                FOREIGN KEY (account_number) REFERENCES account_info(account_number)
            )
            """
            self.cursor.execute(query)
            print("Table 'transactions' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def allAccountsDetails(self):
        try:
            query = 'SELECT * FROM account_info'
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            # Create a PrettyTable instance for displaying results
            tableheading = ["Account Number", "Name", "Aadhaar Number", "Date of Birth", "Mobile Number", "Email", "Address", "Balance", "KYC"]
            tableData = []
            for result in results:
                account_number = result[0]
                aadhaar_number = result[1]
                name = result[2]
                dob = result[3]
                contact = result[4]
                email = result[5]
                address = result[6]
                balance = result[7]
                kyc = result[8]
                tableData.append([account_number, name, aadhaar_number, dob, contact, email, address, balance, kyc])
            return tabulate(tableData, headers=tableheading, tablefmt='fancy_grid')
        except Exception as e:
            print(f"Error featching details: {e}")    

#### New Account Creation-------------------------------------------------------------------
    def insert_account_details(self, aadhaar, name, dob, contact, email, address, balance):
        try:
            # Generate an account number
            account_number = self.generate_account_number()

            # Convert string date to a datetime object
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

            kyc = 'no'

            # Insert data into the account_info table
            query = "INSERT INTO account_info (account_number, aadhaar_number,  name, dob, contact, email, address, balance, kyc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (account_number, aadhaar, name, dob_date, contact, email, address, balance, kyc)
            self.cursor.execute(query, values)

            # Insert an initial deposit transaction into the transactions table
            self.insert_transaction(account_number, 'Deposit', balance, balance)

            self.db.commit()

            return f"Account Open Successfully\nAccount number >>> {account_number}"
        except Exception as e:
            return f"Error saving account details\n{e}"


    def generate_account_number(self):
        # Generate a 6-digit random number
        random_part = ''.join(str(random.randint(0, 9)) for _ in range(5))

        # Concatenate with the fixed prefix
        account_number = '208020' + random_part

        return account_number


#### Account Deletion-------------------------------------------------------------------
    def delete_account(self, account_number, aadhaar, name, dob, mobile):
        try:
            # Convert string date to a datetime object
            dob_date = datetime.strptime(dob, "%Y-%m-%d").date()

            # Delete related records in the transactions table
            query_transactions = "DELETE FROM transactions WHERE account_number = %s"
            self.cursor.execute(query_transactions, (account_number,))

            # Delete data from the account_info table
            query_account_info = "DELETE FROM account_info WHERE account_number = %s AND aadhaar_number = %s AND name = %s AND dob = %s AND contact = %s"
            values = (account_number, aadhaar, name, dob_date, mobile)
            self.cursor.execute(query_account_info, values)

            self.db.commit()

            return f"\nAccount {account_number} Successfully Deleted\n"
        except Exception as e:
            print(f"Error deleting account: {e}")




#### KYC ----------------------------------------------------------------------------------------------

    def checkKYC(self, account_number):
        try:
            # Fetch details from the database based on account number
            self.cursor.execute('SELECT * FROM account_info WHERE account_number = %s', (account_number,))
            account_details = self.cursor.fetchone()

            if account_details:
                # Check if KYC is completed
                if account_details[8] == 'yes':
##                    print("KYC is already completed.")
                    accountDetails = self.get_details(account_number)
                    returnValue = ("KYC is already completed\n",accountDetails)
                    return returnValue
                else:
##                    print("KYC is pending")
                    self.get_details(account_number)
                    returnValue = ("KYC is pending\n",'no')
                    return returnValue
            else:
##                print("Account not found.")
                returnValue = ("Account not found\n","")
                return returnValue
        except Exception as e:
            print(f"Error during KYC: {e}")


    def kyc(self, account_number, aadhaar_number_input, name_input, dob_input):
        # Fetch details from the database based on account number
        self.cursor.execute('SELECT * FROM account_info WHERE account_number = %s', (account_number,))
        account_details = self.cursor.fetchone()
        # Validate date format
        try:
            datetime.strptime(dob_input, "%Y-%m-%d")
        except ValueError:
##            print("Invalid date format. Please enter the date in yyyy-mm-dd format.")
            returnValue = ("Invalid date format. Please enter the date in yyyy-mm-dd format.\n",'')
            return returnValue

        # Clean up and standardize inputs
        aadhaar_number_db = account_details[1].strip()
        name_db = account_details[2].strip()
        dob_db = str(account_details[3]).strip()

        if (aadhaar_number_input == aadhaar_number_db and
                name_input == name_db and
                dob_input == dob_db):
            self.update_kyc_status(account_number)
            returnValue = ("KYC updated successfully.\n",'')
            return returnValue
        else:
            returnValue = ("Aadhaar verification failed. KYC not updated.\n",'')
            return returnValue


    def update_kyc_status(self, account_number):
        try:
            # Update KYC status in the database
            query = "UPDATE account_info SET kyc = 'yes' WHERE account_number = %s"
            self.cursor.execute(query, (account_number,))
            self.db.commit()
        except Exception as e:
            print(f"Error updating KYC status: {e}")


#### Get Account Holder Details------------------------------------------------------------------------

    def search_account(self, account_number):
        # Fetch data from the database based on account_number
        self.cursor.execute('SELECT * FROM account_info WHERE account_number = %s', (account_number,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return ("Account not found.")


    def get_details(self, account_number):
        # Fetch data from the database based on account_number
        self.cursor.execute('SELECT * FROM account_info WHERE account_number = %s', (account_number,))
        result = self.cursor.fetchone()

        if result:
            
##            data = [["Name", result[2]],
##            ["Account Number", result[0]],
##            ["Aadhaar Number", result[1]],
##            ["Date of Birth", result[3]],
##            ["Mobile Number", result[4]],
##            ["Email Id", result[5]],
##            ["Address", result[6]],
##            ["Total Balance", result[7]],
##            ["KYC Status", result[8]]]
##            return tabulate(data,tablefmt='fancy_grid')
            
            return result
        else:
##            return "Account not found"
            return 0


    def get_balance(self, account_number):
        # Fetch balance from the database based on account_number
        self.cursor.execute('SELECT balance FROM account_info WHERE account_number = %s', (account_number,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return 0



#### Deposit and Withdraw---------------------------------------------------------------------------------
            
    def deposit(self, account_number, amount):
        try:
            # Convert the amount to float
            amount = float(amount)

            # Fetch the existing balance
            current_balance = self.get_balance(account_number)

            if current_balance is not None:
                # Update the balance with the deposited amount
                new_balance = float(current_balance) + amount

                # Update the balance in the database
                query = "UPDATE account_info SET balance = %s WHERE account_number = %s"
                values = (new_balance, account_number)
                self.cursor.execute(query, values)
                self.db.commit()

                # Insert a deposit transaction into the transactions table
                self.insert_transaction(account_number, 'Deposit', amount, new_balance)
                line = '-' *50
                lineA4 = f"{('-' *17)}+{('-'*32)}"

                returnValue = (f"+{lineA4}+\n| {'Account Number':<15} | {account_number:<30} |\n+{lineA4}+\n| {'Balance':<15} | {current_balance:<30} |\n+{lineA4}+\n| {'Deposited':<15} | {amount:<30} |\n+{lineA4}+\n| {'New balance':<15} | {new_balance:<30} |\n+{line}+\n")
                return returnValue

            else:
                returnValue = "Account not found"
                return returnValue
        except Exception as e:
            print(f"Error depositing amount: {e}")

    def withdraw(self, account_number, amount):
        try:
            # Convert the amount to float
            amount = float(amount)

            # Fetch the existing balance
            current_balance = self.get_balance(account_number)

            if current_balance is not None:
                # Check if there is sufficient balance
                if current_balance >= amount:
                    # Update the balance with the withdrawn amount
                    new_balance = float(current_balance) - amount

                    # Update the balance in the database
                    query = "UPDATE account_info SET balance = %s WHERE account_number = %s"
                    values = (new_balance, account_number)
                    self.cursor.execute(query, values)
                    self.db.commit()

                    # Insert a withdrawal transaction into the transactions table
                    self.insert_transaction(account_number, 'Withdrawal', amount, new_balance)
                    line = '-' *50
                    lineA4 = f"{('-' *17)}+{('-'*32)}"

                    returnValue = (f"+{lineA4}+\n| {'Account Number':<15} | {account_number:<30} |\n+{lineA4}+\n| {'Balance':<15} | {current_balance:<30} |\n+{lineA4}+\n| {'Deposited':<15} | {amount:<30} |\n+{lineA4}+\n| {'New balance':<15} | {new_balance:<30} |\n+{line}+\n")
                    return returnValue
                else:
                    resultValue = "Insufficient balance."
                    return resultValue
            else:
                returnValue = "Account not found"
                return returnValue
        except Exception as e:
            print(f"Error withdrawing amount: {e}")
            return
                

#### Transactions History----------------------------------------------------------------------------------
    def generate_transaction_id(self, account_number):
            # Generate a 6-digit random number
            random_part = ''.join(str(random.randint(0, 9)) for _ in range(5))

            # Concatenate with the fixed prefix
            transaction_id = account_number[6:] + random_part

            return transaction_id

    def insert_transaction(self, account_number, transaction_type, amount, balance):
        transaction_id = self.generate_transaction_id(account_number)
       
        try:
            # Insert a transaction into the transactions table
            query = "INSERT INTO transactions (transaction_id, account_number, transaction_type, transaction_amount, balance, transaction_date) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (transaction_id, account_number, transaction_type, amount, balance, datetime.now())
            self.cursor.execute(query, values)
            self.db.commit()
        except Exception as e:
            print(f"Error saving transaction details: {e}")

    def get_transaction_history(self, account_number):
        try:
            # Fetch transaction history from the transactions table based on account_number
            query = 'SELECT * FROM transactions WHERE account_number = %s ORDER BY transaction_date DESC'
            self.cursor.execute(query, (account_number,))

            results = self.cursor.fetchall()

            if results:
                tableHeading = ["Transaction ID", "Transaction Date", "Transaction Type", "Transaction Amount", "Balance"]
                tableData = []
                for result in results:
                    transaction_id = result[0]
                    transaction_type = result[2]
                    amount = result[3]
                    balance = result[4]
                    transaction_date = result[5]
                    symbol = '+' if transaction_type == 'Deposit' else '-'
                    amt = symbol + str(amount)
                    
                    tableData.append([transaction_id, transaction_date, transaction_type, amt, balance])
                    
##                return tabulate(tableData, headers=tableHeading, tablefmt="fancy_grid")
                return results

            else:
                returnValue = "No transaction history found."
        except Exception as e:
            print(f"Error fetching transaction history: {e}")



# Example usage:
if __name__ == "__main__":
    db_handler = DatabaseHandler()
    account_number = '20802080444'
    aadhaar="214785698547"
    name="Kumar Lalit"
    dob="2000-10-09"
    deposit_amount = 16.27
    withdrawal_amount = 100.00

##    db_handler.create_my_bank_table()
    
##    allAccount = db_handler.allAccountsDetails()
##    print(f"All Account Details\n{allAccount}")

##    accountDetails = db_handler.get_details(account_number)
##    print(f"Account Details\n{accountDetails}")

##    transactionHistory = db_handler.get_transaction_history(account_number)
##    print("Transaction History")
##    print(transactionHistory)

    openAccount = db_handler.insert_account_details(
        aadhaar="123456789012",
        name="John Doe",
        dob="1990-01-01",
        contact="1234567890",
        email="john.doe@example.com",
        address="123 Main Street",
        balance=1000.00
    )
    print(openAccount)




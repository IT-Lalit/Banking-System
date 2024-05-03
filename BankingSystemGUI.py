import tkinter as tk
from tkinter import ttk
from tabulate import tabulate
from BankingDatabase import DatabaseHandler

class CustomLayout(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db_handler = DatabaseHandler()


        # Main window settings
        self.title("Banking System")
        self.geometry("800x600")

        # Header
        header = tk.Frame(self, bg="lightblue", height=50)
        header.pack(side="top", fill="x", padx=10, pady=10)
        header_label = tk.Label(header, text="My Bank", font=("Monaco", 16), bg="lightblue")
        header_label.pack(pady=10)

        # Navbar
        navbar = tk.Frame(self, bg="lightgrey", height=30)
        navbar.pack(side="top", fill="x", padx=10, pady=10)

        # Buttons in Navbar
        buttons = ["Home", "Open Account", "Deposit", "Withdraw", "Mini Statement", "KYC"]
        for btn_text in buttons:
            button = tk.Button(navbar, text=btn_text, padx=10, pady=5, command=lambda text=btn_text: self.perform_action(text))
            button.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Main Content Area
        self.content_area = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        self.content_area.pack(side="top", fill="both", expand=True)

        self.show_home_content()

        # Footer
        footer = tk.Frame(self, bg="lightblue", height=30)
        footer.pack(side="bottom", fill="x", padx=10, pady=10)
        footer_label = tk.Label(footer, text="© 2024 My Bank. All rights reserved.", font=("Monaco", 10), bg="lightblue")
        footer_label.pack()


##  Button Function calling
    def perform_action(self, action):
        # Clear previous content from content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Placeholder functions for button actions
        if action == "Home":
            self.show_home_content()
        elif action == "Open Account":
            self.open_account()
        elif action == "Deposit":
            self.deposit()
        elif action == "Withdraw":
            self.withdraw()
        elif action == "Mini Statement":
            self.show_mini_statement()
        elif action == "KYC":
            self.perform_kyc()

##    Button Function

    def show_home_content(self):
        label = tk.Label(self.content_area, text="Welcome to My Bank", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=20, pady=80)
        self.content.pack(side="left", fill="y", expand=True)
        

        ac_label = tk.Label(self.content, text="Account Number", font=("Helvetica", 14))
        ac_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ac_entry = tk.Entry(self.content,width=25, font='20')
        ac_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        view_details_btn = tk.Button(self.content, width=25, font='5', text="View details", bg='lightblue', command=lambda: self.view_details(ac_entry.get()))
        view_details_btn.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        check_balance_btn = tk.Button(self.content, width=25, font='5', text="Check Balance", bg='lightblue', command=lambda: self.check_balance(ac_entry.get()))
        check_balance_btn.grid(row=3, column=0, padx=5, pady=5, sticky="w")


    def view_details(self, account_number):
        if account_number != '':
            result = self.db_handler.get_details(account_number)

            if result:
                # Clear previous content
                if hasattr(self, 'contentD'):
                    self.contentD.destroy()

                if hasattr(self, 'content'):
                    self.content.destroy()

                data = [
                    ["Name", result[2]],
                    ["Account Number", result[0]],
                    ["Aadhaar Number", result[1]],
                    ["Date of Birth", result[3]],
                    ["Mobile Number", result[4]],
                    ["Email Id", result[5]],
                    ["Address", result[6]],
                    ["Total Balance", result[7]],
                    ["KYC Status", result[8]]
                ]

                self.contentD = tk.Frame(self.content_area, bg="#f0f0f0", padx=20, pady=10)
                self.contentD.pack(side="right", fill="y", expand=True)

                tableName = tk.Label(self.contentD, text="Account Information", pady=10, font=("Helvetica", 16, "bold"), fg="green", bg="#f0f0f0")
                tableName.pack()

                style = ttk.Style()
                style.configure("Treeview", font=("Helvetica", 12), rowheight=25)

                tree = ttk.Treeview(self.contentD, columns=("Attribute", "Value"), show="", style="Treeview")
                tree.heading("Attribute", text="Attribute", anchor=tk.CENTER)
                tree.heading("Value", text="Value", anchor=tk.CENTER)

                for item in data:
                    tree.insert("", tk.END, values=(item[0], item[1]))

                tree.pack(pady=10)

            else:
                info_label = tk.Label(self.content, text="Account not found", font=("Helvetica", 14),fg='red')
                info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
        else:            
            info_label = tk.Label(self.content, text="Please fill all fields", font=("Helvetica", 14),fg='red')
            info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
    
            

    def check_balance(self, account_number):
        if account_number != '':

            result = self.db_handler.get_details(account_number)
                        
            if result != 0:

                # Clear previous content
                if hasattr(self, 'contentD'):
                    self.contentD.destroy()

                if hasattr(self, 'content'):
                    self.content.destroy()
                
                data = [
                    ["Account Number", result[0]],
                    ["Name", result[2]],
                    ["Total Balance", result[7]],
                ]

                self.contentD = tk.Frame(self.content_area, bg="#f0f0f0", padx=20, pady=10)
                self.contentD.pack(side="right", fill="y", expand=True)

                tableName = tk.Label(self.contentD, text="Balance Information", pady=10, font=("Helvetica", 16, "bold"), fg="green", bg="#f0f0f0")
                tableName.pack()

                style = ttk.Style()
                style.configure("Treeview", font=("Helvetica", 12), rowheight=25)

                tree = ttk.Treeview(self.contentD, columns=("Attribute", "Value"), show="", style="Treeview")
                tree.heading("Attribute", text="Attribute", anchor=tk.CENTER)
                tree.heading("Value", text="Value", anchor=tk.CENTER)

                for item in data:
                    tree.insert("", tk.END, values=(item[0], item[1]))

                tree.pack(pady=10)
                
            else:
                info_label = tk.Label(self.content, text="Account not found", font=("Helvetica", 14),fg='red')
                info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
        else:            
            info_label = tk.Label(self.content, text="Please fill all fields", font=("Helvetica", 14),fg='red')
            info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
    
            

    def open_account(self):
        label = tk.Label(self.content_area, text="Open new account", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=10, pady=50)
        self.content.pack(side="top", fill="y", expand=True)
        
        # Labels and Entry Fields for account opening
        label_aadhaar = tk.Label(self.content, text="Aadhaar Number:", font=("Helvetica", 12))
        label_aadhaar.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        entry_aadhaar = tk.Entry(self.content, font=("Helvetica", 12))
        entry_aadhaar.grid(row=0, column=1, padx=5, pady=5)
        
        label_name = tk.Label(self.content, text="Full Name:", font=("Helvetica", 12))
        label_name.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_name = tk.Entry(self.content, font=("Helvetica", 12))
        entry_name.grid(row=1, column=1, padx=5, pady=5)

        label_dob = tk.Label(self.content, text="Date of Birth:", font=("Helvetica", 12))
        label_dob.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        entry_dob = tk.Entry(self.content, font=("Helvetica", 12))
        entry_dob.grid(row=2, column=1, padx=5, pady=5)

        # Set a default value or placeholder for the date format
        entry_dob.insert(0, "YYYY-MM-DD")

        # Event handler to show the date format if the entry is empty
        def show_placeholder():
            if not entry_dob.get():
                entry_dob.delete(0, tk.END)
                entry_dob.insert(0, "YYYY-MM-DD")

        # Event handlers to handle focus events
        def clear_placeholder(event):
            if entry_dob.get() == "YYYY-MM-DD":
                entry_dob.delete(0, tk.END)

        def restore_placeholder(event):
            show_placeholder()

        # Bind the event handlers to the entry widget
        entry_dob.bind("<FocusIn>", clear_placeholder)
        entry_dob.bind("<FocusOut>", restore_placeholder)

        # Set up an event to show the placeholder initially
        entry_dob.after(100, show_placeholder)
        

        label_contact = tk.Label(self.content, text="Contact Number:", font=("Helvetica", 12))
        label_contact.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        entry_contact = tk.Entry(self.content, font=("Helvetica", 12))
        entry_contact.grid(row=3, column=1, padx=5, pady=5)

        label_email = tk.Label(self.content, text="Email:", font=("Helvetica", 12))
        label_email.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        entry_email = tk.Entry(self.content, font=("Helvetica", 12))
        entry_email.grid(row=4, column=1, padx=5, pady=5)

        label_address = tk.Label(self.content, text="Address:", font=("Helvetica", 12))
        label_address.grid(row=5, column=0, padx=5, pady=5, sticky="e")

        entry_address = tk.Entry(self.content, font=("Helvetica", 12))
        entry_address.grid(row=5, column=1, padx=5, pady=5)

        label_balance = tk.Label(self.content, text="Initial Balance:", font=("Helvetica", 12))
        label_balance.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        entry_balance = tk.Entry(self.content, font=("Helvetica", 12))
        entry_balance.grid(row=6, column=1, padx=5, pady=5)

        # Button to submit the account opening details
        submit_button = tk.Button(self.content, text="Submit", width=30, font='5', bg='lightblue', command=lambda: self.submit_account_details(
            entry_aadhaar.get(), entry_name.get(), entry_dob.get(), entry_contact.get(), entry_email.get(), entry_address.get(), entry_balance.get()))
        submit_button.grid(row=7, columnspan=2, pady=10)
        
    def submit_account_details(self,aadhaar, name, dob, contact, email, address, balance):
        if aadhaar != '' and name != '' and dob != '' and contact != '' and email != '' and address != '' and email != '':
            
            account = self.db_handler.insert_account_details(aadhaar, name, dob, contact, email, address, balance)
            
            if hasattr(self, 'info'):
                self.info.destroy()
            self.info = tk.Label(self.content, text=f"{account}", font=("Helvetica", 14), fg='green')
            self.info.grid(row=8, columnspan=2, padx=5, pady=5)
        else:
            if hasattr(self, 'info'):
                self.info.destroy()
            self.info = tk.Label(self.content, text="Please fill all fields", font=("Helvetica", 14), fg='red')
            self.info.grid(row=8, columnspan=2, padx=5, pady=5)
            

    def deposit(self):
        label = tk.Label(self.content_area, text="Deposit funds into account", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=10, pady=80)
        self.content.pack(side="top", fill="y", expand=True)

        ac_label = tk.Label(self.content, text="Account Number", font=("Helvetica", 14))
        ac_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ac_entry = tk.Entry(self.content, width=25, font='20')
        ac_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        amt_label = tk.Label(self.content, text="Amount", font=("Helvetica", 14))
        amt_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        amt_entry = tk.Entry(self.content, width=25, font='20')
        amt_entry.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        deposit_btn = tk.Button(self.content, width=25, font='5', text="Deposit", bg='lightblue', command=lambda: self.deposit_amount(ac_entry.get(), amt_entry.get()))
        deposit_btn.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def deposit_amount(self, account_number, amount):
        if account_number and amount:
            # Call the method from DatabaseHandler to handle deposit
            self.db_handler.deposit(account_number, amount)
            print(f"Deposited {amount} into Account Number {account_number}")
        else:
            print("Please fill all fields")





    def withdraw(self):
        label = tk.Label(self.content_area, text="Withdraw funds from account", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=10, pady=80)
        self.content.pack(side="top", fill="y", expand=True)

        ac_label = tk.Label(self.content, text="Account Number", font=("Helvetica", 14))
        ac_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ac_entry = tk.Entry(self.content, width=25, font='20')
        ac_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        amt_label = tk.Label(self.content, text="Amount", font=("Helvetica", 14))
        amt_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        amt_entry = tk.Entry(self.content, width=25, font='20')
        amt_entry.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        withdraw_btn = tk.Button(self.content, width=25, font='5', text="Withdraw", bg='lightblue', command=lambda: self.withdraw_amount(ac_entry.get(), amt_entry.get()))
        withdraw_btn.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def withdraw_amount(self, account_number, amount):
        if account_number and amount:
            # Call the method from DatabaseHandler to handle withdrawal
            self.db_handler.withdraw(account_number, amount)
            print(f"Withdrew {amount} from Account Number {account_number}")
        else:
            print("Please fill all fields")

            

    def show_mini_statement(self):
        label = tk.Label(self.content_area, text="Mini Statement", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=10, pady=80)
        self.content.pack(side="top", fill="y", expand=True)

        ac_label = tk.Label(self.content, text="Account Number", font=("Helvetica", 14))
        ac_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ac_entry = tk.Entry(self.content, width=25, font='20')
        ac_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        miniStmt_btn = tk.Button(self.content, width=25, font='5', text="Mini Statement", bg='lightblue', command=lambda: self.show_mini_statement_details(ac_entry.get()))
        miniStmt_btn.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    def show_mini_statement_details(self, account_number):
        if account_number != '':
            # Call the method from DatabaseHandler to get mini statement details
            mini_statement = self.db_handler.get_transaction_history(account_number)

            # Clear previous content
            if hasattr(self, 'contentD'):
                self.contentD.destroy()

            if hasattr(self, 'content'):
                self.content.destroy()

            if mini_statement:
                self.contentD = tk.Frame(self.content_area, bg="#f0f0f0", padx=20, pady=10)
                self.contentD.pack(side="right", fill="y", expand=True)

                tableName = tk.Label(self.contentD, text="Mini Statement", pady=10, font=("Helvetica", 16, "bold"), fg="green", bg="#f0f0f0")
                tableName.pack()

                style = ttk.Style()
                style.configure("Treeview", font=("Helvetica", 12), rowheight=25)

                tree = ttk.Treeview(self.contentD, columns=("Date", "Transaction Type", "Amount"), show="", style="Treeview")
                tree.heading("Date", text="Date", anchor=tk.CENTER)
                tree.heading("Transaction Type", text="Transaction Type", anchor=tk.CENTER)
                tree.heading("Amount", text="Amount", anchor=tk.CENTER)

                for transaction in mini_statement:
                    tree.insert("", tk.END, values=(transaction["date"], transaction["transaction_type"], transaction["amount"]))

                tree.pack(pady=10)

            else:
                info_label = tk.Label(self.content, text="No transactions found for the account", font=("Helvetica", 14), fg='red')
                info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")
        else:            
            info_label = tk.Label(self.content, text="Please fill all fields", font=("Helvetica", 14), fg='red')
            info_label.grid(row=4, column=0, padx=5, pady=5, sticky="n")




    def perform_kyc(self):
        label = tk.Label(self.content_area, text="Update ", font=("Helvetica", 14))
        label.pack()

        self.content = tk.Frame(self.content_area, bg="#f0f0f0", padx=10, pady=50)
        self.content.pack(side="top", fill="y", expand=True)
        
        
        # Labels and Entry Fields for account opening
        label_account = tk.Label(self.content, text="Account Number:", font=("Helvetica", 12))
        label_account.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        entry_account = tk.Entry(self.content, font=("Helvetica", 12))
        entry_account.grid(row=0, column=1, padx=5, pady=5)
        
        label_aadhaar = tk.Label(self.content, text="Aadhaar Number:", font=("Helvetica", 12))
        label_aadhaar.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        entry_aadhaar = tk.Entry(self.content, font=("Helvetica", 12))
        entry_aadhaar.grid(row=1, column=1, padx=5, pady=5)
        
        label_name = tk.Label(self.content, text="Full Name:", font=("Helvetica", 12))
        label_name.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        entry_name = tk.Entry(self.content, font=("Helvetica", 12))
        entry_name.grid(row=2, column=1, padx=5, pady=5)

        label_dob = tk.Label(self.content, text="Date of Birth:", font=("Helvetica", 12))
        label_dob.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        entry_dob = tk.Entry(self.content, font=("Helvetica", 12))
        entry_dob.grid(row=3, column=1, padx=5, pady=5)

        label_contact = tk.Label(self.content, text="Contact Number:", font=("Helvetica", 12))
        label_contact.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        entry_contact = tk.Entry(self.content, font=("Helvetica", 12))
        entry_contact.grid(row=4, column=1, padx=5, pady=5)

        # Button to submit the account opening details
        submit_button = tk.Button(self.content, text="Submit", width=30, font='5', bg='lightblue', command=lambda: self.submit_account_kyc(
            entry_account.get(), entry_aadhaar.get(), entry_name.get(), entry_dob.get(), entry_contact.get()
        ))
        submit_button.grid(row=5, columnspan=2, pady=5)
        
    def submit_account_kyc(self, ac_number, aadhaar_number, name, dob, contact):
        if ac_number != '' and aadhaar_number != '' and name != '' and dob != '' and contact != '':
            # Placeholder function to handle the submission of account opening details
            print(f"Account KYC Details\nAccount Number: {ac_number}\nAadhaar Number: {aadhaar_number}\nName: {name}\nDOB: {dob}\nContact: {contact}")
        else:
            print("Please fill all fields")
    


# Create an instance of the CustomLayout class
app = CustomLayout()
app.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


# Base class for creating Tkinter application pages
class BasePage(tk.Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.configure(bg="#fff")
        self.resizable(True, True)

        # Connect to MySQL database
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="",
                database="Blood_DB"
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def __del__(self):
        # Close the database connection when the window is closed
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")


# Class for the login page
class LoginPage(BasePage):
    def __init__(self):
        super().__init__('Login', '925x500+300+200')

        self.login_frame = Frame(self, background="white")
        self.login_frame.pack(expand=20)

        self.heading = Label(self.login_frame, text='Login', fg='#57a1f8', bg='white', font=('Arial', 23, 'bold'))
        self.heading.grid(row=0, column=0, columnspan=2)

        self.img = PhotoImage(file='login.png')
        Label(self.login_frame, image=self.img, bg='white').grid(rowspan=2, column=0)

        self.user = Entry(self.login_frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.user.grid(row=1, column=1)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=420, y=140)
        Frame(self.login_frame, width=200, height=2, bg='black').place(x=420, y=235)

        self.code = Entry(self.login_frame, width=25, fg='black', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.code.grid(row=2, column=1, sticky="n")
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', self.on_enter_code)
        self.code.bind('<FocusOut>', self.on_leave_code)

        Button(self.login_frame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=self.signin).grid(
            row=3, column=1, columnspan=2)

    def on_enter_user(self, e):
        self.user.delete(0, 'end')

    def on_leave_user(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def on_enter_code(self, e):
        self.code.delete(0, 'end')
        self.code.config(show='*')

    def on_leave_code(self, e):
        name = self.code.get()
        if name == '':
            self.code.config(show='')  
            self.code.insert(0, 'Password')

    def signin(self):
        username = self.user.get()
        password = self.code.get()

        if username == 'admin' and password == '1234':
            self.open_home_page()
        else:
            messagebox.showerror("Invalid", "Invalid username and password")

    def open_home_page(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()
        
        
# Class for the home page
class HomePage(BasePage):
    def __init__(self):
        super().__init__('Home Page', '400x300')

        label = tk.Label(self, text="Blood Donation Management System", font=("Helvetica", 16))
        label.pack(pady=20)

        manage_donors_button = tk.Button(self, text="Manage Donors", command=self.open_manage_donors)
        manage_donors_button.pack(pady=10)

        manage_donations_button = tk.Button(self, text="Manage Donations", command=self.open_manage_donations)
        manage_donations_button.pack(pady=10)

        admin_profile_button = tk.Button(self, text="Admin Profile", command=self.open_admin_profile)
        admin_profile_button.pack(pady=10)

    def open_manage_donors(self):
        self.withdraw()
        manage_donors_page = ManageDonorsPage()
        manage_donors_page.mainloop()

    def open_manage_donations(self):
        self.withdraw()
        manage_donations_page = ManageDonationsPage()
        manage_donations_page.mainloop()

    def open_admin_profile(self):
        self.withdraw()
        admin_profile_page = AdminProfilePage()
        admin_profile_page.mainloop()
        
        
# Class for managing donors
class ManageDonorsPage(BasePage):
    def __init__(self):
        super().__init__('Manage Donors', '600x400')

        label = tk.Label(self, text="Manage Donors Page", font=("Helvetica", 16))
        label.pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("Name", "Age", "Blood Type", "Address", "Contact Number")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Fetch and display existing donors in the table
        self.populate_table()

        # Add button for adding donors
        add_button = tk.Button(self, text="Add Donor", command=self.add_donor)
        add_button.pack(pady=10)

        # Add button for going back to the home page
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Donors"
            cursor.execute(query)
            donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert data into the table
            for donor in donors:
                self.tree.insert("", "end", values=donor)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

    def add_donor(self):
        # Create a new window for adding donors
        add_donor_window = tk.Toplevel(self)
        add_donor_window.title("Add Donor")

        # Entry fields for adding donors
        name_entry = tk.Entry(add_donor_window)
        age_entry = tk.Entry(add_donor_window)
        blood_type_entry = tk.Entry(add_donor_window)
        address_entry = tk.Entry(add_donor_window)
        contact_number_entry = tk.Entry(add_donor_window)

        # Labels for entry fields
        tk.Label(add_donor_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Blood Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Address:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Contact Number:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        age_entry.grid(row=1, column=1, padx=10, pady=5)
        blood_type_entry.grid(row=2, column=1, padx=10, pady=5)
        address_entry.grid(row=3, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=4, column=1, padx=10, pady=5)

        # Button to save donor information
        save_button = tk.Button(add_donor_window, text="Save Donor", command=lambda: self.save_donor_info_entry(
        name_entry.get(), age_entry.get(), blood_type_entry.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=5, columnspan=2, pady=10)

    def save_donor_info_entry(self, name, age, blood_type, address, contact_number):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Donors (Name, Age, Blood_Type, Address, Contact_Number) VALUES (%s, %s, %s, %s, %s)"
            values = (name, age, blood_type, address, contact_number)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Donor information saved successfully!")

            # Update the table with the new donor
            self.populate_table()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error saving donor information.")

        finally:
            if cursor:
                cursor.close()

    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()
        
        
# Class for managing donations
class ManageDonationsPage(BasePage):
    def __init__(self):
        super().__init__('Manage Donations', '400x300')

        label = tk.Label(self, text="Manage Donations Page", font=("Helvetica", 16))
        label.pack(pady=20)

        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)

    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()

# Class for the admin profile page
class AdminProfilePage(BasePage):
    def __init__(self):
        super().__init__('Admin Profile', '400x300')

        label = tk.Label(self, text="Admin Profile Page", font=("Helvetica", 16))
        label.pack(pady=20)

        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)

    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()


if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
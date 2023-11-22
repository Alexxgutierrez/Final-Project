import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import tkcalendar as tkc
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
# Class for the login page
class LoginPage(BasePage):
    def __init__(self):
        super().__init__('Login', '850x500')

        self.login_frame = Frame(self, background="white")
        self.login_frame.pack(expand=20)

        self.heading = Label(self.login_frame, text='Login', fg='#df4145', bg='white', font=('Arial', 23, 'bold'))
        self.heading.grid(row=1, column=1, pady=(20, 0))  # Using grid for the heading with some padding

        self.img = PhotoImage(file='bdmsss.png')
        Label(self.login_frame, image=self.img, bg='white').grid(row=1, column=0, rowspan=3, padx=(20, 0))  # Using grid for the image with some padding

        self.user = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.user.place(x=420, y=120)  # Using grid for the username entry

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=420, y=150)  # Using grid for the first horizontal line

        self.code = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.code.grid(row=3, column=1, pady=10)  # Using grid for the password entry

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=420, y=230)  # Using grid for the second horizontal line

        Button(self.login_frame, width=20, pady=7, text='Login', bg='#00ff00', fg='#df4145', border=0, command=self.signin).grid(row=3, column=1, pady=(190, 20))

    def on_enter_user(self, e):
        if (self.user.get() == 'Username'):
            self.user.delete(0, 'end')

    def on_leave_user(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def on_enter_code(self, e):
        if (self.code.get() == 'Password'):
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
        self.destroy()
        home_page = HomePage()
        home_page.mainloop()
        
        
# Class for the home page
class HomePage(BasePage):
    def __init__(self):
        super().__init__('HomePage', '1920x1080')

        self.sidebar_frame = Frame(self, bg='#f00', width=200)
        self.sidebar_frame.pack(side=LEFT, fill=Y)
        
        self.content_frame = Frame(self, bg='white', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)  # Content frame to display tables

        dashboard_button = tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard, height = 2, width=15)
        dashboard_button.pack(pady=10)
        
        manage_donors_button = tk.Button(self.sidebar_frame, text="Donors", command=self.open_manage_donors, height=2, width=15)
        manage_donors_button.pack(pady=20)

        manage_donations_button = tk.Button(self.sidebar_frame, text="Donations", command=self.open_manage_donations, height=2, width=15)
        manage_donations_button.pack(pady=20)

        logout_button = tk.Button(self.sidebar_frame, text="Logout", command=self.logout, height=2, width=15)
        logout_button.pack(pady=20)
        
        self.show_dashboard()

    def show_dashboard(self):
        # Calculate total donations for each blood type
        blood_type_donations = self.calculate_blood_type_donations()

        # Clear existing items in the display frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create a Treeview widget for displaying the blood type donations
        columns = ("Blood Type", "Donation Count")
        dashboard_tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        dashboard_tree.heading("Blood Type", text="Blood Type")
        dashboard_tree.heading("Donation Count", text="Donation Count")
        dashboard_tree.pack(padx=10, pady=5)

        # Insert data into the Treeview
        for blood_type, donation_count in blood_type_donations.items():
            dashboard_tree.insert("", "end", values=(blood_type, donation_count))

    def calculate_blood_type_donations(self):
        # Perform database query to calculate total donations for each blood type
        try:
            cursor = self.connection.cursor()
            query = "SELECT Blood_Type, COUNT(*) AS Donation_Count FROM Blood_Donations GROUP BY Blood_Type"
            cursor.execute(query)
            blood_type_donations = {row[0]: row[1] for row in cursor.fetchall()}

            # Add AB type with 0 donations if not present in the result
            blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            for blood_type in blood_types:
                if blood_type not in blood_type_donations:
                    blood_type_donations[blood_type] = 0

            return blood_type_donations

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error fetching blood type donations.")

        finally:
            if cursor:
                cursor.close()


    # Inside the Dashboard class
    def open_manage_donors(self):
        self.content_frame.pack_forget()
        self.content_frame = Frame(self, bg='white', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Pass the connection to ManageDonorsPage
        manage_donors_page = ManageDonorsPage(master=self.content_frame, connection=self.connection)
        manage_donors_page.pack(fill=BOTH, expand=True)

    def open_manage_donations(self):
        self.content_frame.pack_forget()
        self.content_frame = Frame(self, bg='white', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        manage_donations_page = ManageDonationsPage(master=self.content_frame, connection=self.connection)
        manage_donations_page.pack(fill=BOTH, expand=True)

    def logout(self):
        self.destroy()
        LoginPage().mainloop()
        
    
# Class for managing donors
class ManageDonorsPage(Frame):
    def __init__(self, master=None, connection=None):
        super().__init__(master)
        self.connection = connection  # Store the connection
        
        label = tk.Label(self, text="Manage Donors", font=("Helvetica", 16))
        label.pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("Donor ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Fetch and display existing donors in the table
        self.populate_table()

        # Add button for adding donors
        add_button = tk.Button(self, text="Add Donor", command=self.add_donor)
        add_button.pack(pady=10)

        # Add button for updating donors
        update_button = tk.Button(self, text="Update Donor", command=self.update_donor)
        update_button.pack(pady=10)

        # Add button for deleting donors
        delete_button = tk.Button(self, text="Delete Donor", command=self.delete_donor)
        delete_button.pack(pady=10)
        
        # Create input fields for search and filtering
        self.blood_type_filter_entry = tk.Entry(self)

        # Labels for filter fields
        tk.Label(self, text="Filter by Blood Type:").pack()
        self.blood_type_filter_entry.pack()

        # Button to apply filters
        filter_button = tk.Button(self, text="Apply Filter", command=self.apply_filters)
        filter_button.pack(pady=10)

    def apply_filters(self):
        # Retrieve filter criteria
        blood_type_filter = self.blood_type_filter_entry.get()

        # Perform filtering based on criteria
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donor_ID, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter,))
            filtered_donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert filtered data into the table
            for donor in filtered_donors:
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
        sex_entry = ttk.Combobox(add_donor_window, values=["Male", "Female"])
        age_entry = tk.Entry(add_donor_window)
        blood_type = ttk.Combobox(add_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        address_entry = tk.Entry(add_donor_window)
        contact_number_entry = tk.Entry(add_donor_window)

        # Labels for entry fields
        tk.Label(add_donor_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Blood Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donor_window, text="Contact Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        blood_type.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button to save donor information
        save_button = tk.Button(add_donor_window, text="Save Donor", command=lambda: self.save_donor_info_entry(
        name_entry.get(), sex_entry.get(), age_entry.get(), blood_type.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            age_entry.delete(0, 'end')
            blood_type.delete(0, 'end')  # Clear the dropdown selection
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')

        clear_button = tk.Button(add_donor_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=7, columnspan=2, pady=10)

    def update_donor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donor to update.")
            return

        donor_info = self.tree.item(selected_item, 'values')
        donor_id = donor_info[0]

        # Open a new window to update donor info
        update_donor_window = tk.Toplevel(self)
        update_donor_window.title("Update Donor")

        # Entry fields for updating donors
        name_entry = tk.Entry(update_donor_window)
        sex_entry = ttk.Combobox(update_donor_window, values=["Male", "Female"])
        age_entry = tk.Entry(update_donor_window)
        blood_type = ttk.Combobox(update_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        address_entry = tk.Entry(update_donor_window)
        contact_number_entry = tk.Entry(update_donor_window)

        # Labels for entry fields
        tk.Label(update_donor_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Age:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Blood Type:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donor_window, text="Contact Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        
        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        age_entry.grid(row=2, column=1, padx=10, pady=5)
        blood_type.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        # Set the default values to the selected donor's information
        name_entry.insert(0, donor_info[1])
        sex_entry.insert(0, donor_info[2])
        age_entry.insert(0, donor_info[3])
        blood_type.insert(0, donor_info[4])
        address_entry.insert(0, donor_info[5])
        contact_number_entry.insert(0, donor_info[6])

        # Button to save updated donor information
        save_button = tk.Button(update_donor_window, text="Save Changes", command=lambda: self.save_updated_donor_info(
        donor_id, name_entry.get(), sex_entry.get(), age_entry.get(), blood_type.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)

        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            age_entry.delete(0, 'end')
            blood_type.delete(0, 'end')
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')

        clear_button = tk.Button(update_donor_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=7, columnspan=2, pady=10)
        
    def save_donor_info_entry(self, name, sex, age, blood_type, address, contact_number):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO donors (Name, Sex, Age, Blood_Type, Address, Contact_Number) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, sex, age, blood_type, address, contact_number)
            cursor.execute(query, values)
            
            self.connection.commit()
            messagebox.showinfo("Success", "Donor information saved successfully!")

            # Update the table with the new donor
            self.populate_table()
            self.clear_add_donor_fields()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error saving donor information.")

        finally:
            if cursor:
                cursor.close()
                
    def clear_add_donor_fields(self):
        # Clear all entry fields for adding donors
        self.name_entry.delete(0,'end')
        self.sex_entry.delete(0,'end')
        self.age_entry.delete(0,'end')
        self.blood_type.set(0, 'end')  # Clear the dropdown selection
        self.address_entry.delete(0,'end')
        self.contact_number_entry.delete(0,'end')

    def save_updated_donor_info(self, donor_id, name, sex, age, blood_type, address, contact_number):
        print(donor_id)
        try:
            cursor = self.connection.cursor()
            query = "UPDATE donors SET Name=%s, Sex=%s, Age=%s, Blood_Type=%s, Address=%s, Contact_Number=%s WHERE Donor_ID=%s"
            values = (name, sex, age, blood_type, address, contact_number, donor_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Donor information updated successfully!")

            # Update the table with the updated donor information
            self.populate_table()
            self.clear_update_donor_fields()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating donor information.")

        finally:
            if cursor:
                cursor.close()
                
    def clear_update_donor_fields(self):
        # Clear all entry fields for updating donors
        self.name_entry.delete(0, 'end')
        self.sex_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.blood_type.set(0, 'end')  # Clear the dropdown selection
        self.address_entry.delete(0, 'end')
        self.contact_number_entry.delete(0, 'end')
                
    def delete_donor(self):
        # Get the selected donor's information
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donor to delete.")
            return

        donor_info = self.tree.item(selected_item, 'values')
        donor_id = donor_info[0]  # Assuming the donor ID is the first column

        # Confirm deletion with a message box
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {donor_info[1]}?")
        if confirmation:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM donors WHERE Donor_ID=%s"
                cursor.execute(query, (donor_id,))

                self.connection.commit()
                messagebox.showinfo("Success", "Donor deleted successfully!")

                # Update the table after deletion
                self.populate_table()

            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Error deleting donor.")

            finally:
                if cursor:
                    cursor.close()

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donor_Id, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors"  # Exclude Donor_ID column
            cursor.execute(query)
            donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert data into the table (excluding Donor_ID)
            for donor in donors:
                self.tree.insert("", "end", values=donor)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
                
        
# Class for managing donations
class ManageDonationsPage(Frame):
    def __init__(self, master=None, connection=None):
        super().__init__(master)
        self.connection = connection  # Store the connection

        label = tk.Label(self, text="Manage Donations", font=("Helvetica", 16))
        label.pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("Donation_ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)
        
        # Add button for adding donors
        add_button = tk.Button(self, text="Add Donor", command=self.add_donation)
        add_button.pack(pady=10)

        # Add button for updating donors
        update_button = tk.Button(self, text="Update Donor", command=self.update_donation)
        update_button.pack(pady=10)

        # Add button for deleting donors
        delete_button = tk.Button(self, text="Delete Donor", command=self.delete_donation)
        delete_button.pack(pady=10)
        
        # Create input fields for search and filtering
        self.blood_type_filter_entry = tk.Entry(self)

        # Labels for filter fields
        tk.Label(self, text="Filter by Blood Type:").pack()
        self.blood_type_filter_entry.pack()

        # Button to apply filters
        filter_button = tk.Button(self, text="Apply Filter", command=self.apply_filters)
        filter_button.pack(pady=10)

        # Populate the table initially
        self.populate_table()
        
    def add_donation(self):
        # Create a new window for adding donors
        add_donation_window = tk.Toplevel(self)
        add_donation_window.title("Add Donation")

        # Entry fields for adding donors
        name_entry = tk.Entry(add_donation_window)
        sex_entry = ttk.Combobox(add_donation_window, values=["Male", "Female"])
        blood_type = ttk.Combobox(add_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        donation_date = tkc.DateEntry(add_donation_window)
        blood_amount = tk.Entry(add_donation_window)

        # Labels for entry fields
        tk.Label(add_donation_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Blood Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Date of Donation:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(add_donation_window, text="Amount (mL):").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        blood_type.grid(row=2, column=1, padx=10, pady=5)
        donation_date.grid(row=3, column=1, padx=10, pady=5)
        blood_amount.grid(row=4, column=1, padx=10, pady=5)

        # Button to save donor information
        save_button = tk.Button(add_donation_window, text="Save Donation", command=lambda: self.save_donation(
        name_entry.get(), sex_entry.get(), blood_type.get(), donation_date.get(), blood_amount.get()))
        save_button.grid(row=5, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            blood_type.delete(0, 'end')  # Clear the dropdown selection
            donation_date(0, 'end')
            blood_amount.delete(0, 'end')

        clear_button = tk.Button(add_donation_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=6, columnspan=2, pady=10)

    def update_donation(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to update.")
            return

        donation_info = self.tree.item(selected_item, 'values')
        donation_id = donation_info[0]

        # Open a new window to update donation info
        update_donation_window = tk.Toplevel(self)
        update_donation_window.title("Update Donation")

        name_entry = tk.Entry(update_donation_window)
        sex_entry = ttk.Combobox(update_donation_window, values=["Male", "Female"])
        blood_type = ttk.Combobox(update_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        donation_date = tkc.DateEntry(update_donation_window)
        blood_amount = tk.Entry(update_donation_window)

        # Labels for entry fields
        tk.Label(update_donation_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Sex:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Blood Type:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Date of Donation:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(update_donation_window, text="Amount (mL):").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Entry fields placement
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        sex_entry.grid(row=1, column=1, padx=10, pady=5)
        blood_type.grid(row=2, column=1, padx=10, pady=5)
        donation_date.grid(row=3, column=1, padx=10, pady=5)
        blood_amount.grid(row=4, column=1, padx=10, pady=5)
        
        # Set the default values to the selected donor's information
        name_entry.insert(0, donation_info[1])
        sex_entry.insert(0, donation_info[2])
        blood_type.insert(0, donation_info[3])
        donation_date.insert(0, donation_info[4])
        blood_amount.insert(0, donation_info[5])

        # Button to save donor information
        save_button = tk.Button(update_donation_window, text="Save Donation", command=lambda: self.save_update_donation(donation_id,
        name_entry.get(), sex_entry.get(), blood_type.get(), donation_date.get(), blood_amount.get()))
        save_button.grid(row=5, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            blood_type.delete(0, 'end')  # Clear the dropdown selection
            donation_date(0, 'end')
            blood_amount.delete(0, 'end')

        clear_button = tk.Button(update_donation_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=6, columnspan=2, pady=10)
                
    def clear_add_donation_fields(self):
        # Clear all entry fields for adding donors
        self.name_entry.delete(0, 'end')
        self.sex_entry.delete(0, 'end')
        self.blood_type.delete(0, 'end')  # Clear the dropdown selection
        self.donation_date(0, 'end')
        self.blood_amount.delete(0, 'end')
                
    def clear_update_donation_fields(self):
        # Clear all entry fields for updating donors
        self.name_entry.delete(0, 'end')
        self.sex_entry.delete(0, 'end')
        self.blood_type.delete(0, 'end')  # Clear the dropdown selection
        self.donation_date(0, 'end')
        self.blood_amount.delete(0, 'end')

    def save_donation(self, name, sex, blood_type, date, amount):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO blood_donations (Name, Sex, Blood_Type, Date_of_Donation, Amount) VALUES (%s, %s, %s, %s, %s)"
            values = (name, sex, blood_type, date, amount)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information added successfully!")

            # Update the table with the new blood donation
            self.populate_table()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error adding blood donation information.")

        finally:
            if cursor:
                cursor.close()

    def save_update_donation(self, donation_id, name, sex, blood_type, date, amount):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE blood_donations SET Name=%s, Sex=%s, Blood_Type=%s, Date_of_Donation=%s, Amount=%s WHERE Donation_ID=%s"
            values = (name, sex, blood_type, date, amount, donation_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information updated successfully!")

            # Update the table with the updated blood donation
            self.populate_table()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating blood donation information.")

        finally:
            if cursor:
                cursor.close()

    def delete_donation(self):
        # Get the selected donation's information
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation to delete.")
            return

        donation_info = self.tree.item(selected_item, 'values')
        donation_id = donation_info[0]  # Assuming the donation ID is the first column

        # Confirm deletion with a message box
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {donation_info[1]}?")
        if confirmation:
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM blood_donations WHERE Donation_ID=%s"
                cursor.execute(query, (donation_id,))

                self.connection.commit()
                messagebox.showinfo("Success", "Blood donation deleted successfully!")

                # Update the table after deletion
                self.populate_table()

            except Error as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", "Error deleting blood donation.")

            finally:
                if cursor:
                    cursor.close()

    def apply_filters(self):
        # Retrieve filter criteria
        blood_type_filter = self.blood_type_filter_entry.get()
        
        # Perform filtering based on criteria
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donation_ID, Name, Sex, Blood_Type, Date_of_Donation, Amount FROM blood_donations WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter,))
            filtered_donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert filtered data into the table
            for donor in filtered_donors:
                self.tree.insert("", "end", values=donor)

        except Error as e:
                print(f"Error: {e}")

        finally:
                if cursor:
                    cursor.close()
        pass

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donation_ID, Name, Sex, Blood_Type, Date_of_Donation, Amount FROM blood_donations"  # Exclude Donation_ID column
            cursor.execute(query)
            donations = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert data into the table (excluding Donation_ID)
            for donation in donations:
                self.tree.insert("", "end", values=donation)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
        
if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()

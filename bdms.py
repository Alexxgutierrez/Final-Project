import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from tkinter import StringVar

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
        
        logout_button = tk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

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
    
    def logout(self):
        self.destroy()
        login_page = LoginPage()
        login_page.mainloop()
        
    
# Class for managing donors
class ManageDonorsPage(BasePage):
    def __init__(self):
        super().__init__('Manage Donors', '600x400')

        label = tk.Label(self, text="Manage Donors Page", font=("Helvetica", 16))
        label.pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("Donor_ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
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

        # Add button for going back to the home page
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)
        
        # Create input fields for search and filtering
        self.age_filter_entry = tk.Entry(self)
        self.sex_filter_entry = tk.Entry(self)
        self.blood_type_filter_entry = tk.Entry(self)

        # Labels for filter fields
        tk.Label(self, text="Filter by Blood Type:").pack()
        self.blood_type_filter_entry.pack()

        # Button to apply filters
        filter_button = tk.Button(self, text="Apply Filters", command=self.apply_filters)
        filter_button.pack(pady=10)

    def apply_filters(self):
        # Retrieve filter criteria
        blood_type_filter = self.blood_type_filter_entry.get()

        # Perform filtering based on criteria
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM donors WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter))
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
        sex_entry = tk.Entry(add_donor_window)
        age_entry = tk.Entry(add_donor_window)
        blood_type_entry = tk.Entry(add_donor_window)
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
        blood_type_entry.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button to save donor information
        save_button = tk.Button(add_donor_window, text="Save Donor", command=lambda: self.save_donor_info_entry(
        name_entry.get(), sex_entry.get(), age_entry.get(), blood_type_entry.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            age_entry.delete(0, 'end')
            blood_type_entry.delete(0, 'end')
            address_entry.delete(0, 'end')
            contact_number_entry.delete(0, 'end')

        clear_button = tk.Button(add_donor_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=7, columnspan=2, pady=10)

    def update_donor(self):
        # Get the selected donor's information
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donor to update.")
            return

        donor_info = self.tree.item(selected_item, 'values')
        donor_id = donor_info[0]  # Assuming the donor ID is the first column

        # Create a new window for updating donors
        update_donor_window = tk.Toplevel(self)
        update_donor_window.title("Update Donor")

        # Entry fields for updating donors
        name_entry = tk.Entry(update_donor_window)
        sex_entry = tk.Entry(update_donor_window)
        age_entry = tk.Entry(update_donor_window)
        blood_type_entry = tk.Entry(update_donor_window)
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
        blood_type_entry.grid(row=3, column=1, padx=10, pady=5)
        address_entry.grid(row=4, column=1, padx=10, pady=5)
        contact_number_entry.grid(row=5, column=1, padx=10, pady=5)

        # Set the default values to the selected donor's information
        name_entry.insert(0, donor_info[1])
        sex_entry.insert(0, donor_info[2])
        age_entry.insert(0, donor_info[3])
        blood_type_entry.insert(0, donor_info[4])
        address_entry.insert(0, donor_info[5])
        contact_number_entry.insert(0, donor_info[6])

        # Button to save updated donor information
        save_button = tk.Button(update_donor_window, text="Save Donor", command=lambda: self.save_donor_info_entry(
        name_entry.get(), sex_entry.get(), age_entry.get(), blood_type_entry.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.delete(0, 'end')
            age_entry.delete(0, 'end')
            blood_type_entry.delete(0, 'end')
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

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error saving donor information.")

        finally:
            if cursor:
                cursor.close()

    def save_updated_donor_info(self, donor_id, name, sex, age, blood_type, address, contact_number):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE donors SET Name=%s, Sex=%s, Age=%s, Blood_Type=%s, Address=%s, Contact_Number=%s WHERE Donor_ID=%s"
            values = (name, sex, age, blood_type, address, contact_number, donor_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Donor information updated successfully!")

            # Update the table with the updated donor information
            self.populate_table()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating donor information.")

        finally:
            if cursor:
                cursor.close()

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
            query = "SELECT * FROM donors"
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
                
    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()
        
# Class for managing donations
class ManageDonationsPage(BasePage):
    def __init__(self):
        super().__init__('Manage Donations', '800x600')

        label = tk.Label(self, text="Manage Donations Page", font=("Helvetica", 16))
        label.pack(pady=20)

        # Create a Treeview widget for the table
        columns = ("Donation_ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

        # Button to search donation
        search_donation_button = tk.Button(self, text="Search Donation", command=self.search_donation)
        search_donation_button.pack(pady=10)

        # Button to go back to the home page
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)

        # Populate the table initially
        self.populate_table()

    def add_donation(self, name, sex, blood_type, date, amount):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Blood_Donations (Name, Sex, Blood_Type, Date_of_Donation, Amount) VALUES (%s, %s, %s, %s, %s)"
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

    def update_donation(self, donation_id, name, sex, blood_type, date, amount):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Blood_Donations SET Name=%s, Sex=%s, Blood_Type=%s, Date_of_Donation=%s, Amount=%s WHERE Donation_ID=%s"
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

    def delete_donation(self, donation_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM Blood_Donations WHERE Donation_ID=%s"
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

    def search_donation(self):
        # Implement the search functionality here
        pass

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Blood_Donations"
            cursor.execute(query)
            donations = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert data into the table
            for donation in donations:
                self.tree.insert("", "end", values=donation)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()


# Class for the admin profile page
class AdminProfilePage(BasePage):
    def __init__(self):
        super().__init__('Admin Profile', '400x300')

        self.profile_data = {}  # To store the admin profile data

        label = tk.Label(self, text="Company Info", font=("Helvetica", 16))
        label.pack(pady=20)

        # Fields for admin profile
        self.name_entry = tk.Entry(self, state='readonly')
        self.email_entry = tk.Entry(self, state='readonly')
        self.contact_number_entry = tk.Entry(self, state='readonly')
        self.telephone_entry = tk.Entry(self, state='readonly')
        self.address_entry = tk.Entry(self, state='readonly')

        # Labels for admin profile fields
        tk.Label(self, text="Name:").pack()
        self.name_entry.pack()

        tk.Label(self, text="Email:").pack()
        self.email_entry.pack()

        tk.Label(self, text="Contact Number:").pack()
        self.contact_number_entry.pack()

        tk.Label(self, text="Telephone Number:").pack()
        self.telephone_entry.pack()

        tk.Label(self, text="Address:").pack()
        self.address_entry.pack()

        # Button to edit profile
        self.edit_button = tk.Button(self, text="Edit Profile", command=self.edit_profile)
        self.edit_button.pack(pady=10)

        self.save_changes_button = tk.Button(self, text="Save Changes", command=self.save_profile_changes)
        self.save_changes_button.pack_forget()  # Initially hide the Save Changes button

        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home)
        back_button.pack(pady=10)

        # Simulate loading admin profile data (replace with actual data retrieval)
        self.load_admin_profile()

    def load_admin_profile(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Admin_Profile WHERE Admin_ID = %s"
            cursor.execute(query, (1,))  # Replace 1 with the actual Admin_ID

            admin_profile = cursor.fetchone()
            if admin_profile:
                self.profile_data = {
                    'name': admin_profile[1],
                    'email': admin_profile[2],
                    'contact_number': admin_profile[3],
                    'telephone_number': admin_profile[4],
                    'address': admin_profile[5]
                }

                # Populate the fields with admin profile data
                self.name_entry.insert(0, self.profile_data['name'])
                self.email_entry.insert(0, self.profile_data['email'])
                self.contact_number_entry.insert(0, self.profile_data['contact_number'])
                self.telephone_entry.insert(0, self.profile_data['telephone_number'])
                self.address_entry.insert(0, self.profile_data['address'])
            else:
                print("Admin profile not found.")

        except mysql.connector.Error as e:
            print(f"Error fetching admin profile: {e}")
            messagebox.showerror("Error", "Error loading admin profile information.")

        finally:
            if cursor:
                cursor.close()

    def edit_profile(self):
        # Enable editing of the profile fields
        self.name_entry.config(state='normal')
        self.email_entry.config(state='normal')
        self.contact_number_entry.config(state='normal')
        self.telephone_entry.config(state='normal')
        self.address_entry.config(state='normal')

        # Show the 'Save Changes' button only when editing starts
        self.save_changes_button.pack(pady=10)
        self.edit_button.pack_forget()  # Hide the 'Edit Profile' button while editing

    def save_profile_changes(self):
        # Retrieve updated values from the fields
        updated_name = self.name_entry.get()
        updated_email = self.email_entry.get()
        updated_contact_number = self.contact_number_entry.get()
        updated_telephone_number = self.telephone_entry.get()
        updated_address = self.address_entry.get()

        try:
        # Update the admin profile in the database
            cursor = self.connection.cursor()
            query = "UPDATE Admin_Profile SET Name=%s, Email=%s, Contact_Number=%s, Telephone_Number=%s, Address=%s WHERE Admin_ID=%s"
            values = (updated_name, updated_email, updated_contact_number, updated_telephone_number, updated_address, 1)  # Replace 1 with the actual Admin_ID

            cursor.execute(query, values)
            self.connection.commit()

            # Disable editing after changes are saved
            self.name_entry.config(state='readonly')
            self.email_entry.config(state='readonly')
            self.contact_number_entry.config(state='readonly')
            self.telephone_entry.config(state='readonly')
            self.address_entry.config(state='readonly')

            # Remove the 'Save Changes' button after changes are saved
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == "Save Changes":
                    widget.pack_forget()

            # Provide feedback to the admin about the changes
            messagebox.showinfo("Success", "Profile changes saved successfully!")

        except Error as e:
            # Handle any errors that occur during database update
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating profile information.")

        finally:
            if cursor:
                cursor.close()
        
        # Hide the 'Save Changes' button after changes are saved
        self.save_changes_button.pack_forget()
        self.edit_button.pack()  # Show the 'Edit Profile' button again after saving changes

    def back_to_home(self):
        self.withdraw()
        home_page = HomePage()
        home_page.mainloop()


if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
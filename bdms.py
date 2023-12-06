import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import tkcalendar as tkc
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from tkinter import PhotoImage, font

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
                user="root",
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
        super().__init__('Login', '850x500')

        self.login_frame = Frame(self, background="white")
        self.login_frame.pack(expand=20)

        self.heading = Label(self.login_frame, text='Login', fg='#df4145', bg='white', font=('MonoLisa', 23, 'bold'))
        self.heading.grid(row=1, column=1, pady=(20, 0))  # Using grid for the heading with some padding

        self.img = PhotoImage(file='bdmsss.png')
        Label(self.login_frame, image=self.img, bg='white').grid(row=1, column=0, rowspan=3, padx=(20, 0))  # Using grid for the image with some padding

        self.user = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.user.place(x=430, y=120)  # Using grid for the username entry
        
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=430, y=150)  # Using grid for the first horizontal line

        self.code = Entry(self.login_frame, width=25, fg='#df4145', border=0, bg="white", font=('Microsoft Yahei UI Light', 11))
        self.code.grid(row=3, column=1, pady=10)  # Using grid for the password entry
        
        self.code.place(x=430,y=200)
        self.code.insert(0, 'Password')
        self.code.bind('<FocusIn>', self.on_enter_code)
        self.code.bind('<FocusOut>', self.on_leave_code)

        Frame(self.login_frame, width=200, height=2, bg='black').place(x=430, y=230)  # Using grid for the second horizontal line

        Button(self.login_frame, width=22, pady=7, text='Login', bg='#df4145', fg='white', border=0, command=self.signin).grid(row=3, column=1, pady=(190, 20))
        
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

        self.sidebar_frame = Frame(self, bg='#353A40', width=200)
        self.sidebar_frame.pack(side=LEFT, fill=Y)

        self.topbar_frame = Frame(self, bg='#df4145', height=75)
        self.topbar_frame.pack(side=TOP, fill=X)

        logo_image = PhotoImage(file="bdmslogo.png")

        logo_label = Label(self.sidebar_frame, image=logo_image, bg='#353A40')
        logo_label.image = logo_image
        logo_label.grid(row=0, column=0, sticky="nw", padx=40, pady=5)

        self.content_frame = Frame(self, bg='#E5E4E2', width=700, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)  # Content frame to display tables

        button_font = font.Font(family='Verdana', size=12)

        self.selected_button = None  # Variable to keep track of the selected button

        dashboard_button = tk.Button(self.sidebar_frame, text="DASHBOARD", command=lambda: self.handle_button_click(self.show_dashboard, dashboard_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        dashboard_button.grid(row=1, column=0, pady=(20, 25))

        manage_donors_button = tk.Button(self.sidebar_frame, text="DONORS", command=lambda: self.handle_button_click(self.open_manage_donors, manage_donors_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        manage_donors_button.grid(row=2, column=0, pady=25)

        manage_donations_button = tk.Button(self.sidebar_frame, text="DONATIONS", command=lambda: self.handle_button_click(self.open_manage_donations, manage_donations_button), bg='white', fg='#df4145', height=2, width=15, font=button_font, relief='flat')
        manage_donations_button.grid(row=3, column=0, pady=25)

        logout_button = tk.Button(self.sidebar_frame, text="LOGOUT", command=lambda: self.handle_button_click(self.logout, logout_button), fg='#df4145', bg='white', height=2, width=15, font=button_font, relief='flat')
        logout_button.grid(row=4, column=0, pady=25)

        self.heading_label = tk.Label(self.topbar_frame, text="DASHBOARD    ", font=("Helvetica", 37), bg='#df4145',fg='white')
        self.heading_label.pack(side=tk.LEFT, padx=20, pady=20)

        self.show_dashboard()

    def highlight_button(self, button):
        # Reset the background color of the previously selected button
        if self.selected_button:
            self.selected_button.config(bg='white')

        # Highlight the clicked button
        button.config(bg='#00FFFF')  # You can use any color for highlighting
        self.selected_button = button

    def handle_button_click(self, callback, button):
        # Reset the background color of the previously selected button
        if self.selected_button:
            self.selected_button.config(bg='white')

        # Check if the clicked button is the logout button
        if button.cget("text") != "LOGOUT":
            # Highlight the clicked button
            button.config(bg='#a4e9d5')  # You can use any color for highlighting
            self.selected_button = button

            # Set the heading label based on the clicked button
            page_title = button.cget("text")
            self.heading_label.config(text=page_title)

        # Call the corresponding method
        callback()

    def show_dashboard(self):
        # Calculate total donations for each blood type 
        blood_type_donations = self.calculate_blood_type_donations()

        # Clear existing items in the display frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Load the blood drop image
        blood_image = PhotoImage(file='bloodrop2.png')
        
        # Define blood types
        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        # Create frames for each blood type
        for i, blood_type in enumerate(blood_types):
            row = i // 4  # Calculate the row based on the index
            col = i % 4   # Calculate the column based on the index

            frame = Frame(self.content_frame, bg='#E0FFFF', width=200, height=105, bd=2, relief="groove")
            frame.pack_propagate(False)
            frame.grid(row=row, column=col, padx=55, pady=60)

            # Add blood drop image
            blood_label = Label(frame, image=blood_image, bg='#E0FFFF')
            blood_label.image = blood_image
            blood_label.place(x=160,y=5)

            # Add blood type label with bold text
            type_label = Label(frame, text=blood_type, font=("Helvetica", 16, "bold"), bg='#E0FFFF')
            type_label.place(x=115, y=10)

            # Add donation amount label with anchor set to "sw"
            amount_label = Label(frame, text=f"{blood_type_donations.get(blood_type, 0)} mL", bg='#E0FFFF')
            amount_label.place(x=2, y=80)

        # Ensure that the grid expands to fill any extra space
        self.content_frame.grid_columnconfigure(4, weight=1)

    def calculate_blood_type_donations(self):
        
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT Blood_Type, SUM(Amount) AS Total_Amount FROM Blood_Donations GROUP BY Blood_Type"
            cursor.execute(query)
            blood_type_donations = {row[0]: row[1] for row in cursor.fetchall()}

            # Ensure all blood types are included, even if they have zero donations
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
        self.content_frame = Frame(self, bg='#E5E4E2', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Pass the connection to ManageDonorsPage
        manage_donors_page = ManageDonorsPage(master=self.content_frame, connection=self.connection)
        manage_donors_page.pack(fill=BOTH, expand=True)

    def open_manage_donations(self):
        self.content_frame.pack_forget()
        self.content_frame = Frame(self, bg='#E5E4E2', width=600, height=400)
        self.content_frame.pack_propagate(False)
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        manage_donations_page = ManageDonationsPage(master=self.content_frame, connection=self.connection)
        manage_donations_page.pack(fill=BOTH, expand=True)

    def logout(self):
        # Display a confirmation message before logging out
        confirm_logout = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        
        if confirm_logout:
            # If the user confirms, destroy the current window and show the login page
            self.destroy()
            LoginPage().mainloop()
        
    
# Class for managing donors
class ManageDonorsPage(Frame):
    def __init__(self, master=None, connection=None):
        super().__init__(master)
        self.connection = connection  # Store the connection
        self.add_donor_window = None
        self.update_donor_window = None
        
        self.name_entry = None
        self.age_entry = None
        self.sex_entry = None
        self.blood_type = None
        self.address_entry = None
        self.contact_number_entry = None

        # Create a Treeview widget for the table
        columns = ("Donor ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # center
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # column widths
        self.tree.column("Donor ID", width=100)  
        self.tree.column("Name", width=250)  
        self.tree.column("Sex", width=100)  
        self.tree.column("Age", width=100)
        self.tree.column("Blood Type", width=100)  
        self.tree.column("Address", width=250)  
        self.tree.column("Contact Number", width=200)  

        for col in columns:
            self.tree.heading(col, text=col)
            
        # Define tag configurations for colors
        self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF")
        self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41")
        
        # Adjust the placement of the table freely

        self.tree.pack(pady=20) 
        self.tree.place(x=50, y=50)
        # Fetch and display existing donors in the table
        self.populate_table()
        
        style = ttk.Style()
        style.configure('Blood.TButton', foreground='#353A40', background='#df4145', font=('Arial', 12, 'bold'))

        # Add buttons for adding, updating, deleting donors, and apply filters
        add_button = ttk.Button(self, text="Add Donor", command=self.add_donor, style='Blood.TButton')
        update_button = ttk.Button(self, text="Update Donor", command=self.update_donor, style='Blood.TButton')
        delete_button = ttk.Button(self, text="Delete Donor", command=self.delete_donor, style='Blood.TButton')
        filter_button = ttk.Button(self, text="Filter by Blood Type", command=self.apply_filters, style='Blood.TButton')

        # Pack buttons horizontally
        add_button.place(x=115, y=320)
        update_button.place(x=360, y=320)
        delete_button.place(x=640, y=320) 
        filter_button.place(x=925, y=320)

        # Create input field for filtering
        self.blood_type_filter_entry = ttk.Combobox(self, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_filter_entry.configure(state='readonly')  #para di type
        
        # Labels for filter fields
        self.blood_type_filter_entry.place(x=925, y=360)
        #tk.Label(self, text="Filter by Blood Type").place(x=950, y=330)

    def apply_filters(self):
        # Retrieve filter criteria
        blood_type_filter = self.blood_type_filter_entry.get()

        # Perform filtering based on criteria
        try:
            cursor = self.connection.cursor()

            # Set up tag configurations for even and odd rows
            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            # Fetch and display existing donors in the table
            query = "SELECT Donor_ID, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors WHERE Blood_Type=%s"
            cursor.execute(query, (blood_type_filter,))
            filtered_donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert filtered data into the table with alternating row colors
            for i, donor in enumerate(filtered_donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

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
        sex_entry.configure(state='readonly')  #para di type
        age_entry = tk.Entry(add_donor_window)
        blood_type = ttk.Combobox(add_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  #para di type
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
            sex_entry.set('')
            age_entry.delete(0, 'end')
            blood_type.set('') 
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
        sex_entry.configure(state='readonly')  # para di type
        age_entry = tk.Entry(update_donor_window)
        blood_type = ttk.Combobox(update_donor_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  #para di type
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
        sex_entry.set(donor_info[2])
        age_entry.insert(0, donor_info[3])
        blood_type.set(donor_info[4])
        address_entry.insert(0, donor_info[5])
        contact_number_entry.insert(0, donor_info[6])

        # Button to save updated donor information
        save_button = tk.Button(update_donor_window, text="Save Changes", command=lambda: self.save_updated_donor_info(
        donor_id, name_entry.get(), sex_entry.get(), age_entry.get(), blood_type.get(), address_entry.get(), contact_number_entry.get()))
        save_button.grid(row=6, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')
            age_entry.delete(0, 'end')
            blood_type.set('')
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
            
            # Close the add_donor_window
            self.add_donor_window.destroy()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error saving donor information.")

        finally:
            if cursor:
                cursor.close()

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
            self.update_donor_window.destroy()

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error updating donor information.")

        finally:
            if cursor:
                cursor.close()
                
    def clear_add_donor_fields(self):
        # Clear all entry fields for adding donors
        self.name_entry.__delattr__(0,'end')
        self.sex_entry.__setattr__('')
        self.age_entry.__delattr__(0,'end')
        self.blood_type.__setattr__('')  
        self.address_entry.__delattr__(0,'end')
        self.contact_number_entry.__delattr__(0,'end')
        
    def clear_update_donor_fields(self):
        # Clear all entry fields for updating donors
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.age_entry.__delattr__(0, 'end')
        self.blood_type.__setattr__('')  
        self.address_entry.__delattr__(0, 'end')
        self.contact_number_entry.__delattr__(0, 'end')
                
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
            query = "SELECT Donor_Id, Name, Sex, Age, Blood_Type, Address, Contact_Number FROM donors"
            cursor.execute(query)
            donors = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Set up center alignment for columns
            center_columns = ("Donor ID", "Name", "Sex", "Age", "Blood Type", "Address", "Contact Number")
            for col in center_columns:
                self.tree.column(col, anchor='center')

            # Set up tag configurations for even and odd rows
            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            # Insert data into the table with appropriate tags
            for i, donor in enumerate(donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)


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
        self.add_donation_window = None
        self.update_donation_window = None
        
        self.name_entry = None
        self.sex_entry = None
        self.blood_type = None
        self.donation_date = None
        self.blood_amount = None

        # Create a Treeview widget for the table
        columns = ("Donation ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
       # Adjusting column headings alignment
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        # Set column widths for specific columns
        self.tree.column("Donation ID", width=100) 
        self.tree.column("Name", width=250)
        self.tree.column("Sex", width=100)
        self.tree.column("Blood Type", width=100)
        self.tree.column("Date of Donation", width=250)
        self.tree.column("Amount (ml)", width=170)
        
        for col in columns:
            self.tree.heading(col, text=col)
            
        # Define tag configurations for colors
        self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF")
        self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41")
        
        self.tree.pack(pady=20)
        self.tree.place(x=115,y=50)
        
        style = ttk.Style()
        style.configure('Blood.TButton', foreground='#353A40', background='#df4145', font=('Arial', 12, 'bold'))
        
         # Add buttons for adding, updating, deleting donors, and apply filters
        add_button = ttk.Button(self, text="Add Donation", command=self.add_donation, style='Blood.TButton')
        update_button = ttk.Button(self, text="Update Donation", command=self.update_donation, style='Blood.TButton')
        delete_button = ttk.Button(self, text="Delete Donation", command=self.delete_donation, style='Blood.TButton')
        filter_button = ttk.Button(self, text="Filter by Blood Type", command=self.apply_filters, style='Blood.TButton')

        # Pack buttons horizontally
        add_button.place(x=115, y=320)
        update_button.place(x=360, y=320)
        delete_button.place(x=640, y=320) 
        filter_button.place(x=925, y=320)

        # Create input field for filtering
        self.blood_type_filter_entry = ttk.Combobox(self, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        self.blood_type_filter_entry.configure(state='readonly')  #para di type
        
        # Labels for filter fields
        self.blood_type_filter_entry.place(x=925, y=360)

        # Populate the table initially
        self.populate_table()
        
    def add_donation(self):
        # Create a new window for adding donations
        add_donation_window = tk.Toplevel(self)
        add_donation_window.title("Add Donation")

        # Entry fields for adding donations
        name_entry = tk.Entry(add_donation_window)
        sex_entry = ttk.Combobox(add_donation_window, values=["Male", "Female"])
        sex_entry.configure(state='readonly')  # para di type
        blood_type = ttk.Combobox(add_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  # para di type
        donation_date = tkc.DateEntry(add_donation_window)
        donation_date.configure(state='readonly') #para di type
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
            sex_entry.set('')
            blood_type.set('')  
            donation_date.set_date('01/01/01')
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
        sex_entry.configure(state='readonly')  # para di type
        blood_type = ttk.Combobox(update_donation_window, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        blood_type.configure(state='readonly')  # para di type
        donation_date = tkc.DateEntry(update_donation_window)
        donation_date.configure(state='readonly')  # para di type
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
        sex_entry.set(donation_info[2])
        blood_type.set(donation_info[3])

        # Convert the date to the 'MM/DD/YY' format
        old_date_format = "%Y-%m-%d"  
        new_date_format = "%m/%d/%y"  #change format

        # Parse the date from the existing format to a datetime object
        parsed_date = datetime.strptime(donation_info[4], old_date_format)

        # Convert the datetime object to the desired format as a string
        formatted_date = parsed_date.strftime(new_date_format)

        # Set the formatted date as the default value for donation_date
        donation_date.set_date(formatted_date)

        blood_amount.insert(0, donation_info[5])

        # Button to save donor information
        save_button = tk.Button(update_donation_window, text="Save Donation", command=lambda: self.save_update_donation(donation_id,
        name_entry.get(), sex_entry.get(), blood_type.get(), donation_date.get(), blood_amount.get()))
        save_button.grid(row=5, columnspan=2, pady=10)
        
        def clear_fields():
            name_entry.delete(0, 'end')
            sex_entry.set('')  
            blood_type.set('')  
            donation_date.set_date('01/01/01') 
            blood_amount.delete(0, 'end')  

        clear_button = tk.Button(update_donation_window, text="Clear Fields", command=clear_fields)
        clear_button.grid(row=6, columnspan=2, pady=10)
                
    def clear_add_donation_fields(self):
        # Clear all entry fields for adding donors
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.blood_type.__setattr__('') 
        self.donation_date.__setattr__('01/01/01')
        self.blood_amount.__delattr__(0, 'end')
                
    def clear_update_donation_fields(self):
        # Clear all entry fields for updating donors
        self.name_entry.__delattr__(0, 'end')
        self.sex_entry.__setattr__('')
        self.blood_type.__setattr__('')  
        self.donation_date.__setattr__('01/01/01')
        self.blood_amount.__delattr__(0, 'end')

    def save_donation(self, name, sex, blood_type, date, amount):
        try:
            # Convert the date to the desired format 'YYYY-MM-DD'
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            cursor = self.connection.cursor()
            query = "INSERT INTO blood_donations (Name, Sex, Blood_Type, Date_of_Donation, Amount) VALUES (%s, %s, %s, %s, %s)"
            values = (name, sex, blood_type, formatted_date, amount)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information added successfully!")

            # Update the table with the new blood donation
            self.populate_table()
            self.clear_add_donation_fields()  # Clear the entry fields after adding a donor
            self.add_donation_window.destroy()  # Close the add donation window.

        except Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Error adding blood donation information.")

        finally:
            if cursor:
                cursor.close()

    def save_update_donation(self, donation_id, name, sex, blood_type, date, amount):
        try:
            # Convert the date to the desired format 'YYYY-MM-DD'
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")

            
            cursor = self.connection.cursor()
            query = "UPDATE blood_donations SET Name=%s, Sex=%s, Blood_Type=%s, Date_of_Donation=%s, Amount=%s WHERE Donation_ID=%s"
            values = (name, sex, blood_type, formatted_date, amount, donation_id)
            cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Success", "Blood donation information updated successfully!")

            # Update the table with the updated blood donation
            self.populate_table()
            self.clear_update_donation_fields()  # Clear the entry fields after updating a donor information.
            self.update_donation_window.destroy()  # Close the update donation window.

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

            # Set up tag configurations for even and odd rows
            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            # Insert data into the table with appropriate tags
            for i, donor in enumerate(filtered_donors):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
                print(f"Error: {e}")

        finally:
                if cursor:
                    cursor.close()
        pass

    def populate_table(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT Donation_ID, Name, Sex, Blood_Type, Date_of_Donation, Amount FROM blood_donations"
            cursor.execute(query)
            donations = cursor.fetchall()

            # Clear existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Set up center alignment for columns
            center_columns = ("Donation ID", "Name", "Sex", "Blood Type", "Date of Donation", "Amount (ml)")
            for col in center_columns:
                self.tree.column(col, anchor='center')

             # Set up tag configurations for even and odd rows
            self.tree.tag_configure("evenrow", background="#d32d41", foreground="#E0FFFF", anchor='center')
            self.tree.tag_configure("oddrow", background="#E0FFFF", foreground="#d32d41", anchor='center')

            # Insert data into the table with appropriate tags
            for i, donor in enumerate(donations):
                row_tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.tree.insert("", "end", values=donor, tags=row_tags)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()
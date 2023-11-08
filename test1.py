import tkinter as tk
import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
mycursor = mydb.cursor()

# Create the users table if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

# Function to create a new account
def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username already exists
    mycursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    if result:
        status_label['text'] = "Username already exists"
    else:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()
        status_label['text'] = "Account created successfully"

# Function to log in
def log_in():
    username = username_entry.get()
    password = password_entry.get()

    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()

    if result:
        status_label['text'] = "Login successful"
    else:
        status_label['text'] = "Invalid username or password"

# GUI setup
root = tk.Tk()
root.title("Login/Signup")

# Username entry
username_label = tk.Label(root, text="Username")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Password entry
password_label = tk.Label(root, text="Password")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Buttons for login and signup
login_button = tk.Button(root, text="Login", command=log_in)
login_button.pack()
signup_button = tk.Button(root, text="Sign Up", command=sign_up)
signup_button.pack()

# Status label
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

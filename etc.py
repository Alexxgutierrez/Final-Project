import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testdb"
)
mycursor = mydb.cursor()

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

def log_in():
    username = username_entry.get()
    password = password_entry.get()

    mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()

    if result:
        status_label['text'] = "Login successful"
    else:
        status_label['text'] = "Invalid username or password"

root = tk.Tk()
root.title("Login/Signup")

window_width,window_height = 300,300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Load and display the background image
bg_image = Image.open("C:\\Users\\Kathleen Chelsea\\Documents\\project\\final project\\background photo.png")  # Replace with your image path
bg_image = bg_image.resize((1550, 800), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Calculate the center positions for the login and sign-up widgets
image_width = bg_image.width
image_height = bg_image.height

login_x = (image_width - 200) // 2  # Adjust 200 as needed for the width of the widgets
login_y = (image_height - 100) // 2  # Adjust 100 as needed for the height of the widgets

# Username entry
username_label = tk.Label(root, text="Username")
username_label.place(x=login_x, y=login_y)

username_entry = tk.Entry(root)
username_entry.place(x=login_x + 100, y=login_y)  # Adjust positions as needed

# Password entry
password_label = tk.Label(root, text="Password")
password_label.place(x=login_x, y=login_y + 30)  # Adjust positions as needed

password_entry = tk.Entry(root, show="*")
password_entry.place(x=login_x + 100, y=login_y + 30)  # Adjust positions as needed

# Buttons for login and signup
login_button = tk.Button(root, text="Login", command=log_in)
login_button.place(x=login_x + 30, y=login_y + 60)  # Adjust positions as needed

signup_button = tk.Button(root, text="Sign Up", command=sign_up)
signup_button.place(x=login_x + 110, y=login_y + 60)  # Adjust positions as needed

# Status label
status_label = tk.Label(root, text="")
status_label.place(x=login_x + 20, y=login_y + 90)  # Adjust positions as needed

root.mainloop()

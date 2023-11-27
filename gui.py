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

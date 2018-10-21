#!/usr/bin/python3
import sqlite3
import smtplib
import time
import datetime
from tkinter import *

class login_page(Frame):

    screen=0

    login_conn = sqlite3.connect('users.db')
	login_cur  = login_conn.cursor()

	error_msg  = " "

    def __init__(self,master):
        super(login_page,self).__init__(master)
        self.grid()
        self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def login(self):
		if(name == ''):
			error_msg = "Name field cannot be empty!"
		elif(password == ''):
			error_msg = "Password field cannot be empty! "
		else:
			try:
				success = 0
				admin   = 0
				login_cur.execute("SELECT password FROM users WHERE name = ?", (name,))
				check = login_cur.fetchall()
				if(password == check[0][0]):
					success = 1
					if(name == 'admin'): admin = 1
					else: admin = 0
				else:
					error_msg = "Incorrect Password!"
				return success, admin
			except Exception:
				error_msg = "Invalid login name or password!"

    def define_widgets(self):

        login_page_label=Label(self,text="Login Page")
        login_page_label.grid(row=0,column=1,columnspan=2,sticky=W)

        login_name_label=Label(self,text="User ID:")
        login_name_label.grid(row=2,column=0,sticky=E)

        self.login_name=StringVar()
        login_name_entry=Entry(self,textvariable=self.login_name)
        login_name_entry.grid(row=2,column=1,columnspan=3,sticky=W)

        login_pass_label=Label(self,text="Password:")
        login_pass_label.grid(row=3,column=0,sticky=E)

        self.login_pass=StringVar()
        login_pass_entry=Entry(self,textvariable=self.login_pass,show="*")
        login_pass_entry.grid(row=3,column=1,columnspan=3,sticky=W)

        login_btn=Button(self,text="Login",command=self.login_action)
        login_btn.grid(row=5,column=2,sticky=W)

        exit=Button(self,text="Exit",command=self.leave)
        exit.grid(row=5,column=3,sticky=W)

    def login_action(self):
    	print("This is password: ", self.login_pass.get())
    	self.quit()

    def leave(self):
        quit()


root=Tk()
root.title("NSL - Employee daily status update software")
root.geometry("800x500")

window=login_page(root)
screen=window.screen

name=None
password=None

while True:
    root.mainloop()

    if screen==0:
        name=window.login_name.get()

    screen=window.screen

    if screen<0:
        print("write data")
        break
        
    #
    # this has to be in a try: as when you click X (window close) rather
    # than exit i get a double destruction problem 
    try:
        window.destroy()
    except TclError:
        quit()

    if screen==0:
        window=login_page(root)
        window.login_name.set(" ")
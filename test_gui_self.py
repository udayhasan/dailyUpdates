#!/usr/bin/python3
import sqlite3
import smtplib
import time
import datetime
from tkinter import *

class login_page(Frame):

    screen	   = 0

    login_conn = None
    login_cur  = None

    error_msg  = " "
    admin	   = None

	def __init__(self,master):
		super(login_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = login_conn.cursor()
		self.grid()
		self.define_widgets()

    def create_user_table(self):
    	self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

    def login(self, name, password):
    	#print(name, password)
    	if(name == ''):
    		self.error_msg = "Name field cannot be empty!"
    	elif(password == ''):
    		self.error_msg = "Password field cannot be empty! "
    	else:
    		try:
    			success = 0
    			admin   = 0
    			self.login_cur.execute("SELECT password FROM users WHERE name = ?", (name,))
    			check = self.login_cur.fetchall()
    			self.login_conn.close()
    			if(password == check[0][0]):
    				success = 1
    				self.screen = 1
    				if(name == 'admin'): admin = 1
    				else: admin = 0
    			else:
    				self.screen = 0
    				self.error_msg = "Incorrect Password!"
    			return success, admin
    		except Exception:
    			self.error_msg = "Invalid login name or password!"
    			return success, admin

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
    	self.create_user_table()
    	success, self.admin = self.login(self.login_name.get(), self.login_pass.get())
    	
    	if(success ==1): self.screen = 1
    	else: self.screen = 0

    	print(self.screen)

    	self.quit()

    def leave(self):
        quit()

class user_dashboard(Frame):

	screen = 1
	admin  = 0

	def __init__(self,master,admin):
		super(user_dashboard,self).__init__(master)
		self.grid()
		self.define_widgets()
		self.admin = admin

	def define_widgets(self):

		dash_board_label=Label(self,text="::Dashboard::")
		dash_board_label.grid(row=0,column=0,columnspan=2,sticky=W)

		log_out=Button(self,text="Log Out",command=self.set_logout)
		log_out.grid(row=5,column=1,sticky=W)

		exit=Button(self,text="Exit",command=self.leave)
		exit.grid(row=5,column=2,sticky=W)

		edit_name_btn=Button(self,text="Edit User Name",command=self.set_value)
		edit_name_btn.grid(row=1,column=1,sticky=W)

		edit_email_btn=Button(self,text="Edit User Email",command=self.set_value)
		edit_email_btn.grid(row=1,column=2,sticky=W)

		edit_pass_btn=Button(self,text="Edit User Password",command=self.set_value)
		edit_pass_btn.grid(row=2,column=1,sticky=W)

		update_status_btn=Button(self,text="Update Status",command=self.set_value)
		update_status_btn.grid(row=2,column=2,sticky=W)

		edit_status_btn=Button(self,text="Edit Status",command=self.set_value)
		edit_status_btn.grid(row=3,column=1,sticky=W)

		if(self.admin == 1):
			add_user_btn=Button(self,text="Add User",command=self.set_value)
			add_user_btn.grid(row=3,column=2,sticky=W)

			delete_user_btn=Button(self,text="Delete User",command=self.set_value)
			delete_user_btn.grid(row=4,column=1,sticky=W)

			export_report_btn=Button(self,text="Export Report",command=self.set_value)
			export_report_btn.grid(row=4,column=2,sticky=W)

	def set_logout(self):
		self.screen = 0
		self.quit()

	def set_value(self):
		self.screen = 1
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
admin=None

while True:
    root.mainloop()

    if screen==0:
        name=window.login_name.get()
        password=window.login_pass.get()
        admin=window.admin

    screen=window.screen
    #print(screen)
    

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
    elif screen==1:
    	window=user_dashboard(root, admin)
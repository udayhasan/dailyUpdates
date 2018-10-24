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
    	self.login_cur  = self.login_conn.cursor()
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
        login_name_entry.focus_set()

        login_pass_label=Label(self,text="Password:")
        login_pass_label.grid(row=3,column=0,sticky=E)

        self.login_pass=StringVar()
        login_pass_entry=Entry(self,textvariable=self.login_pass,show="*")
        login_pass_entry.grid(row=3,column=1,columnspan=3,sticky=W)

        forgot_id_label=Label(self,text="Forgot User ID?", fg = "blue", underline=True)
        forgot_id_label.bind('<Button-1>',self.forgot_id)
        forgot_id_label.grid(row=4,column=1,sticky=W)

        forgot_pass_label=Label(self,text="Forgot Password?", fg = "blue", underline=True)
        forgot_pass_label.bind('<Button-1>',self.forgot_password)
        forgot_pass_label.grid(row=5,column=1,sticky=E)

        login_btn=Button(self,text="Login", bg="DeepSkyBlue4", fg = "white", command=self.login_action)
        login_btn.grid(row=6,column=2,sticky=W)

        exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
        exit.grid(row=6,column=1,sticky=W)

    def login_action(self):
    	self.create_user_table()
    	success, self.admin = self.login(self.login_name.get(), self.login_pass.get())
    	
    	if(success ==1): self.screen = 1
    	else: self.screen = 0

    	print(self.screen)

    	self.quit()

    def forgot_id(self,event):
    	self.screen = 12
    	self.quit()

    def forgot_password(self,event):
    	self.screen = 7
    	self.quit()

    def leave(self):
        quit()

class user_dashboard(Frame):

	screen = 1
	admin  = 0

	def __init__(self,master,admin):
		super(user_dashboard,self).__init__(master)
		self.grid()
		self.admin = admin
		self.define_widgets()

	def define_widgets(self):

		dash_board_label=Label(self,text="::Dashboard::")
		dash_board_label.grid(row=0,column=0,columnspan=2,sticky=W)

		log_out=Button(self,text="Log Out",command=self.set_logout, bg="DeepSkyBlue4", fg = "white")
		log_out.grid(row=6,column=1,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=6,column=2,sticky=W)

		edit_name_btn=Button(self,text="Edit User Name",command=lambda: self.set_value(3), width = 16, height=4, bd=4, bg="aquamarine2")
		edit_name_btn.grid(row=1,column=1,sticky=W)

		edit_email_btn=Button(self,text="Edit User Email",command=lambda: self.set_value(4), width = 16, height=4, bd=4, bg="gold2")
		edit_email_btn.grid(row=1,column=2,sticky=W)

		edit_pass_btn=Button(self,text="Edit User Password",command=lambda: self.set_value(5), width = 16, height=4, bd=4, bg="magenta3")
		edit_pass_btn.grid(row=2,column=1,sticky=W)

		update_status_btn=Button(self,text="Update Status",command=lambda: self.set_value(8), width = 16, height=4, bd=4, bg="cyan3")
		update_status_btn.grid(row=2,column=2,sticky=W)

		edit_status_btn=Button(self,text="Edit Status",command=lambda: self.set_value(9), width = 16, height=4, bd=4, bg="PaleGreen2")
		edit_status_btn.grid(row=3,column=1,sticky=W)

		if(self.admin == 1):
			add_user_btn=Button(self,text="Add User",command=lambda: self.set_value(2), width = 16, height=4, bd=4, bg="medium orchid")
			add_user_btn.grid(row=3,column=2,sticky=W)

			delete_user_btn=Button(self,text="Delete User",command=lambda: self.set_value(6), width = 16, height=4, bd=4, bg="LightSteelBlue3")
			delete_user_btn.grid(row=4,column=1,sticky=W)

			export_report_btn=Button(self,text="Export Report",command=lambda: self.set_value(10), width = 16, height=4, bd=4, bg="turquoise")
			export_report_btn.grid(row=4,column=2,sticky=W)

			backup_btn=Button(self,text="Backup",command=lambda: self.set_value(11), width = 16, height=4, bd=4, bg="yellow")
			backup_btn.grid(row=5,column=1,sticky=W)

	def set_logout(self):
		self.screen = 0
		self.quit()

	def set_value(self, value):
		self.screen = value
		print(self.screen)
		self.quit()

	def leave(self):
		quit()

class add_user_page(Frame):
	screen = 2
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(add_user_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		add_page_label=Label(self,text="Add User Page")
		add_page_label.grid(row=0,column=1,columnspan=2,sticky=W)

		add_name_label=Label(self,text="User Name:")
		add_name_label.grid(row=2,column=0,sticky=E)

		self.add_name=StringVar()
		add_name_entry=Entry(self,textvariable=self.add_name)
		add_name_entry.grid(row=2,column=1,columnspan=3,sticky=W)
		add_name_entry.focus_set()

		add_email_label=Label(self,text="User Email:")
		add_email_label.grid(row=3,column=0,sticky=E)

		self.add_email=StringVar()
		add_email_entry=Entry(self,textvariable=self.add_email)
		add_email_entry.grid(row=3,column=1,columnspan=3,sticky=W)

		add_pass_label=Label(self,text="Password:")
		add_pass_label.grid(row=4,column=0,sticky=E)

		self.add_pass=StringVar()
		add_pass_entry=Entry(self,textvariable=self.add_pass)
		add_pass_entry.grid(row=4,column=1,columnspan=3,sticky=W)

		add_btn=Button(self,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.add_user)
		add_btn.grid(row=5,column=2,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=5,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=5,column=1,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def add_user(self):
		self.create_user_table()
		if(self.add_name.get() == '' or self.add_email.get() == '' or self.add_pass.get() == ''):
			error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("SELECT name, email FROM users")
				user_details = self.login_cur.fetchall()
				user_names  = [user_details[i][0] for i in range(len(user_details))]
				user_emails = [user_details[i][1] for i in range(len(user_details))]

				print(user_names, user_emails)

				if((self.add_name.get() not in user_names) and (self.add_email.get() not in user_emails)):
					self.login_cur.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", (self.add_name.get(), self.add_email.get(), self.add_pass.get()))
					self.login_conn.commit()
					time.sleep(0.02)
					self.login_conn.close()
					print("New User named %s is added to the database" %(self.add_name.get()))
					self.screen = 2
					self.quit()
				else:
					self.error_msg = "You cannot add this User Name/Email, already exists!"
					self.screen = 2
					self.quit()
			except Exception as e:
				error_msg = "Invalid input"
				print(e)

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class edit_user_name_page(Frame):
	screen = 3
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(edit_user_name_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		edit_name_label=Label(self,text="Edit User Name")
		edit_name_label.grid(row=0,column=1,columnspan=2,sticky=W)

		edit_name_cur_label=Label(self,text="Current User Name:")
		edit_name_cur_label.grid(row=1,column=0,sticky=E)

		self.edit_name_cur=StringVar()
		edit_name_cur_entry=Entry(self,textvariable=self.edit_name_cur)
		edit_name_cur_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		edit_name_cur_entry.focus_set()

		edit_name_new_label=Label(self,text="New User Name:")
		edit_name_new_label.grid(row=2,column=0,sticky=E)

		self.edit_name_new=StringVar()
		edit_name_new_entry=Entry(self,textvariable=self.edit_name_new)
		edit_name_new_entry.grid(row=2,column=1,columnspan=3,sticky=W)
		edit_name_new_entry.focus_set()

		edit_name_btn=Button(self,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_name)
		edit_name_btn.grid(row=3,column=2,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=3,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=3,column=1,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_name(self):
		self.create_user_table()
		if(self.edit_name_cur.get() == '' or self.edit_name_new.get() == ''):
			self.error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("UPDATE users SET name = ? WHERE name = ?", (self.edit_name_new.get(), self.edit_name_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("User name %s is replaced by %s" %(self.edit_name_cur.get(), self.edit_name_new.get()))
			except Exception:
				self.error_msg = "Invalid search name or replacing name!"

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class edit_user_email_page(Frame):
	screen = 4
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(edit_user_email_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		edit_email_label=Label(self,text="Edit User Email")
		edit_email_label.grid(row=0,column=1,columnspan=2,sticky=W)

		edit_name_cur_label=Label(self,text="User Name:")
		edit_name_cur_label.grid(row=1,column=0,sticky=E)

		self.edit_name_cur=StringVar()
		edit_name_cur_entry=Entry(self,textvariable=self.edit_name_cur)
		edit_name_cur_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		edit_name_cur_entry.focus_set()

		edit_email_new_label=Label(self,text="New User Email:")
		edit_email_new_label.grid(row=2,column=0,sticky=E)

		self.edit_email_new=StringVar()
		edit_email_new_entry=Entry(self,textvariable=self.edit_email_new)
		edit_email_new_entry.grid(row=2,column=1,columnspan=3,sticky=W)
		edit_email_new_entry.focus_set()

		edit_email_btn=Button(self,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_email)
		edit_email_btn.grid(row=3,column=2,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=3,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=3,column=1,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_email(self):
		self.create_user_table()
		if(self.edit_name_cur.get() == '' or self.edit_email_new.get() == ''):
			self.error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("UPDATE users SET email = ? WHERE name = ?", (self.edit_email_new.get(), self.edit_name_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("User email of %s is replaced by %s" %(self.edit_name_cur.get(), self.edit_email_new.get()))
			except Exception:
				self.error_msg = "Invalid search name or replacing name!"

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class edit_user_pass_page(Frame):
	screen = 5
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(edit_user_pass_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		edit_pass_label=Label(self,text="Edit User Password")
		edit_pass_label.grid(row=0,column=1,columnspan=2,sticky=W)

		edit_name_cur_label=Label(self,text="User Name:")
		edit_name_cur_label.grid(row=1,column=0,sticky=E)

		self.edit_name_cur=StringVar()
		edit_name_cur_entry=Entry(self,textvariable=self.edit_name_cur)
		edit_name_cur_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		edit_name_cur_entry.focus_set()

		edit_pass_cur_label=Label(self,text="Current Password:")
		edit_pass_cur_label.grid(row=2,column=0,sticky=E)

		self.edit_pass_cur=StringVar()
		edit_pass_cur_entry=Entry(self,textvariable=self.edit_pass_cur)
		edit_pass_cur_entry.grid(row=2,column=1,columnspan=3,sticky=W)
		edit_pass_cur_entry.focus_set()

		edit_pass_new_label=Label(self,text="New Password:")
		edit_pass_new_label.grid(row=3,column=0,sticky=E)

		self.edit_pass_new=StringVar()
		edit_pass_new_entry=Entry(self,textvariable=self.edit_pass_new)
		edit_pass_new_entry.grid(row=3,column=1,columnspan=3,sticky=W)
		edit_pass_new_entry.focus_set()

		edit_pass_btn=Button(self,text="Change Password", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_password)
		edit_pass_btn.grid(row=4,column=2,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=4,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=4,column=1,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_password(self):
		self.create_user_table()
		if(self.edit_name_cur.get() == '' or self.edit_pass_cur.get() == '' or self.edit_pass_new.get() == ''):
			self.error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("UPDATE users SET password = ? WHERE name = ? and password = ?", (self.edit_pass_new.get(), self.edit_name_cur.get(), self.edit_pass_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("Password for %s is changed successfully!" %(name))
			except Exception:
				self.error_msg = "Invalid search name or previous password or new password!"


	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class delete_user_page(Frame):
	screen = 6
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(delete_user_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		delete_user_label=Label(self,text="Delete User")
		delete_user_label.grid(row=0,column=1,columnspan=2,sticky=W)

		delete_user_name_label=Label(self,text="User Name:")
		delete_user_name_label.grid(row=1,column=0,sticky=E)

		self.delete_user_name=StringVar()
		delete_user_name_entry=Entry(self,textvariable=self.delete_user_name)
		delete_user_name_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		delete_user_name_entry.focus_set()

		delete_user_btn=Button(self,text="Delete User", bg="DeepSkyBlue4", fg = "white", command=self.delete_user)
		delete_user_btn.grid(row=1,column=2,sticky=W)

		refresh_user_btn=Button(self,text="Refresh",command=self.refresh_user)
		refresh_user_btn.grid(row=2,column=2,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=2,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=2,column=1,sticky=W)

		temp = Label(self,relief=RIDGE, bg="light blue")
		temp.configure(text="Current Users")
		temp.grid(row=5, column=0, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue")
		temp.configure(text="Email")
		temp.grid(row=5, column=1, sticky=NSEW)

		self.create_user_table()
		self.login_cur.execute("SELECT name, email FROM users")
		data = self.login_cur.fetchall()

		for i in range(len(data)):
			temp = Label(self,relief=RIDGE, bg="white")
			temp.configure(text="%s" %(data[i][0]))
			temp.grid(row=6+i, column=0, sticky=NSEW)
			temp = Label(self,relief=RIDGE, text=data[i][1], bg="white")
			temp.configure(text="%s" %(data[i][1]))
			temp.grid(row=6+i, column=1, sticky=NSEW)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def delete_user(self):
		self.create_user_table()
		if(self.delete_user_name.get() == ''):
			self.error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("DELETE FROM users WHERE name = ?", (self.delete_user_name.get(),))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("User named %s has been deleted successfully!" %(self.delete_user_name.get()))
				self.screen = 6
				self.quit()
			except Exception:
				self.error_msg = "Invalid search name!"

	def refresh_user(self):
		self.screen = 6
		self.quit()

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class forgot_pass_page(Frame):
	screen = 7
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master):
		super(forgot_pass_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		forgot_user_password=Label(self,text="Forgot Password?")
		forgot_user_password.grid(row=0,column=1,columnspan=2,sticky=W)

		forgot_pass_name=Label(self,text="User Name:")
		forgot_pass_name.grid(row=1,column=0,sticky=E)

		self.forgot_pass_name=StringVar()
		forgot_pass_name_entry=Entry(self,textvariable=self.forgot_pass_name)
		forgot_pass_name_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		forgot_pass_name_entry.focus_set()

		forgot_pass_email=Label(self,text="Email:")
		forgot_pass_email.grid(row=2,column=0,sticky=E)

		self.forgot_pass_email=StringVar()
		forgot_pass_email_entry=Entry(self,textvariable=self.forgot_pass_email)
		forgot_pass_email_entry.grid(row=2,column=1,columnspan=3,sticky=W)
		forgot_pass_email_entry.focus_set()

		forgot_pass_btn=Button(self,text="Send Password", bg="DeepSkyBlue4", fg = "white", command=self.forgot_pass_send)
		forgot_pass_btn.grid(row=3,column=1,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=3,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=3,column=2,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def forgot_pass_send(self):
		self.create_user_table()
		if(self.forgot_pass_name.get() == '' or self.forgot_pass_email.get() == ''):
			self.error_msg = "Invalid input!"
		else:
			try:
				self.login_cur.execute("SELECT password FROM users WHERE name = ? and email = ?", (self.forgot_pass_name.get(), self.forgot_pass_email.get()))
				password = self.login_cur.fetchall()
	
				me  	= "noreply.nslstatus@gmail.com"
				you 	= self.forgot_pass_email.get()
				body 	= "Dear "+name+",\nYour lost password is :"+str(password[0][0])+"\nN.B: You don't need to reply this message.\nThanks.\n"+time.asctime(time.localtime(time.time()))
	
				server  = smtplib.SMTP("smtp.gmail.com", 25)
				server.ehlo()
				server.starttls()
				server.login(me, 'a1234567890z')
				server.sendmail(me, you, body)
				server.quit()
				self.login_conn.close()
				print("Mail sent successfully!")
	
			except Exception:
				self.error_msg = "Invalid search name or email!"

	def go_prev(self):
		self.screen = 0
		self.quit()

	def leave(self):
		quit()

class update_status_page(Frame):
	screen = 8
	status_conn = None
	status_cur  = None
	name 		= None

	error_msg  = " "

	def __init__(self,master, name):
		super(update_status_page,self).__init__(master)
		self.status_conn = sqlite3.connect('status.db')
		self.status_cur  = self.status_conn.cursor()
		self.name 		 = name
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		update_status_label=Label(self,text="Update Status")
		update_status_label.grid(row=0,column=1,columnspan=2,sticky=W)

		#Team
		team_label=Label(self,text="Team Name:")
		team_label.grid(row=1,column=0,sticky=E)

		self.team=StringVar()
		team_entry=Entry(self,textvariable=self.team)
		team_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		team_entry.focus_set()

		#Task List
		task_list_label=Label(self,text="Task List:")
		task_list_label.grid(row=2,column=0,sticky=E)

		self.task_list=StringVar()
		task_list_entry=Entry(self,textvariable=self.task_list)
		task_list_entry.grid(row=2,column=1,columnspan=3,sticky=W)

		#Progress Status
		progress_status_label=Label(self,text="Progress Status:")
		progress_status_label.grid(row=3,column=0,sticky=E)

		self.progress_status=StringVar()
		progress_status_entry=Entry(self,textvariable=self.progress_status)
		progress_status_entry.grid(row=3,column=1,columnspan=3,sticky=W)

		#Meeting Status
		meeting_status_label=Label(self,text="Meeting Status:")
		meeting_status_label.grid(row=4,column=0,sticky=E)

		self.meeting_status=StringVar()
		meeting_status_entry=Entry(self,textvariable=self.meeting_status)
		meeting_status_entry.grid(row=4,column=1,columnspan=3,sticky=W)

		#Project Status
		project_status_label=Label(self,text="Project Status:")
		project_status_label.grid(row=5,column=0,sticky=E)

		self.project_status=StringVar()
		project_status_entry=Entry(self,textvariable=self.project_status)
		project_status_entry.grid(row=5,column=1,columnspan=3,sticky=W)

		#Remarks
		remarks_label=Label(self,text="Remarks:")
		remarks_label.grid(row=6,column=0,sticky=E)

		self.remarks=StringVar()
		remarks_entry=Entry(self,textvariable=self.remarks)
		remarks_entry.grid(row=6,column=1,columnspan=3,sticky=W)

		update_status_btn=Button(self,text="Update Status", bg="DeepSkyBlue4", fg = "white", command=self.update_status)
		update_status_btn.grid(row=7,column=1,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=7,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=7,column=2,sticky=W)

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")
	
	def update_status(self):
		if(self.task_list.get() == '' and self.team.get() == ''):
			self.error_msg = "Insufficient inputs!"
		else:
			try:
				self.create_status_table()

				ids 	= str(time.time()).split(".")[0]+str(time.time()).split(".")[1]+self.name
				dates 	= datetime.datetime.now().strftime("%d-%b-%Y")
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks 	= datetime.datetime.now().strftime("%U")
				months 	= datetime.datetime.now().strftime("%b")
				years 	= datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("INSERT INTO status(ids, dates, up_time, weeks, months, years, name, team, task_list, progress_status, meeting_status, project_status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ids, dates, up_time, weeks, months, years, self.name, self.team.get(), self.task_list.get(), self.progress_status.get(), self.meeting_status.get(), self.project_status.get(), self.remarks.get()))
				self.status_conn.commit()
				time.sleep(0.02)
				self.status_conn.close()
				print("%s, You have successfully updated your daily status!" %(self.name))
				self.screen = 8
				self.quit()
			except Exception as e:
				print(e)
				self.error_msg = "Invalid inputs!"
		print(self.error_msg)
	
	
	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()	

class edit_status_page(Frame):
	screen = 9
	status_conn = None
	status_cur  = None
	name 		= None

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_status_page,self).__init__(master)
		self.status_conn = sqlite3.connect('status.db')
		self.status_cur  = self.status_conn.cursor()
		self.name 		 = name
		self.grid()
		self.define_widgets()

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")

	def define_widgets(self):
		edit_status_label=Label(self,text="Update Status")
		edit_status_label.grid(row=0,column=1,columnspan=2,sticky=W)

		#ID
		status_id_label=Label(self,text="Status ID:")
		status_id_label.grid(row=1,column=0,sticky=E)

		self.status_id=StringVar()
		status_entry=Entry(self,textvariable=self.status_id)
		status_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		status_entry.focus_set()

		edit_status_btn=Button(self,text="Edit Status", bg="DeepSkyBlue4", fg = "white", command=self.edit_status_window)
		edit_status_btn.grid(row=1,column=5,sticky=W)

		delete_status_btn=Button(self,text="Delete Status", bg="DeepSkyBlue4", fg = "white", command=self.delete_status_window)
		delete_status_btn.grid(row=1,column=4,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=2,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=2,column=2,sticky=W)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Status ID")
		temp.grid(row=4, column=0, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Date")
		temp.grid(row=4, column=1, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Time")
		temp.grid(row=4, column=2, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Team")
		temp.grid(row=4, column=3, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Task List")
		temp.grid(row=4, column=4, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Progress Status")
		temp.grid(row=4, column=5, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Meeting Status")
		temp.grid(row=4, column=6, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Project Status")
		temp.grid(row=4, column=7, sticky=NSEW)

		temp = Label(self,relief=RIDGE, bg="light blue", text="Remarks")
		temp.grid(row=4, column=8, sticky=NSEW)

		self.create_status_table()
		self.status_cur.execute("SELECT ids, dates, up_time, team, task_list, progress_status, meeting_status, project_status, remarks FROM status WHERE name = ?", (self.name,))
		data = self.status_cur.fetchall()

		for i in range(len(data)):
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][0])
			temp.grid(row=5+i, column=0, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][1])
			temp.grid(row=5+i, column=1, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][2])
			temp.grid(row=5+i, column=2, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][3])
			temp.grid(row=5+i, column=3, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][4])
			temp.grid(row=5+i, column=4, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][5])
			temp.grid(row=5+i, column=5, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][6])
			temp.grid(row=5+i, column=6, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][7])
			temp.grid(row=5+i, column=7, sticky=NSEW)
	
			temp = Label(self,relief=RIDGE, bg="light blue")
			temp.configure(text=data[i][8])
			temp.grid(row=5+i, column=8, sticky=NSEW)

	def delete_status_window(self, id):
		self.create_status_table()
		if(self.status_id.get() == ''):
			self.error_msg = "Invalid Status ID!"
		else:
			try:
				self.status_cur.execute("DELETE FROM status WHERE ids = ?", (self.status_id.get(),))
				self.status_conn.commit()
				time.sleep(0.02)
				print("Status corresponding to ID %s has been deleted successfully!" %(self.status_id.get()))
				self.screen = 9
				self.quit()
			except Exception:
				self.error_msg = "Invalid search name!"

	def edit_status_window(self):
		#Team
		team_label=Label(self,text="Team Name:")
		team_label.grid(row=1,column=0,sticky=E)

		self.team=StringVar()
		team_entry=Entry(self,textvariable=self.team)
		team_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		team_entry.focus_set()

		#Task List
		task_list_label=Label(self,text="Task List:")
		task_list_label.grid(row=2,column=0,sticky=E)

		self.task_list=StringVar()
		task_list_entry=Entry(self,textvariable=self.task_list)
		task_list_entry.grid(row=2,column=1,columnspan=3,sticky=W)

		#Progress Status
		progress_status_label=Label(self,text="Progress Status:")
		progress_status_label.grid(row=3,column=0,sticky=E)

		self.progress_status=StringVar()
		progress_status_entry=Entry(self,textvariable=self.progress_status)
		progress_status_entry.grid(row=3,column=1,columnspan=3,sticky=W)

		#Meeting Status
		meeting_status_label=Label(self,text="Meeting Status:")
		meeting_status_label.grid(row=4,column=0,sticky=E)

		self.meeting_status=StringVar()
		meeting_status_entry=Entry(self,textvariable=self.meeting_status)
		meeting_status_entry.grid(row=4,column=1,columnspan=3,sticky=W)

		#Project Status
		project_status_label=Label(self,text="Project Status:")
		project_status_label.grid(row=5,column=0,sticky=E)

		self.project_status=StringVar()
		project_status_entry=Entry(self,textvariable=self.project_status)
		project_status_entry.grid(row=5,column=1,columnspan=3,sticky=W)

		#Remarks
		remarks_label=Label(self,text="Remarks:")
		remarks_label.grid(row=6,column=0,sticky=E)

		self.remarks=StringVar()
		remarks_entry=Entry(self,textvariable=self.remarks)
		remarks_entry.grid(row=6,column=1,columnspan=3,sticky=W)

		update_status_btn=Button(self,text="Update Status", bg="DeepSkyBlue4", fg = "white", command=self.update_status)
		update_status_btn.grid(row=7,column=1,sticky=W)

	def update_status(self):
		if(self.task_list.get() == '' and self.team.get() == ''):
			self.error_msg = "Insufficient inputs!"
		else:
			try:
				self.create_status_table()

				ids 	= str(time.time()).split(".")[0]+str(time.time()).split(".")[1]+self.name
				dates 	= datetime.datetime.now().strftime("%d-%b-%Y")
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks 	= datetime.datetime.now().strftime("%U")
				months 	= datetime.datetime.now().strftime("%b")
				years 	= datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("INSERT INTO status(ids, dates, up_time, weeks, months, years, name, team, task_list, progress_status, meeting_status, project_status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ids, dates, up_time, weeks, months, years, self.name, self.team.get(), self.task_list.get(), self.progress_status.get(), self.meeting_status.get(), self.project_status.get(), self.remarks.get()))
				self.status_conn.commit()
				time.sleep(0.02)
				self.status_conn.close()
				print("%s, You have successfully updated your daily status!" %(self.name))
				self.screen = 8
				self.quit()
			except Exception as e:
				print(e)
				self.error_msg = "Invalid inputs!"
		print(self.error_msg)
	
	
	def go_prev(self):
		self.status_conn.close()
		self.screen = 1
		self.quit()

	def leave(self):
		self.status_conn.close()
		quit()	

class forgot_id_page(Frame):
	screen = 12
	login_conn = None
	login_cur  = None
	forgot_id_name_label = None

	error_msg  = " "

	def __init__(self,master):
		super(forgot_id_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.grid()
		self.define_widgets()

	def define_widgets(self):
		forgot_user_id=Label(self,text="Forgot User ID?")
		forgot_user_id.grid(row=0,column=1,columnspan=2,sticky=W)

		forgot_id_email=Label(self,text="Email:")
		forgot_id_email.grid(row=1,column=0,sticky=E)

		self.forgot_id_email=StringVar()
		forgot_id_email_entry=Entry(self,textvariable=self.forgot_id_email)
		forgot_id_email_entry.grid(row=1,column=1,columnspan=3,sticky=W)
		forgot_id_email_entry.focus_set()

		forgot_id_btn=Button(self,text="Find User Name", bg="DeepSkyBlue4", fg = "white", command=self.pre_forgot_id_find)
		forgot_id_btn.grid(row=2,column=1,sticky=W)

		back=Button(self,text="< Prev", command=self.go_prev)
		back.grid(row=2,column=0,sticky=W)

		exit=Button(self,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.grid(row=2,column=2,sticky=W)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def pre_forgot_id_find(self):
		self.forgot_id_name_label=Label(self, relief=RIDGE, fg="RED", text="<User ID>", state=DISABLED)
		self.forgot_id_name_label.grid(row=3,column=1,sticky=W)
		self.forgot_id_find()

	def forgot_id_find(self):
		self.create_user_table()
		if(self.forgot_id_email.get() == ''):
			self.error_msg = "Invalid input!"
			self.screen = 12
			self.quit()
		else:
			try:
				self.login_cur.execute("SELECT name FROM users WHERE email = ?", (self.forgot_id_email.get(),))
				id_name = self.login_cur.fetchall()
				self.forgot_id_name_label.configure(text="Your ID is: "+str(id_name[0][0]), state=ACTIVE)
			except Exception as e:
				self.error_msg = "No such email address!"
				print(e)

	def go_prev(self):
		self.login_conn.close()
		self.screen = 0
		self.quit()

	def leave(self):
		self.login_conn.close()
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
    elif screen==2:
    	window=add_user_page(root)
    elif screen==3:
    	window=edit_user_name_page(root)
    elif screen==4:
    	window=edit_user_email_page(root)
    elif screen==5:
    	window=edit_user_pass_page(root)
    elif screen==6:
    	window=delete_user_page(root)
    elif screen==7:
    	window=forgot_pass_page(root)
    elif screen==8:
    	window=update_status_page(root, name)
    elif screen==9:
    	window=edit_status_page(root, name)
    elif screen==12:
    	window=forgot_id_page(root)
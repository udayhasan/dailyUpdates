#!/usr/bin/python3
import sqlite3
import smtplib
import time
import datetime
from tkinter import *

class login_page(Frame):

	screen     = 0

	login_conn = None
	login_cur  = None

	error_msg  = " "
	admin      = None

	def __init__(self,master):
		super(login_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
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
		#for line1:
		frame1=Frame(self)
		frame1.pack()

		login_page_label=Label(frame1,text="::Login Page::")
		login_page_label.config(width=200, font=("Courier", 25))
		login_page_label.pack(pady=10)

		#for line2:
		frame2=Frame(self)
		frame2.pack()

		login_name_label=Label(frame2,text="User ID:", anchor=W)
		login_name_label.config(width=10, height=1)
		login_name_label.pack(side=LEFT, pady=5)

		self.login_name=StringVar()
		login_name_entry=Entry(frame2,textvariable=self.login_name)
		login_name_entry.config(width=25)
		login_name_entry.pack(side=LEFT, pady=5)
		login_name_entry.focus_set()

		#for line3:
		frame3=Frame(self)
		frame3.pack()
		login_pass_label=Label(frame3,text="Password:", anchor=W)
		login_pass_label.config(width=10, height=1)
		login_pass_label.pack(side=LEFT, pady=5)

		self.login_pass=StringVar()
		login_pass_entry=Entry(frame3,textvariable=self.login_pass,show="*")
		login_pass_entry.config(width=25)
		login_pass_entry.pack(side=LEFT, pady=5)

		#forline5:
		frame5=Frame(self)
		frame5.pack()
		login_btn=Button(frame5,text="Login", bg="DeepSkyBlue4", fg = "white", command=self.login_action)
		login_btn.pack(side=LEFT, pady=5)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT, pady=5)

		#for line4:
		frame4=Frame(self)
		frame4.pack()

		forgot_id_label=Label(frame4,text="Forgot User ID?", fg = "blue", underline=True)
		forgot_id_label.bind('<Button-1>',self.forgot_id)
		forgot_id_label.pack(side=LEFT)

		forgot_pass_label=Label(frame4,text="Forgot Password?", fg = "blue", underline=True)
		forgot_pass_label.bind('<Button-1>',self.forgot_password)
		forgot_pass_label.pack(side=LEFT)

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
		self.pack()
		self.admin = admin
		self.define_widgets()

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Dashboard::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#for line2:
		frame2 = Frame(self)
		frame2.pack()

		if(self.admin == 0):
			edit_name_btn=Button(frame2,text="Edit User Name",command=lambda: self.set_value(3), width = 16, height=4, bd=4, bg="aquamarine2")
			edit_name_btn.pack(side=LEFT, padx=2, pady=2)

		edit_email_btn=Button(frame2,text="Edit User Email",command=lambda: self.set_value(4), width = 16, height=4, bd=4, bg="gold2")
		edit_email_btn.pack(side=LEFT, padx=2, pady=2)

		edit_pass_btn=Button(frame2,text="Edit User Password",command=lambda: self.set_value(5), width = 16, height=4, bd=4, bg="magenta3")
		edit_pass_btn.pack(side=LEFT, padx=2, pady=2)

		update_status_btn=Button(frame2,text="Update Status",command=lambda: self.set_value(8), width = 16, height=4, bd=4, bg="cyan3")
		update_status_btn.pack(side=LEFT, padx=2, pady=2)

		edit_status_btn=Button(frame2,text="Edit Status",command=lambda: self.set_value(9), width = 16, height=4, bd=4, bg="PaleGreen2")
		edit_status_btn.pack(side=LEFT, padx=2, pady=2)

		if(self.admin == 1):
			#for line3:
			frame3 = Frame(self)
			frame3.pack()
			add_user_btn=Button(frame3,text="Add User",command=lambda: self.set_value(2), width = 16, height=4, bd=4, bg="medium orchid")
			add_user_btn.pack(side=LEFT, padx=2, pady=2)

			delete_user_btn=Button(frame3,text="Delete User",command=lambda: self.set_value(6), width = 16, height=4, bd=4, bg="LightSteelBlue3")
			delete_user_btn.pack(side=LEFT, padx=2, pady=2)

			export_report_btn=Button(frame3,text="Export Report",command=lambda: self.set_value(10), width = 16, height=4, bd=4, bg="turquoise")
			export_report_btn.pack(side=LEFT, padx=2, pady=2)

			backup_btn=Button(frame3,text="Backup",command=lambda: self.set_value(11), width = 16, height=4, bd=4, bg="yellow")
			backup_btn.pack(side=LEFT, padx=2, pady=2)

		#for line4
		frame4 = Frame(self)
		frame4.pack()
		log_out=Button(frame4,text="Log Out",command=self.set_logout, bg="DeepSkyBlue4", fg = "white", width = 16, height=4, bd=4)
		log_out.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width = 16, height=4, bd=4)
		exit.pack(side=LEFT, padx=2, pady=2)

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
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack(pady=5)
		add_page_label=Label(frame1,text="::Add User::")
		add_page_label.config(width=200, font=("Courier", 25))
		add_page_label.pack()

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		add_name_label=Label(frame2,text="User Name:", width=13, anchor=W)
		add_name_label.pack(side=LEFT, padx=2, pady=2)

		self.add_name=StringVar()
		add_name_entry=Entry(frame2,textvariable=self.add_name, width=40)
		add_name_entry.pack(side=LEFT, padx=2, pady=2)
		add_name_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		add_email_label=Label(frame3,text="User Email:", width=13, anchor=W)
		add_email_label.pack(side=LEFT, padx=2, pady=2)

		self.add_email=StringVar()
		add_email_entry=Entry(frame3,textvariable=self.add_email, width=40)
		add_email_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		add_pass_label=Label(frame4,text="Password:", width=13, anchor=W)
		add_pass_label.pack(side=LEFT, padx=2, pady=2)

		self.add_pass=StringVar()
		add_pass_entry=Entry(frame4,textvariable=self.add_pass, width=40)
		add_pass_entry.pack(side=LEFT, padx=2, pady=2)

		frame5 = Frame(self)
		frame5.pack()

		add_btn=Button(frame5,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.add_user)
		add_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame5,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT, padx=2, pady=2)

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

	def __init__(self,master, name):
		super(edit_user_name_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name       = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_name_label=Label(frame1,text="::Edit Profile::")
		edit_name_label.config(width=200, font=("Courier", 25))
		edit_name_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()
		edit_name_cur_label=Label(frame2,text="Current User Name:", width=20, anchor=W)
		edit_name_cur_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_name_cur=StringVar()
		edit_name_cur_entry=Entry(frame2,textvariable=self.edit_name_cur, width=40)
		self.edit_name_cur.set(self.name)
		edit_name_cur_entry.pack(side=LEFT, padx=2, pady=2)
		edit_name_cur_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()
		edit_name_new_label=Label(frame3,text="New User Name:", width=20, anchor=W)
		edit_name_new_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_name_new=StringVar()
		edit_name_new_entry=Entry(frame3,textvariable=self.edit_name_new, width=40)
		edit_name_new_entry.pack(side=LEFT, padx=2, pady=2)
		edit_name_new_entry.focus_set()

		frame4 = Frame(self)
		frame4.pack()
		edit_name_btn=Button(frame4,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_name, width=10)
		edit_name_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame4,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_name(self):
		self.create_user_table()
		if(self.edit_name_cur.get() == '' or self.edit_name_new.get() == ''):
			self.error_msg = "Invalid input!"
		elif(self.edit_name_cur.get() == 'admin' or self.edit_name_new.get() == 'admin'):
			self.error_msg = "You cannot change admin name!"
		else:
			try:
				self.login_cur.execute("UPDATE users SET name = ? WHERE name = ?", (self.edit_name_new.get(), self.edit_name_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("User name %s is replaced by %s" %(self.edit_name_cur.get(), self.edit_name_new.get()))
				self.screen = 3
				self.quit()
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
		self.pack()
		self.define_widgets()

	def define_widgets(self):

		frame1 = Frame(self)
		frame1.pack()
		edit_email_label=Label(frame1,text="::Edit Email Address::")
		edit_email_label.config(width=200, font=("Courier", 25))
		edit_email_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		edit_name_cur_label=Label(frame2,text="User Name:", width=20, anchor=W)
		edit_name_cur_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_name_cur=StringVar()
		edit_name_cur_entry=Entry(frame2,textvariable=self.edit_name_cur, width=40)
		edit_name_cur_entry.pack(side=LEFT, padx=2, pady=2)
		edit_name_cur_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		edit_email_new_label=Label(frame3,text="New User Email:", width=20, anchor=W)
		edit_email_new_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_email_new=StringVar()
		edit_email_new_entry=Entry(frame3,textvariable=self.edit_email_new, width=40)
		edit_email_new_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		edit_email_btn=Button(frame4,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_email, width=10)
		edit_email_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame4,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

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
				self.screen = 4
				self.quit()
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

	def __init__(self,master, name):
		super(edit_user_pass_page,self).__init__(master)
		self.login_conn = sqlite3.connect('users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_pass_label=Label(frame1,text="::Edit User Password::")
		edit_pass_label.config(width=200, font=("Courier", 25))
		edit_pass_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame3 = Frame(self)
		frame3.pack()

		edit_pass_cur_label=Label(frame3,text="Current Password:", width=20, anchor=W)
		edit_pass_cur_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_cur=StringVar()
		edit_pass_cur_entry=Entry(frame3,textvariable=self.edit_pass_cur, width=40, show="*")
		edit_pass_cur_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		edit_pass_new_label=Label(frame4,text="New Password:", width=20, anchor=W)
		edit_pass_new_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_new=StringVar()
		edit_pass_new_entry=Entry(frame4,textvariable=self.edit_pass_new, width=40, show="*")
		edit_pass_new_entry.pack(side=LEFT, padx=2, pady=2)

		frame2 = Frame(self)
		frame2.pack()

		edit_pass_confirm_label=Label(frame2,text="Confirm Password:", width=20, anchor=W)
		edit_pass_confirm_label.pack(side=LEFT, padx=2, pady=2)

		self.edit_pass_confirm=StringVar()
		edit_pass_confirm_entry=Entry(frame2,textvariable=self.edit_pass_confirm, width=40, show="*")
		edit_pass_confirm_entry.pack(side=LEFT, padx=2, pady=2)

		frame5 = Frame(self)
		frame5.pack()

		edit_pass_btn=Button(frame5,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.edit_user_password, width=10)
		edit_pass_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame5,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def edit_user_password(self):
		self.create_user_table()
		if(self.edit_pass_confirm.get() == '' or self.edit_pass_cur.get() == '' or self.edit_pass_new.get() == ''):
			self.error_msg = "Invalid input!"
		elif(self.edit_pass_confirm.get() == self.edit_pass_new.get()):
			try:
				self.login_cur.execute("UPDATE users SET password = ? WHERE name = ? and password = ?", (self.edit_pass_new.get(), self.name, self.edit_pass_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("Password for %s is changed successfully!" %(name))
			except Exception:
				self.error_msg = "Invalid search name or previous password or new password!"
		else:
			self.error_msg = "Your password is not confirmed correctly!"


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
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		delete_user_label=Label(self,text="Delete User")
		delete_user_label.pack(fill=X, padx=10, pady=10)

		#frame for line1:
		frame1 = Frame(self)
		frame1.pack()
		delete_user_name_label=Label(frame1,text="User Name:")
		delete_user_name_label.pack(side=LEFT)

		self.delete_user_name=StringVar()
		self.delete_user_name_entry=Entry(frame1,textvariable=self.delete_user_name)
		self.delete_user_name_entry.pack(side=LEFT)

		delete_user_btn=Button(frame1,text="Delete User", bg="DeepSkyBlue4", fg = "white", command=self.delete_user)
		delete_user_btn.pack(side=LEFT)

		#frame for line3:
		frame3 = Frame(self)
		frame3.config(width=100, height=2)
		frame3.pack(fill=X)

		temp = Label(frame3,relief=RIDGE, text="Current Users", bg="light blue")
		temp.config(width=23, height=2)
		temp.pack(side=LEFT)

		temp = Label(frame3,relief=RIDGE, text="Email", bg="light blue")
		temp.config(width=80, height=2)
		temp.pack(side=LEFT, padx=5, pady=5)

		#scrolling part start
		scroll_frame = Frame(self)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=200, width=850)
		scroll_canvas.pack(side=LEFT, expand=True, fill=Y)
		list_scrollbar.pack(side=LEFT, fill=Y, padx = 5)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack(fill=X)

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_user_table()
		self.login_cur.execute("SELECT name, email FROM users")
		data = self.login_cur.fetchall()

		self.temp_user_name_btn = []

		for i in range(len(data)):
			self.temp_user_name_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
			self.temp_user_name_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(data[i][0]), command=lambda i=i : self.copy_name_to_field(i))
			self.temp_user_name_btn[i].config(width = 20, height = 1)
			self.temp_user_name_btn[i].pack(side=LEFT)

			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 80, height = 2)
			temp.pack(side=LEFT, padx=5, fill=X)

		#frame for line2:
		frame2 = Frame(self)
		frame2.pack(pady=10)
		refresh_user_btn=Button(frame2,text="Refresh",command=self.refresh_user)
		refresh_user_btn.pack(side=LEFT)

		back=Button(frame2,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT)

		exit=Button(frame2,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT)

	def copy_name_to_field(self, id):
		print(self.temp_user_name_btn[id]['text'])
		self.delete_user_name.set(self.temp_user_name_btn[id]['text'])

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def delete_user(self):
		self.create_user_table()
		if(self.delete_user_name.get() == ''):
			self.error_msg = "Invalid input!"
		elif(self.delete_user_name.get() == 'admin'):
			self.error_msg = "You cannot delete admin"
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
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		forgot_user_password=Label(frame1,text="Forgot Password?")
		forgot_user_password.config(width=200, font=("Courier", 25))
		forgot_user_password.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		forgot_pass_name=Label(frame2,text="User Name:", width=20, anchor=W)
		forgot_pass_name.pack(side=LEFT, padx=2, pady=2)

		self.forgot_pass_name=StringVar()
		forgot_pass_name_entry=Entry(frame2,textvariable=self.forgot_pass_name, width=40)
		forgot_pass_name_entry.pack(side=LEFT, padx=2, pady=2)
		forgot_pass_name_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		forgot_pass_email=Label(frame3,text="Email:", width=20, anchor=W)
		forgot_pass_email.pack(side=LEFT, padx=2, pady=2)

		self.forgot_pass_email=StringVar()
		forgot_pass_email_entry=Entry(frame3,textvariable=self.forgot_pass_email, width=40)
		forgot_pass_email_entry.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		forgot_pass_btn=Button(frame4,text="Send Password", bg="DeepSkyBlue4", fg = "white", command=self.forgot_pass_send, width=10)
		forgot_pass_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame4,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

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
	
				me      = "noreply.nslstatus@gmail.com"
				you     = self.forgot_pass_email.get()
				body    = "Dear "+name+",\nYour lost password is :"+str(password[0][0])+"\nN.B: You don't need to reply this message.\nThanks.\n"+time.asctime(time.localtime(time.time()))
	
				server  = smtplib.SMTP("smtp.gmail.com", 25)
				server.ehlo()
				server.starttls()
				server.login(me, 'a1234567890z')
				server.sendmail(me, you, body)
				server.quit()
				self.login_conn.close()
				print("Mail sent successfully!")
				self.screen = 7
				self.quit()
	
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
	name        = None
	db_name     = "status_" + datetime.datetime.now().strftime("%b") + datetime.datetime.now().strftime("%Y") + ".db"

	error_msg  = " "

	def __init__(self,master, name):
		super(update_status_page,self).__init__(master)
		self.status_conn = sqlite3.connect(self.db_name)
		self.status_cur  = self.status_conn.cursor()
		self.name        = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		update_status_label=Label(frame1,text="::Update Status::")
		update_status_label.config(width=200, font=("Courier", 25))
		update_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()
		#Team
		team_label=Label(frame2,text="Team Name:", width=20, anchor=W)
		team_label.pack(side=LEFT, pady=5)

		self.team=StringVar()
		team_entry=Entry(frame2,textvariable=self.team, width=40)
		team_entry.pack(side=LEFT, padx=2, pady=5)
		team_entry.focus_set()

		#Task List
		frame3 = Frame(self)
		frame3.pack()
		
		task_list_label=Label(frame3,text="Task List:", width=20, anchor=W)
		task_list_label.pack(side=LEFT, padx=2, pady=5)

		task_scroll = Scrollbar(frame3)
		self.task_text = Text(frame3, height=4, width=38)
		task_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.task_text.pack(side=LEFT, fill=Y)
		task_scroll.config(command=self.task_text.yview)
		self.task_text.config(yscrollcommand=task_scroll.set)

		#Progress Status
		frame4 = Frame(self)
		frame4.pack()

		progress_status_label=Label(frame4,text="Progress:", width=20, anchor=W)
		progress_status_label.pack(side=LEFT, padx=2, pady=5)

		progress_scroll = Scrollbar(frame4)
		self.progress_text = Text(frame4, height=4, width=38)
		progress_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.progress_text.pack(side=LEFT, fill=Y)
		progress_scroll.config(command=self.progress_text.yview)
		self.progress_text.config(yscrollcommand=progress_scroll.set)

		#Meeting Status
		frame5 = Frame(self)
		frame5.pack()

		meeting_status_label=Label(frame5,text="Meeting Status:", width=20, anchor=W)
		meeting_status_label.pack(side=LEFT, padx=2, pady=5)

		meeting_scroll = Scrollbar(frame5)
		self.meeting_text = Text(frame5, height=4, width=38)
		meeting_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.meeting_text.pack(side=LEFT, fill=Y)
		meeting_scroll.config(command=self.meeting_text.yview)
		self.meeting_text.config(yscrollcommand=meeting_scroll.set)

		#Project Status
		frame6 = Frame(self)
		frame6.pack()

		project_status_label=Label(frame6,text="Project Status:", width=20, anchor=W)
		project_status_label.pack(side=LEFT, padx=2, pady=5)

		project_scroll = Scrollbar(frame6)
		self.project_text = Text(frame6, height=3, width=38)
		project_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.project_text.pack(side=LEFT, fill=Y)
		project_scroll.config(command=self.project_text.yview)
		self.project_text.config(yscrollcommand=project_scroll.set)

		#Remarks
		frame7 = Frame(self)
		frame7.pack()

		remarks_status_label=Label(frame7,text="Remarks:", width=20, anchor=W)
		remarks_status_label.pack(side=LEFT, padx=2, pady=5)

		remarks_scroll = Scrollbar(frame7)
		self.remarks_text = Text(frame7, height=2, width=38)
		remarks_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.remarks_text.pack(side=LEFT, fill=Y)
		remarks_scroll.config(command=self.remarks_text.yview)
		self.remarks_text.config(yscrollcommand=remarks_scroll.set)

		frameLast = Frame(self)
		frameLast.pack()

		update_status_btn=Button(frameLast,text="Update Status", bg="DeepSkyBlue4", fg = "white", command=self.update_status, width=10)
		update_status_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")
	
	def update_status(self):
		if(self.task_text.get("1.0", "end-1c") == '' and self.team.get() == ''):
			self.error_msg = "Insufficient inputs!"
		else:
			try:
				self.create_status_table()

				ids     = str(time.time()).split(".")[0]+str(time.time()).split(".")[1]+self.name
				dates   = datetime.datetime.now().strftime("%d-%b-%Y")
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks   = datetime.datetime.now().strftime("%U")
				months  = datetime.datetime.now().strftime("%b")
				years   = datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("INSERT INTO status(ids, dates, up_time, weeks, months, years, name, team, task_list, progress_status, meeting_status, project_status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ids, dates, up_time, weeks, months, years, self.name, self.team.get(), self.task_text.get("1.0", "end-1c"), self.progress_text.get("1.0", "end-1c"), self.meeting_text.get("1.0", "end-1c"), self.project_text.get("1.0", "end-1c"), self.remarks_text.get("1.0", "end-1c")))
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
	name        = None
	db_name     = "status_" + datetime.datetime.now().strftime("%b") + datetime.datetime.now().strftime("%Y") + ".db"

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_status_page,self).__init__(master)
		self.status_conn = sqlite3.connect(self.db_name)
		self.status_cur  = self.status_conn.cursor()
		self.name        = name
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

		self.temp_user_name_btn = []
		self.names = []

		for i in range(len(data)):
			self.temp_user_name_btn.append(None)

		for i in range(len(data)):
			self.temp_user_name_btn[i] = Button(self, bg="white", fg="black", text=str(data[i][0]), command=lambda i=i : self.copy_name_to_field(i))
			self.temp_user_name_btn[i].grid(row=5+i, column=0, sticky=NSEW)
	
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


	def copy_name_to_field(self, id):
		print(self.temp_user_name_btn[id]['text'])
		self.status_id.set(self.temp_user_name_btn[id]['text'])

	def delete_status_window(self):
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
		if(self.status_id.get() == ''):
			self.error_msg = "Invalid ID!"
		else:
			try:
				self.create_status_table()
				self.status_cur.execute("SELECT team, task_list, progress_status, meeting_status, project_status, remarks FROM status WHERE ids = ?", (self.status_id.get(),))
				data = self.status_cur.fetchall()
				
				#Team
				team_label=Label(self,text="Team Name:")
				team_label.grid(row=1,column=10,sticky=E)

				self.team=StringVar()
				team_entry=Entry(self,textvariable=self.team)
				team_entry.insert(0, data[0][0])
				team_entry.grid(row=1,column=11,columnspan=3,sticky=W)
				team_entry.focus_set()

				#Task List
				task_list_label=Label(self,text="Task List:")
				task_list_label.grid(row=2,column=10,sticky=E)

				self.task_list=StringVar()
				task_list_entry=Entry(self,textvariable=self.task_list)
				task_list_entry.insert(0, data[0][1])
				task_list_entry.grid(row=2,column=11,columnspan=3,sticky=W)

				#Progress Status
				progress_status_label=Label(self,text="Progress Status:")
				progress_status_label.grid(row=3,column=10,sticky=E)

				self.progress_status=StringVar()
				progress_status_entry=Entry(self,textvariable=self.progress_status)
				progress_status_entry.insert(0, data[0][2])
				progress_status_entry.grid(row=3,column=11,columnspan=3,sticky=W)

				#Meeting Status
				meeting_status_label=Label(self,text="Meeting Status:")
				meeting_status_label.grid(row=4,column=10,sticky=E)

				self.meeting_status=StringVar()
				meeting_status_entry=Entry(self,textvariable=self.meeting_status)
				meeting_status_entry.insert(0, data[0][3])
				meeting_status_entry.grid(row=4,column=11,columnspan=3,sticky=W)

				#Project Status
				project_status_label=Label(self,text="Project Status:")
				project_status_label.grid(row=5,column=10,sticky=E)

				self.project_status=StringVar()
				project_status_entry=Entry(self,textvariable=self.project_status)
				project_status_entry.insert(0, data[0][4])
				project_status_entry.grid(row=5,column=11,columnspan=3,sticky=W)

				#Remarks
				remarks_label=Label(self,text="Remarks:")
				remarks_label.grid(row=6,column=10,sticky=E)

				self.remarks=StringVar()
				remarks_entry=Entry(self,textvariable=self.remarks)
				remarks_entry.insert(0, data[0][5])
				remarks_entry.grid(row=6,column=11,columnspan=3,sticky=W)

				update_status_btn=Button(self,text="Update Status", bg="DeepSkyBlue4", fg = "white", command=self.update_status)
				update_status_btn.grid(row=7,column=11,sticky=W)
			except Exception:
				self.error_msg = "No such ID found!"

	def update_status(self):
		if(self.task_list.get() == '' and self.team.get() == ''):
			self.error_msg = "Insufficient inputs!"
		else:
			try:
				self.create_status_table()

				dates   = datetime.datetime.now().strftime("%d-%b-%Y")
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks   = datetime.datetime.now().strftime("%U")
				months  = datetime.datetime.now().strftime("%b")
				years   = datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("UPDATE status SET dates=?, up_time=?, weeks=?, months=?, years=?, team=?, task_list=?, progress_status=?, meeting_status=?, project_status=?, remarks=? WHERE ids=? and name=?", (dates, up_time, weeks, months, years, self.team.get(), self.task_list.get(), self.progress_status.get(), self.meeting_status.get(), self.project_status.get(), self.remarks.get(), self.status_id.get(), self.name))
				self.status_conn.commit()
				time.sleep(0.02)
				print("%s, You have successfully updated your daily status!" %(self.name))
				self.screen = 9
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
root.geometry("1000x750")

header_img = PhotoImage(file='./img/nslHeader.png')
header = Button(root, relief=FLAT, image = header_img, height = 140, bg="white")
header.pack(fill=X)

bottom_text = Label(root, text = "Neural Semiconductor Ltd. © 2018")
bottom_text.pack(pady=10, side=BOTTOM)

bottom_line = Canvas(root, height=2, borderwidth=0, highlightthickness=0, bg="black")
bottom_line.pack(fill=X, padx=80, side=BOTTOM)

window=login_page(root)
screen=window.screen

name=None
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
		window=edit_user_name_page(root, name)
	elif screen==4:
		window=edit_user_email_page(root)
	elif screen==5:
		window=edit_user_pass_page(root, name)
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

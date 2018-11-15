#!/usr/bin/python3
import sqlite3
import time
from tkinter import *
from tkinter import messagebox
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
import csv

class login_page(Frame):

	screen     = 0

	login_conn = None
	login_cur  = None

	error_msg  = " "
	admin      = None

	def __init__(self,master):
		super(login_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def login(self, name, password):
		#print(name, password)
		if(name == ''):
			self.error_msg = "Name field cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		elif(password == ''):
			self.error_msg = "Password field cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				success = 0
				admin   = 0
				self.login_cur.execute("SELECT password, admin_status FROM users WHERE name = ?", (name,))
				check = self.login_cur.fetchall()
				self.login_conn.close()
				if(password == check[0][0]):
					success = 1
					self.screen = 1
					if(check[0][1] == '1'):
						admin = 1
					else:
						admin = 0
				else:
					self.screen = 0
					self.error_msg = "Incorrect Password!"
					messagebox.showinfo("Error", self.error_msg)
				return success, admin
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
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

	name   = None
	admin  = None

	me     		= "noreply.nslstatus@gmail.com"
	you    		= "noreply.nslstatus@gmail.com"
	password 	= 'a1234567890z'
	to_email    = []

	task_id 	= None

	def __init__(self,master, name, admin):
		super(user_dashboard,self).__init__(master)
		self.pack()
		self.name = name
		self.admin = admin

		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect("./db/tasks.db")
		self.task_cur  = self.task_conn.cursor()

		self.food_conn = sqlite3.connect("./db/foods.db")
		self.food_cur  = self.food_conn.cursor()

		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def create_food_table(self):
		self.food_cur.execute("CREATE TABLE IF NOT EXISTS foods(name TEXT, value TEXT, dates TEXT, weeks TEXT, months TEXT, years TEXT)")

	def food_order(self, existing, order, dates, weeks, months, years):
		if(existing == 0):
			#order activate
			self.food_btn.config(bg='green3')
			self.create_food_table()
			self.food_cur.execute("INSERT INTO foods(name, value, dates, weeks, months, years) VALUES (?, ?, ?, ?, ?, ?)", (self.name, str(1), dates, weeks, months, years))
			self.food_conn.commit()
			time.sleep(0.02)
			self.screen = 1
			self.quit()

		elif(existing == 1 and order == 0):
			#button red korbe
			self.food_btn.config(bg='tomato')
			self.create_food_table()
			self.food_cur.execute("DELETE FROM foods WHERE name = ? and dates = ?", (self.name, dates))
			self.food_conn.commit()
			time.sleep(0.02)
			self.screen = 1
			self.quit()

		elif(existing == 1 and order == 1):
			#button green korbe
			self.food_btn.config(bg='green3')
			self.create_food_table()
			self.food_cur.execute("UPDATE foods SET name = ?, value = ?, dates = ?, weeks = ?, months = ?, years = ? WHERE name = ? and dates = ?", (self.name, str(1), dates, weeks, months, years, self.name, dates))
			self.food_conn.commit()
			time.sleep(0.02)
			self.screen = 1
			self.quit()

	def backup_def(self):
		try:
			self.create_user_table()
			self.login_cur.execute("SELECT email FROM users WHERE admin_status = 1")
			data = self.login_cur.fetchall()

			for mail in data:
				self.to_email.append(mail[0])

			print(self.to_email)
			self.login_conn.close()

			msg = MIMEMultipart()
			msg['Subject'] = 'Backup-'+datetime.datetime.now().strftime("%d-%b-%Y")+"-"+datetime.datetime.now().strftime("%H:%M:%S")
			msg['From'] = self.me
			msg['To'] = ", ".join(self.to_email)
			msg.attach(MIMEText("This is backup on "+datetime.datetime.now().strftime("%d-%b-%Y")+" at time: "+datetime.datetime.now().strftime("%H:%M:%S"), 'html'))

			attachment = ['./db/users.db', './db/status.db', './db/tasks.db', './db/attns.db', './db/foods.db']

			for f in attachment:
				with open(f, 'rb') as a_file:
					basename = os.path.basename(f)
					part = MIMEApplication(a_file.read(), Name=basename)
				part['Content-Disposition'] = 'attachment; filename="%s"' % basename
				msg.attach(part)

			server  = smtplib.SMTP("smtp.gmail.com", 25)
			server.ehlo()
			server.starttls()
			server.login(self.me, self.password)
			server.sendmail(self.me, self.to_email, msg.as_string())
			server.quit()
		except Exception as e:
			print(e)

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Dashboard - "+self.name+"::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#for line2:
		frame2 = Frame(self)
		frame2.pack()

		update_status_btn=Button(frame2,text="Update Status",command=lambda: self.set_value(8), width = 16, height=2, bd=4, bg="cyan3")
		update_status_btn.pack(side=LEFT, padx=2, pady=2)

		edit_status_btn=Button(frame2,text="Edit Status",command=lambda: self.set_value(9), width = 16, height=2, bd=4, bg="PaleGreen2")
		edit_status_btn.pack(side=LEFT, padx=2, pady=2)

		assign_task_btn=Button(frame2,text="Assign Task",command=lambda: self.set_value(13), width = 16, height=2, bd=4, bg="blue2")
		assign_task_btn.pack(side=LEFT, padx=2, pady=2)

		edit_task_btn=Button(frame2,text="Edit Task",command=lambda: self.set_value(15), width = 16, height=2, bd=4, bg="aquamarine2")
		edit_task_btn.pack(side=LEFT, padx=2, pady=2)

		edit_email_btn=Button(frame2,text="Edit User Email",command=lambda: self.set_value(4), width = 16, height=2, bd=4, bg="gold2")
		edit_email_btn.pack(side=LEFT, padx=2, pady=2)

		edit_pass_btn=Button(frame2,text="Edit User Password",command=lambda: self.set_value(5), width = 16, height=2, bd=4, bg="magenta3")
		edit_pass_btn.pack(side=LEFT, padx=2, pady=2)

		attns_btn=Button(frame2,text="Attendance",command=lambda: self.set_value(19), width = 16, height=2, bd=4, bg="LightSteelBlue3")
		attns_btn.pack(side=LEFT, padx=2, pady=2)

		if(self.admin == 1):
			#for line3:
			frame3 = Frame(self)
			frame3.pack()

			edit_user_admin_sts_btn=Button(frame3,text="Admin Privilege",command=lambda: self.set_value(3), width = 16, height=2, bd=4, bg="aquamarine2")
			edit_user_admin_sts_btn.pack(side=LEFT, padx=2, pady=2)

			all_task_btn=Button(frame3,text="All Tasks",command=lambda: self.set_value(17), width = 16, height=2, bd=4, bg="medium orchid")
			all_task_btn.pack(side=LEFT, padx=2, pady=2)

			add_user_btn=Button(frame3,text="Add User",command=lambda: self.set_value(2), width = 16, height=2, bd=4, bg="yellow")
			add_user_btn.pack(side=LEFT, padx=2, pady=2)

			delete_user_btn=Button(frame3,text="Delete User",command=lambda: self.set_value(6), width = 16, height=2, bd=4, bg="LightSteelBlue3")
			delete_user_btn.pack(side=LEFT, padx=2, pady=2)

			export_report_btn=Button(frame3,text="Export Report",command=lambda: self.set_value(22), width = 16, height=2, bd=4, bg="turquoise")
			export_report_btn.pack(side=LEFT, padx=2, pady=2)

			backup_btn=Button(frame3,text="Backup",command=self.backup_def, width = 16, height=2, bd=4, bg="medium orchid")
			backup_btn.pack(side=LEFT, padx=2, pady=2)

		###########################################################
		#Foods
		dates 	= datetime.datetime.now().strftime("%d-%b-%Y")
		weeks   = datetime.datetime.now().strftime("%U")
		months  = datetime.datetime.now().strftime("%b")
		years   = datetime.datetime.now().strftime("%Y")

		self.create_food_table()
		self.food_cur.execute("SELECT value, name FROM foods WHERE name = ? and dates = ?", (self.name, dates))
		foodData = self.food_cur.fetchall()
		print(self.name, dates, foodData)

		#for line4
		frame4 = Frame(self)
		frame4.pack()

		if(int(datetime.datetime.now().strftime("%H"))>=10 and len(foodData) > 0 and int(foodData[0][0]) == 1):

			self.food_btn=Button(frame4,text="Food Order\n(Given)", bg="green3", state = DISABLED, fg = "white", width = 16, height=2, bd=4)
			self.food_btn.pack(side=LEFT, padx=2, pady=2)

		elif((int(datetime.datetime.now().strftime("%H"))>=10 and len(foodData) == 0) or ((int(datetime.datetime.now().strftime("%H"))>=10 and len(foodData) > 0 and int(foodData[0][0]) == 0))):

			self.food_btn=Button(frame4,text="Food Order\n(Not Given)", bg="tomato", state = DISABLED, fg = "white", width = 16, height=2, bd=4)
			self.food_btn.pack(side=LEFT, padx=2, pady=2)

		elif(int(datetime.datetime.now().strftime("%H"))<10 and len(foodData) > 0 and int(foodData[0][0]) == 1):

			self.food_btn=Button(frame4,text="Food Order\n(Given)", bg="green3", fg = "white", command = lambda : self.food_order(1, 0, dates, weeks, months, years), width = 16, height=2, bd=4)
			self.food_btn.pack(side=LEFT, padx=2, pady=2)
			
		elif(int(datetime.datetime.now().strftime("%H"))<10 and len(foodData) > 0 and int(foodData[0][0]) == 0):

			self.food_btn=Button(frame4, text="Food Order\n(Not Given)", bg="tomato", fg = "white", command = lambda : self.food_order(1, 1, dates, weeks, months, years), width = 16, height=2, bd=4)
			self.food_btn.pack(side=LEFT, padx=2, pady=2)

		elif(int(datetime.datetime.now().strftime("%H"))<10 and len(foodData) == 0):

			self.food_btn=Button(frame4, text="Food Order\n(Not Given)", bg="tomato", fg = "white", command = lambda : self.food_order(0, 1, dates, weeks, months, years), width = 16, height=2, bd=4)
			self.food_btn.pack(side=LEFT, padx=2, pady=2)
		else:
			self.error_msg = "Error Happend!"
			messagebox.showinfo("Error", self.error_msg)

		###########################################################

		log_out=Button(frame4,text="Log Out",command=self.set_logout, bg="DeepSkyBlue4", fg = "white", width = 16, height=2, bd=4)
		log_out.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame4,text="Exit", bg = "brown3", fg = "white", command=self.leave, width = 16, height=2, bd=4)
		exit.pack(side=LEFT, padx=2, pady=2)

		#Table Head
		frame_table_head = Frame(self)
		frame_table_head.pack()

		#Task ID
		temp = Label(frame_table_head, relief=RIDGE, text="Serial", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Assigned By
		temp = Label(frame_table_head,relief=RIDGE, text="Assigned By", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task List
		temp = Label(frame_table_head,relief=RIDGE, text="Task List", bg="light blue")
		temp.config(width = 20, height = 1)
		temp.pack(side=LEFT)

		#Description
		temp = Label(frame_table_head,relief=RIDGE, text="Description", bg="light blue")
		temp.config(width = 25, height = 1)
		temp.pack(side=LEFT)

		#Dead Line
		temp = Label(frame_table_head,relief=RIDGE, text="Dead Line", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Priority
		temp = Label(frame_table_head,relief=RIDGE, text="Priority", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task Status
		temp = Label(frame_table_head,relief=RIDGE, text="Task Status", bg="light blue")
		temp.config(width = 15, height = 1)
		temp.pack(side=LEFT)

		#assigned tasks
		frame5 = Frame(self)
		frame5.pack()

		#scrolling part start
		scroll_frame = Frame(frame5)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=150, width=814)
		scroll_canvas.pack(side=LEFT)
		list_scrollbar.pack(side=RIGHT, fill=Y)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack(fill=X)

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_task_table()
		self.task_cur.execute("SELECT ids, a_by, task_list, description, deadline, priority, status FROM tasks WHERE a_to = ?", (self.name,))
		data1 = self.task_cur.fetchall()
		data = []

		for i in range(len(data1)):
			if(data1[i][6] != 'complete'):
				data.append(data1[i])

		print(data1)

		self.task_id_btn = []
		for i in range(len(data)):
			self.task_id_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)

			#Task ID
			self.task_id_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(i+1), command=lambda i=i : self.envoke_task_details(i, data[i][0]), width=7, anchor="nw")
			self.task_id_btn[i].pack(side=LEFT)

			#Assigned By
			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 10, height = 1, anchor="nw")
			temp.pack(side=LEFT)

			#Task List
			temp = Label(frame_temp,relief=RIDGE, text=data[i][2], bg="white")
			temp.config(width = 20, height = 1, anchor="nw")
			temp.pack(side=LEFT)

			#Description
			temp = Label(frame_temp,relief=RIDGE, text=data[i][3], bg="white")
			temp.config(width = 25, height = 1, anchor="nw")
			temp.pack(side=LEFT)

			#Dead Line
			temp = Label(frame_temp,relief=RIDGE, text=data[i][4], bg="tomato")
			temp.config(width = 10, height = 1, anchor="nw")
			temp.pack(side=LEFT)

			#Priority
			temp = Label(frame_temp,relief=RIDGE, text=data[i][5], bg="white")
			temp.config(width = 10, height = 1, anchor="nw")
			temp.pack(side=LEFT)

			#Task Status
			temp = Label(frame_temp,relief=RIDGE, text=data[i][6], bg="white")
			temp.config(width = 15, height = 1, anchor="nw")
			temp.pack(side=LEFT)

	def envoke_task_details(self, i, id):
		self.task_id = id
		print(self.task_id)
		self.screen = 14
		self.quit()
		#print(id)

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

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
		self.login_conn = sqlite3.connect('./db/users.db')
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

		frame6 = Frame(self)
		frame6.pack()

		self.admin_status=IntVar()
		add_admin_check=Checkbutton(frame6,text="Add as admin?", variable=self.admin_status, width=30)
		add_admin_check.pack(side=RIGHT, padx=2, pady=2)

		frame5 = Frame(self)
		frame5.pack()

		add_btn=Button(frame5,text="Add User", bg="DeepSkyBlue4", fg = "white", command=self.add_user)
		add_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame5,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame5,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def add_user(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.add_name.get() == '' or self.add_email.get() == '' or self.add_pass.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("SELECT name, email FROM users")
					user_details = self.login_cur.fetchall()
					user_names  = [user_details[i][0] for i in range(len(user_details))]
					user_emails = [user_details[i][1] for i in range(len(user_details))]

					print(user_names, user_emails)

					if((self.add_name.get() not in user_names) and (self.add_email.get() not in user_emails)):
						self.login_cur.execute("INSERT INTO users(name, email, password, admin_status) VALUES (?, ?, ?, ?)", (self.add_name.get(), self.add_email.get(), self.add_pass.get(), str(self.admin_status.get())))
						self.login_conn.commit()
						time.sleep(0.02)
						self.login_conn.close()
						print("New User named %s is added to the database" %(self.add_name.get()))
						self.screen = 2
						self.quit()
					else:
						self.error_msg = "You cannot add this User Name/Email, already exists!"
						messagebox.showinfo("Error", self.error_msg)
						self.screen = 2
						self.quit()
				except Exception as e:
					self.error_msg = "Error happened!\nError: "+str(e)
					messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

"""class edit_user_name_page(Frame):
	screen = 3
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_user_name_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
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
			messagebox.showinfo("Error", self.error_msg)
		elif(self.edit_name_cur.get() == 'admin' or self.edit_name_new.get() == 'admin'):
			self.error_msg = "You cannot change admin name!"
			messagebox.showinfo("Error", self.error_msg)
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
				messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()"""

class edit_user_admin_sts_page(Frame):
	screen = 3
	login_conn = None
	login_cur  = None

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_user_admin_sts_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name       = name
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_name_label=Label(frame1,text="::Edit Admin Status::")
		edit_name_label.config(width=200, font=("Courier", 25))
		edit_name_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)
		
		#Add admin
		frame2 = Frame(self)
		frame2.pack()
		
		assigned_to_label=Label(frame2,text="Make Admin:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.login_cur.execute("SELECT name FROM users")
		name_list = self.login_cur.fetchall()

		self.assigned_to_name=StringVar()
		self.assigned_to_name.set('admin')

		assigned_to_list=OptionMenu(frame2,self.assigned_to_name, *name_list)
		assigned_to_list.config(width=35)
		assigned_to_list.pack(side=LEFT, padx=2, pady=5)

		admin_btn = Button(frame2,text="Make Admin", command=self.make_admin_def, fg = 'white', bg = 'DeepSkyBlue4', width=10)
		admin_btn.pack(side=LEFT, padx=2, pady=2)

		#Remove from admin
		if(self.name == "admin"):
			frame3 = Frame(self)
			frame3.pack()
			
			remove_from_label=Label(frame3,text="Remove Admin:", width=20, anchor=W)
			remove_from_label.pack(side=LEFT, pady=5)

			self.remove_from_name=StringVar()
			self.remove_from_name.set('admin')

			remove_from_list=OptionMenu(frame3,self.remove_from_name, *name_list)
			remove_from_list.config(width=35)
			remove_from_list.pack(side=LEFT, padx=2, pady=5)

			remove_btn = Button(frame3,text="Remove Admin", command=self.remove_admin_def, fg = 'white', bg = 'DeepSkyBlue4', width=10)
			remove_btn.pack(side=LEFT, padx=2, pady=2)

		frameBelow = Frame(self)
		frameBelow.pack()

		back=Button(frameBelow,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frameBelow,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def make_admin_def(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.assigned_to_name.get()==''):
				self.error_msg = "Name field cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("UPDATE users SET admin_status = ? WHERE name = ?", ('1', self.assigned_to_name.get()[2:len(self.assigned_to_name.get())-3]))
					self.login_conn.commit()
					time.sleep(0.02)
					print("User %s is made an Admin" %(self.assigned_to_name.get()[2:len(self.assigned_to_name.get())-3]))
					self.screen = 3
					self.quit()
				except Exception:
					self.error_msg = "Invalid search name!"
					messagebox.showinfo("Error", self.error_msg)

	def remove_admin_def(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_user_table()
			if(self.remove_from_name.get()==''):
				self.error_msg = "Name field cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			elif(self.remove_from_name.get()=='admin'):
				self.error_msg = "You cannot delete 'admin'"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.login_cur.execute("UPDATE users SET admin_status = ? WHERE name = ?", ('0', self.remove_from_name.get()[2:len(self.remove_from_name.get())-3]))
					self.login_conn.commit()
					time.sleep(0.02)
					print("User %s is removed from Admin" %(self.remove_from_name.get()[2:len(self.remove_from_name.get())-3]))
					self.screen = 3
					self.quit()
				except Exception as e:
					self.error_msg = "Error happened!\nError: "+str(e)
					messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.login_conn.close()
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
		self.login_conn = sqlite3.connect('./db/users.db')
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
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.login_cur.execute("UPDATE users SET email = ? WHERE name = ?", (self.edit_email_new.get(), self.edit_name_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("User email of %s is replaced by %s" %(self.edit_name_cur.get(), self.edit_email_new.get()))
				self.screen = 4
				self.quit()
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

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
		self.login_conn = sqlite3.connect('./db/users.db')
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
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		elif(self.edit_pass_confirm.get() == self.edit_pass_new.get()):
			try:
				self.login_cur.execute("UPDATE users SET password = ? WHERE name = ? and password = ?", (self.edit_pass_new.get(), self.name, self.edit_pass_cur.get()))
				self.login_conn.commit()
				time.sleep(0.02)
				self.login_conn.close()
				print("Password for %s is changed successfully!" %(name))
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
		else:
			self.error_msg = "Your password is not confirmed correctly!"
			messagebox.showinfo("Error", self.error_msg)


	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class delete_user_page(Frame):
	screen = 6
	login_conn = None
	login_cur  = None
	name       = None

	error_msg  = " "

	def __init__(self,master, name):
		super(delete_user_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.name       = name
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
		frame3.pack()

		temp = Label(frame3,relief=RIDGE, text="Current Users", bg="light blue")
		temp.config(width=23, height=1)
		temp.pack(side=LEFT)

		temp = Label(frame3,relief=RIDGE, text="Email", bg="light blue")
		temp.config(width=70, height=1)
		temp.pack(side=LEFT, pady=5)

		temp = Label(frame3,relief=RIDGE, text="Admin Status", bg="light blue")
		temp.config(width=30, height=1)
		temp.pack(side=LEFT, pady=5)

		#scrolling part start
		scroll_frame = Frame(self)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=200, width=980)
		scroll_canvas.pack(side=LEFT, expand=True, fill=Y)
		list_scrollbar.pack(side=RIGHT, fill=Y)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack(fill=X)

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_user_table()
		self.login_cur.execute("SELECT name, email, admin_status FROM users")
		data = self.login_cur.fetchall()

		self.temp_user_name_btn = []

		for i in range(len(data)):
			self.temp_user_name_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
			self.temp_user_name_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(data[i][0]), command=lambda i=i : self.copy_name_to_field(i))
			self.temp_user_name_btn[i].config(width = 20, height = 1, anchor="nw")
			self.temp_user_name_btn[i].pack(side=LEFT)

			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 70, height = 1, anchor="nw")
			temp.pack(side=LEFT, fill=X)

			temp = Label(frame_temp,relief=RIDGE, text=data[i][2], bg="white")
			temp.config(width = 30, height = 1, anchor="nw")
			temp.pack(side=LEFT, fill=X)

		#frame for line2:
		frame2 = Frame(self)
		frame2.pack(pady=10)

		refresh_user_btn=Button(frame2,text="Refresh",command=self.refresh_user, bg='DeepSkyBlue4', fg='white')
		refresh_user_btn.pack(side=LEFT)

		back=Button(frame2,text="< Prev", command=self.go_prev)
		back.pack(side=LEFT)

		exit=Button(frame2,text="Exit", bg = "brown3", fg = "white", command=self.leave)
		exit.pack(side=LEFT)

	def copy_name_to_field(self, id):
		print(self.temp_user_name_btn[id]['text'])
		self.delete_user_name.set(self.temp_user_name_btn[id]['text'])

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def delete_user(self):
		if(messagebox.askyesno("Warning", "Are you sure to delete this user?")):
			if(self.delete_user_name.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			elif(self.delete_user_name.get() == 'admin'):
				self.error_msg = "You cannot delete admin"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.create_user_table()
					self.login_cur.execute("SELECT admin_status FROM users WHERE name = ?", (self.delete_user_name.get(),))
					data = self.login_cur.fetchall()
					print(data[0][0])

					if(self.name == 'admin'):
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
							messagebox.showinfo("Error", self.error_msg)
					elif(self.name != 'admin' and data[0][0] == '0'):
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
							messagebox.showinfo("Error", self.error_msg)
					else:
						self.error_msg = "You cannot delete another admin"
						messagebox.showinfo("Error", self.error_msg)
				except Exception as e:
					print(e)

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
		self.login_conn = sqlite3.connect('./db/users.db')
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
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.login_cur.execute("SELECT password FROM users WHERE name = ? and email = ?", (self.forgot_pass_name.get(), self.forgot_pass_email.get()))
				password = self.login_cur.fetchall()
	
				me      = "noreply.nslstatus@gmail.com"
				you     = self.forgot_pass_email.get()
				body    = "Dear "+self.forgot_pass_name.get()+",\nYour lost password is :"+str(password[0][0])+"\nN.B: You don't need to reply this message.\nThanks.\n"+time.asctime(time.localtime(time.time()))

				msg = MIMEMultipart()
				msg['Subject'] = "Forgotten user password"
				msg['From'] = me
				msg['To'] = you
				msg.attach(MIMEText(str(body), 'html'))

				server  = smtplib.SMTP("smtp.gmail.com", 25)
				server.ehlo()
				server.starttls()
				server.login(me, 'a1234567890z')
				server.sendmail(me, you, msg.as_string())
				server.quit()
				self.login_conn.close()
				print("Mail sent successfully!")
				self.screen = 7
				self.quit()
	
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

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
	db_name     = "./db/status.db"

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

		#Date
		frameDate = Frame(self)
		frameDate.pack()
		
		date_label=Label(frameDate,text="Date:", width=20, anchor=W)
		date_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frameDate,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.day_name=StringVar()
		self.day_name.set(datetime.datetime.now().strftime("%d"))

		day_list=OptionMenu(frameDate,self.day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		day_list.pack(side=LEFT, padx=2, pady=5)

		month_label=Label(frameDate,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.month_name=StringVar()
		self.month_name.set(datetime.datetime.now().strftime("%b"))

		month_list=OptionMenu(frameDate,self.month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		month_list.pack(side=LEFT, padx=2, pady=5)

		year_label=Label(frameDate,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.year_name=StringVar()
		self.year_name.set(datetime.datetime.now().strftime("%Y"))

		year_list=OptionMenu(frameDate,self.year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		year_list.pack(side=LEFT, padx=2, pady=5)

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
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_status_table()

				ids     = str(time.time()).split(".")[0]+str(time.time()).split(".")[1]+self.name
				dates   = self.day_name.get()+"-"+self.month_name.get()+"-"+self.year_name.get()
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks   = datetime.datetime.now().strftime("%U")
				months  = datetime.datetime.now().strftime("%b")
				years   = datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("INSERT INTO status(ids, dates, up_time, weeks, months, years, name, team, task_list, progress_status, meeting_status, project_status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ids, dates, up_time, weeks, months, years, self.name, self.team.get().lower(), self.task_text.get("1.0", "end-1c"), self.progress_text.get("1.0", "end-1c"), self.meeting_text.get("1.0", "end-1c"), self.project_text.get("1.0", "end-1c"), self.remarks_text.get("1.0", "end-1c")))
				self.status_conn.commit()
				time.sleep(0.02)
				self.status_conn.close()
				print("%s, You have successfully updated your daily status!" %(self.name))
				self.screen = 8
				self.quit()
			except Exception as e:
				self.error_msg = "Invalid inputs! Error Happened!\n Error: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
	
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
	db_name     = "./db/status.db"

	error_msg  = " "

	def __init__(self,master, name):
		super(edit_status_page,self).__init__(master)
		self.status_conn = sqlite3.connect(self.db_name)
		self.status_cur  = self.status_conn.cursor()
		self.name        = name
		self.pack()
		self.define_widgets()

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_status_label=Label(frame1,text="::Edit Status::")
		edit_status_label.config(width=200, font=("Courier", 25))
		edit_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#ID
		frame2 = Frame(self)
		frame2.pack()

		status_id_label=Label(frame2,text="Status ID:", width=20)
		status_id_label.pack(side=LEFT, padx=2, pady=2)

		self.status_id=StringVar()
		status_entry=Entry(frame2,textvariable=self.status_id, width=40)
		status_entry.pack(side=LEFT, padx=2, pady=2)
		status_entry.focus_set()

		edit_status_btn=Button(frame2,text="Edit", bg="DeepSkyBlue4", fg = "white", command=self.edit_status_window, width=15)
		edit_status_btn.pack(side=LEFT, padx=2, pady=2)

		delete_status_btn=Button(frame2,text="Delete", bg="brown3", fg = "white", command=self.delete_status_window, width=15)
		delete_status_btn.pack(side=LEFT, padx=2, pady=2)

		frame3 = Frame(self)
		frame3.pack()

		back=Button(frame3,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame3,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

		frame4 = Frame(self)
		frame4.pack()

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Serial", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Date", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Time", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Team", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Task List", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Progress Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Meeting Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Project Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Remarks", width=15)
		temp.pack(side=LEFT, pady=2)

		frame5 = Frame(self)
		frame5.pack()

		status_scroll = Scrollbar(frame5)
		status_canvas = Canvas(frame5, height=100, width=1090)
		status_scroll.pack(side=RIGHT, fill=Y)
		status_canvas.pack(side=LEFT)
		status_scroll.config(command=status_canvas.yview)
		status_canvas.config(yscrollcommand=status_scroll.set)

		lists = Frame(status_canvas)
		lists.pack(fill=X)

		status_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_status_table()
		self.status_cur.execute("SELECT ids, dates, up_time, team, task_list, progress_status, meeting_status, project_status, remarks FROM status WHERE name = ?", (self.name,))
		data = self.status_cur.fetchall()

		self.temp_user_name_btn = []
		self.names = []

		for i in range(len(data)):
			self.temp_user_name_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)

			self.temp_user_name_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(i+1), command=lambda i=i : self.copy_name_to_field(i,data[i][0]), width=7, height="1", anchor="nw")
			self.temp_user_name_btn[i].pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=10)
			temp.configure(text=data[i][1], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=10)
			temp.configure(text=data[i][2], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=10)
			temp.configure(text=data[i][3], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=20)
			temp.configure(text=data[i][4], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=20)
			temp.configure(text=data[i][5], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=20)
			temp.configure(text=data[i][6], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=20)
			temp.configure(text=data[i][7], height="1", anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="light blue", width=15)
			temp.configure(text=data[i][8], height="1", anchor="nw")
			temp.pack(side=LEFT)

		self.frameBelow = Frame(self)
		self.frameBelow.pack(pady=10)


	def copy_name_to_field(self, i, id):
		print(self.temp_user_name_btn[i]['text'])
		self.status_id.set(id)

	def delete_status_window(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_status_table()
			if(self.status_id.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
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
					messagebox.showinfo("Error", self.error_msg)

	def edit_status_window(self):
		if(self.status_id.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_status_table()
				self.status_cur.execute("SELECT team, task_list, progress_status, meeting_status, project_status, remarks, dates FROM status WHERE ids = ?", (self.status_id.get(),))
				data = self.status_cur.fetchall()

				self.frameBelow.pack_forget()

				self.frameBelow = Frame(self)
				self.frameBelow.pack()

				frameLeft = Frame(self.frameBelow)
				frameLeft.pack(side=LEFT, padx=5)
				
				frame2 = Frame(frameLeft)
				frame2.pack()

				#Team
				team_label=Label(frame2,text="Team Name:", width=20, anchor=W)
				team_label.pack(side=LEFT, pady=5)
				
				self.team=StringVar()
				team_entry=Entry(frame2,textvariable=self.team, width=40)
				team_entry.insert(0, data[0][0])
				team_entry.pack(side=LEFT, padx=2, pady=5)
				team_entry.focus_set()
				
				#Date
				date=data[0][6].split('-')
				frameDate = Frame(frameLeft)
				frameDate.pack()

				date_label=Label(frameDate,text="Date:", width=20, anchor=W)
				date_label.pack(side=LEFT, pady=5, padx=2)

				day_label=Label(frameDate,text="Day:", anchor=W)
				day_label.pack(side=LEFT, pady=5)

				self.day_name=StringVar()
				self.day_name.set(date[0])

				day_list=OptionMenu(frameDate,self.day_name, *[str(i) for i in range(1, 32)])
				#day_list.config(width=5)
				day_list.pack(side=LEFT, padx=2, pady=5)

				month_label=Label(frameDate,text="Month:", anchor=W)
				month_label.pack(side=LEFT, pady=5)

				self.month_name=StringVar()
				self.month_name.set(date[1])

				month_list=OptionMenu(frameDate,self.month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
				#month_list.config(width=5)
				month_list.pack(side=LEFT, padx=2, pady=5)

				year_label=Label(frameDate,text="Year:", anchor=W)
				year_label.pack(side=LEFT, pady=5)

				self.year_name=StringVar()
				self.year_name.set(date[2])

				year_list=OptionMenu(frameDate,self.year_name, *[str(i) for i in range(2011, 2021)])
				#year_list.config(width=5)
				year_list.pack(side=LEFT, padx=2, pady=5)

				#Task List
				frame3 = Frame(frameLeft, width=450, height=200)
				frame3.pack()
				
				task_list_label=Label(frame3,text="Task List:", width=20, anchor=W)
				task_list_label.pack(side=LEFT, padx=2, pady=5)
				
				task_scroll = Scrollbar(frame3)
				self.task_text = Text(frame3, height=4, width=38)
				self.task_text.insert("1.0",data[0][1])
				task_scroll.pack(side=RIGHT, fill=Y, padx = 5)
				self.task_text.pack(side=LEFT, fill=Y)
				task_scroll.config(command=self.task_text.yview)
				self.task_text.config(yscrollcommand=task_scroll.set)

				#Progress Status
				frame4 = Frame(frameLeft)
				frame4.pack()
				
				progress_status_label=Label(frame4,text="Progress:", width=20, anchor=W)
				progress_status_label.pack(side=LEFT, padx=2, pady=5)
				
				progress_scroll = Scrollbar(frame4)
				self.progress_text = Text(frame4, height=4, width=38)
				self.progress_text.insert("1.0",data[0][2])
				progress_scroll.pack(side=RIGHT, fill=Y, padx = 5)
				self.progress_text.pack(side=LEFT, fill=Y)
				progress_scroll.config(command=self.progress_text.yview)
				self.progress_text.config(yscrollcommand=progress_scroll.set)

				frameRight = Frame(self.frameBelow)
				frameRight.pack(side=LEFT, padx=5)

				#Meeting Status
				frame5 = Frame(frameRight)
				frame5.pack()
				
				meeting_status_label=Label(frame5,text="Meeting Status:", width=20, anchor=W)
				meeting_status_label.pack(side=LEFT, padx=2, pady=5)
				
				meeting_scroll = Scrollbar(frame5)
				self.meeting_text = Text(frame5, height=4, width=38)
				self.meeting_text.insert("1.0",data[0][3])
				meeting_scroll.pack(side=RIGHT, fill=Y, padx = 5)
				self.meeting_text.pack(side=LEFT, fill=Y)
				meeting_scroll.config(command=self.meeting_text.yview)
				self.meeting_text.config(yscrollcommand=meeting_scroll.set)


				#Project Status
				frame6 = Frame(frameRight)
				frame6.pack()
				
				project_status_label=Label(frame6,text="Project Status:", width=20, anchor=W)
				project_status_label.pack(side=LEFT, padx=2, pady=5)
				
				project_scroll = Scrollbar(frame6)
				self.project_text = Text(frame6, height=3, width=38)
				self.project_text.insert("1.0",data[0][4])
				project_scroll.pack(side=RIGHT, fill=Y, padx = 5)
				self.project_text.pack(side=LEFT, fill=Y)
				project_scroll.config(command=self.project_text.yview)
				self.project_text.config(yscrollcommand=project_scroll.set)


				#Remarks
				frame7 = Frame(frameRight)
				frame7.pack()
				
				remarks_status_label=Label(frame7,text="Remarks:", width=20, anchor=W)
				remarks_status_label.pack(side=LEFT, padx=2, pady=5)
				
				remarks_scroll = Scrollbar(frame7)
				self.remarks_text = Text(frame7, height=2, width=38)
				self.remarks_text.insert("1.0",data[0][5])
				remarks_scroll.pack(side=RIGHT, fill=Y, padx = 5)
				self.remarks_text.pack(side=LEFT, fill=Y)
				remarks_scroll.config(command=self.remarks_text.yview)
				self.remarks_text.config(yscrollcommand=remarks_scroll.set)

				frameUpdate = Frame(self)
				frameUpdate.pack()
				update_status_btn=Button(frameUpdate,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.update_status, width=20)
				update_status_btn.pack(pady=10)
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

	def update_status(self):
		if(self.task_text.get("1.0", "end-1c") == '' and self.team.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_status_table()

				dates   = self.day_name.get()+"-"+self.month_name.get()+"-"+self.year_name.get()
				up_time = datetime.datetime.now().strftime("%H:%M:%S")
				weeks   = datetime.datetime.now().strftime("%U")
				months  = datetime.datetime.now().strftime("%b")
				years   = datetime.datetime.now().strftime("%Y")

				self.status_cur.execute("UPDATE status SET dates=?, up_time=?, weeks=?, months=?, years=?, team=?, task_list=?, progress_status=?, meeting_status=?, project_status=?, remarks=? WHERE ids=? and name=?", (dates, up_time, weeks, months, years, self.team.get().lower(), self.task_text.get("1.0", "end-1c"), self.progress_text.get("1.0", "end-1c"), self.meeting_text.get("1.0", "end-1c"), self.project_text.get("1.0", "end-1c"), self.remarks_text.get("1.0", "end-1c"), self.status_id.get(), self.name))
				self.status_conn.commit()
				time.sleep(0.02)
				print("%s, You have successfully updated your daily status!" %(self.name))
				self.screen = 9
				self.quit()
			except Exception as e:
				self.error_msg = "Invalid inputs! Error happened! \nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
	
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
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()
		self.pack()
		self.define_widgets()

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		forgot_user_password=Label(frame1,text="::Forgot User Name?::")
		forgot_user_password.config(width=200, font=("Courier", 25))
		forgot_user_password.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frame2 = Frame(self)
		frame2.pack()

		forgot_id_email=Label(frame2,text="Email:", width=10, anchor=W)
		forgot_id_email.pack(side=LEFT, padx=2, pady=2)

		self.forgot_id_email=StringVar()
		forgot_id_email_entry=Entry(frame2,textvariable=self.forgot_id_email, width=40)
		forgot_id_email_entry.pack(side=LEFT, padx=2, pady=2)
		forgot_id_email_entry.focus_set()

		frame3 = Frame(self)
		frame3.pack()

		forgot_id_btn=Button(frame3,text="Find", bg="DeepSkyBlue4", fg = "white", command=self.pre_forgot_id_find, width=10)
		forgot_id_btn.pack(side=LEFT, padx=2, pady=2)

		back=Button(frame3,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame3,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

		self.frame4 = Frame(self)
		self.frame4.pack()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def pre_forgot_id_find(self):
		self.frame4.pack_forget()
		self.frame4 = Frame(self)
		self.frame4.pack()
		self.forgot_id_name_label=Label(self.frame4, relief=RIDGE, text="<User ID>", state=DISABLED)
		self.forgot_id_name_label.pack(side=LEFT, padx=2, pady=2)
		self.forgot_id_find()

	def forgot_id_find(self):
		self.create_user_table()
		if(self.forgot_id_email.get() == ''):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
			self.screen = 12
			self.quit()
		else:
			try:
				self.login_cur.execute("SELECT name FROM users WHERE email = ?", (self.forgot_id_email.get(),))
				id_name = self.login_cur.fetchall()
				self.forgot_id_name_label.configure(text=":: "+str(id_name[0][0])+" ::", state=ACTIVE, fg="blue", font=("Courier", 25))
			except Exception as e:
				self.error_msg = "Error Happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)

	def go_prev(self):
		self.login_conn.close()
		self.screen = 0
		self.quit()

	def leave(self):
		self.login_conn.close()
		quit()

class assign_task_page(Frame):
	screen 			= 13

	status_conn 	= None
	status_cur  	= None
	
	task_conn 		= None
	task_cur  		= None
	
	name        	= None
	
	task_db  		= "./db/tasks.db"

	error_msg  		= " "

	assigned_to_users_list = []

	def __init__(self,master, name):
		super(assign_task_page,self).__init__(master)

		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect(self.task_db)
		self.task_cur  = self.task_conn.cursor()

		self.name        = name
		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def assign_to_user(self, user):
		if str(user[2:len(user)-3]) not in self.assigned_to_users_list:
			self.assigned_to_users_list.append(str(user[2:len(user)-3]))
			strList = ''
			for i in self.assigned_to_users_list:
				strList = strList + str(i) + ", "
			self.assigned_to_names_str.set(strList)
			print(strList)

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		update_status_label=Label(frame1,text="::Assign Task::")
		update_status_label.config(width=200, font=("Courier", 25))
		update_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frameHolder = Frame(self)
		frameHolder.pack()

		frameLeft = Frame(frameHolder)
		frameLeft.pack(side=LEFT, padx=5)

		#Assigned To
		frame2 = Frame(frameLeft)
		frame2.pack()
		
		assigned_to_label=Label(frame2,text="Assign To:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.login_cur.execute("SELECT name FROM users")
		name_list = self.login_cur.fetchall()
		self.login_conn.close()

		self.assigned_to_name=StringVar()
		self.assigned_to_name.set(self.name)

		assigned_to_list=OptionMenu(frame2,self.assigned_to_name, *name_list, command = lambda x: self.assign_to_user(self.assigned_to_name.get()))
		assigned_to_list.config(width=35)
		assigned_to_list.pack(side=LEFT, padx=2, pady=5)
		assigned_to_list.focus_set()

		#Assigned List
		frame11 = Frame(frameLeft)
		frame11.pack()
		
		assigned_to_label=Label(frame11,text="Assigned To:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.assigned_to_names_str = StringVar()
		self.assigned_to_users_list = []
		assigned_to_names=Label(frame11, width=43, anchor=W, textvariable=self.assigned_to_names_str)
		assigned_to_names.pack(side=LEFT, pady=5)

		#Task List
		frame3 = Frame(frameLeft)
		frame3.pack()
		
		task_list_label=Label(frame3,text="Task List:", width=20, anchor=W)
		task_list_label.pack(side=LEFT, padx=2, pady=5)

		task_scroll = Scrollbar(frame3)
		self.task_text = Text(frame3, height=4, width=43)
		task_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.task_text.pack(side=LEFT, fill=Y)
		task_scroll.config(command=self.task_text.yview)
		self.task_text.config(yscrollcommand=task_scroll.set)

		#Task Description
		frame4 = Frame(frameLeft)
		frame4.pack()

		task_des_label=Label(frame4,text="Description:", width=20, anchor=W)
		task_des_label.pack(side=LEFT, padx=2, pady=5)

		task_des_scroll = Scrollbar(frame4)
		self.task_des_text = Text(frame4, height=4, width=43)
		task_des_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.task_des_text.pack(side=LEFT, fill=Y)
		task_des_scroll.config(command=self.task_des_text.yview)
		self.task_des_text.config(yscrollcommand=task_des_scroll.set)

		#Estimated Date
		frame5 = Frame(frameLeft)
		frame5.pack()
		
		est_date_label=Label(frame5,text="Est. Date:", width=19, anchor=W)
		est_date_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frame5,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.day_name=StringVar()
		self.day_name.set(datetime.datetime.now().strftime("%d"))

		day_list=OptionMenu(frame5,self.day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		day_list.pack(side=LEFT, padx=2, pady=5)

		month_label=Label(frame5,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.month_name=StringVar()
		self.month_name.set(datetime.datetime.now().strftime("%b"))

		month_list=OptionMenu(frame5,self.month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		month_list.pack(side=LEFT, padx=2, pady=5)

		year_label=Label(frame5,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.year_name=StringVar()
		self.year_name.set(datetime.datetime.now().strftime("%Y"))

		year_list=OptionMenu(frame5,self.year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		year_list.pack(side=LEFT, padx=2, pady=5)

		#Deadline
		frame6 = Frame(frameLeft)
		frame6.pack(side=LEFT, padx=5)
		
		deadline_label=Label(frame6,text="Deadline:", width=19, anchor=W)
		deadline_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frame6,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.deadline_day_name=StringVar()
		self.deadline_day_name.set(datetime.datetime.now().strftime("%d"))

		deadline_day_list=OptionMenu(frame6,self.deadline_day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		deadline_day_list.pack(side=LEFT, padx=2, pady=5)

		deadline_month_label=Label(frame6,text="Month:", anchor=W)
		deadline_month_label.pack(side=LEFT, pady=5)

		self.deadline_month_name=StringVar()
		self.deadline_month_name.set(datetime.datetime.now().strftime("%b"))

		deadline_month_list=OptionMenu(frame6,self.deadline_month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		deadline_month_list.pack(side=LEFT, padx=2, pady=5)

		deadline_year_label=Label(frame6,text="Year:", anchor=W)
		deadline_year_label.pack(side=LEFT, pady=5)

		self.deadline_year_name=StringVar()
		self.deadline_year_name.set(datetime.datetime.now().strftime("%Y"))

		deadline_year_list=OptionMenu(frame6,self.deadline_year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		deadline_year_list.pack(side=LEFT, padx=2, pady=5)

		frameRight = Frame(frameHolder)
		frameRight.pack()

		#Comments
		frame7 = Frame(frameRight)
		frame7.pack()

		comments_label=Label(frame7,text="Comments:", width=20, anchor=W)
		comments_label.pack(side=LEFT, padx=2, pady=5)

		comments_scroll = Scrollbar(frame7)
		self.comments_text = Text(frame7, height=4, width=43)
		comments_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.comments_text.pack(side=LEFT, fill=Y)
		comments_scroll.config(command=self.comments_text.yview)
		self.comments_text.config(yscrollcommand=comments_scroll.set)

		#Priority
		frame8 = Frame(frameRight)
		frame8.pack()
		
		priority_label=Label(frame8,text="Priority:", width=20, anchor=W)
		priority_label.pack(side=LEFT, pady=5, padx=2)

		self.priority_level=StringVar()
		self.priority_level.set("5")

		priority_list=OptionMenu(frame8,self.priority_level, *[str(i) for i in range(1, 6)])
		priority_list.config(width=35)
		priority_list.pack(side=LEFT, padx=2, pady=5)

		#Remarks
		frame9 = Frame(frameRight)
		frame9.pack()

		remarks_status_label=Label(frame9,text="Remarks:", width=20, anchor=W)
		remarks_status_label.pack(side=LEFT, padx=2, pady=5)

		remarks_scroll = Scrollbar(frame9)
		self.remarks_text = Text(frame9, height=2, width=43)
		remarks_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.remarks_text.pack(side=LEFT, fill=Y)
		remarks_scroll.config(command=self.remarks_text.yview)
		self.remarks_text.config(yscrollcommand=remarks_scroll.set)

		#Task Status
		frame10 = Frame(frameRight)
		frame10.pack()
		
		task_status_label=Label(frame10,text="Status:", width=20, anchor=W)
		task_status_label.pack(side=LEFT, pady=5, padx=2)

		self.task_status_level=StringVar()
		self.task_status_level.set("discussion")

		task_status_list=OptionMenu(frame10,self.task_status_level, *['discussion', 'in progress', 'incomplete', 'complete', 'delivered'])
		task_status_list.config(width=35)
		task_status_list.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(frameRight)
		frameLast.pack()

		assign_task_btn=Button(frameLast,text="Assign", bg="DeepSkyBlue4", fg = "white", command=self.assign_task, width=10)
		assign_task_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)
	
	def assign_task(self):
		if(self.task_text.get("1.0", "end-1c") == '' and len(self.assigned_to_users_list)==0):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_task_table()

				for users in self.assigned_to_users_list:
					ids     = "task"+users+str(time.time()).split(".")[0]+str(time.time()).split(".")[1]+self.name
					dates   = datetime.datetime.now().strftime("%d-%b-%Y")
					up_time = datetime.datetime.now().strftime("%H:%M:%S")

					self.task_cur.execute("INSERT INTO tasks(ids, dates, up_time, a_by, a_to, task_list, description, est_date, deadline, comments, priority, remarks, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (ids, dates, up_time, self.name, users, self.task_text.get("1.0", "end-1c"), self.task_des_text.get("1.0", "end-1c"), self.day_name.get()+"-"+self.month_name.get()+"-"+self.year_name.get(), self.deadline_day_name.get()+"-"+self.deadline_month_name.get()+"-"+self.deadline_year_name.get(), self.comments_text.get("1.0", "end-1c"), self.priority_level.get(), self.remarks_text.get("1.0", "end-1c"), self.task_status_level.get()))
					self.task_conn.commit()
					time.sleep(0.02)

				self.task_conn.close()
				print("%s, You have successfully assigned task to!" %(self.name))
				self.screen = 13
				self.quit()
			except Exception as e:
				self.error_msg = "Error Happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
	
	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class task_description_page(Frame):
	screen 			= 14
	prev_screen     = None

	status_conn 	= None
	status_cur  	= None
	
	task_conn 		= None
	task_cur  		= None
	
	name        	= None
	task_id 		= 0
	
	task_db  		= "./db/tasks.db"

	error_msg  		= " "

	assigned_to_users_list = []

	def __init__(self,master, name, task_id, prev_screen):
		super(task_description_page,self).__init__(master)

		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect(self.task_db)
		self.task_cur  = self.task_conn.cursor()

		self.name        = name
		self.task_id 	 = task_id
		self.prev_screen = prev_screen

		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def define_widgets(self):
		try:
			print(self.task_id, self.name)
			self.create_task_table()
			self.task_cur.execute("SELECT a_by, dates, up_time, task_list, description, est_date, deadline, comments, priority, remarks, status FROM tasks WHERE ids = ?", (self.task_id,))
			data = self.task_cur.fetchall()

			frame1 = Frame(self)
			frame1.pack()
			update_status_label=Label(frame1,text="::Task Description::")
			update_status_label.config(width=200, font=("Courier", 25))
			update_status_label.pack(pady=5)

			canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
			canvas.pack(fill=X, padx=80, pady=10)

			frameHolder = Frame(self)
			frameHolder.pack()

			#Assigned By
			frame2 = Frame(frameHolder)
			frame2.pack()
			
			assigned_by_label=Label(frame2,text="Assign By:", width=20, anchor=W)
			assigned_by_label.pack(side=LEFT, pady=5)

			self.assigned_by_name=StringVar()
			self.assigned_by_name.set(self.name)

			assigned_by_name_label=Label(frame2,text=data[0][0], width=46, anchor=W)
			assigned_by_name_label.pack(side=LEFT, pady=5)


			#Assigned Time
			frame11 = Frame(frameHolder)
			frame11.pack()
			
			assigned_time_label=Label(frame11,text="Assigning Time:", width=20, anchor=W)
			assigned_time_label.pack(side=LEFT, pady=5)

			self.assigned_time = StringVar()
			self.assigned_time.set("On "+str(data[0][1])+" at "+str(data[0][2]))
			assigned_time_name=Label(frame11, width=46, anchor=W, textvariable=self.assigned_time)
			assigned_time_name.pack(side=LEFT, pady=5)

			#Task List
			frame3 = Frame(frameHolder)
			frame3.pack()
			
			task_list_label=Label(frame3,text="Task List:", width=20, anchor=W)
			task_list_label.pack(side=LEFT, padx=2, pady=5)

			task_scroll = Scrollbar(frame3)
			self.task_text = Text(frame3, height=4, width=43)
			task_scroll.pack(side=RIGHT, fill=Y, padx = 5)
			self.task_text.pack(side=LEFT, fill=Y)
			task_scroll.config(command=self.task_text.yview)
			self.task_text.config(yscrollcommand=task_scroll.set)
			self.task_text.insert(END, data[0][3])

			#Task Description
			frame4 = Frame(frameHolder)
			frame4.pack()

			task_des_label=Label(frame4,text="Description:", width=20, anchor=W)
			task_des_label.pack(side=LEFT, padx=2, pady=5)

			task_des_scroll = Scrollbar(frame4)
			self.task_des_text = Text(frame4, height=4, width=43)
			task_des_scroll.pack(side=RIGHT, fill=Y, padx = 5)
			self.task_des_text.pack(side=LEFT, fill=Y)
			task_des_scroll.config(command=self.task_des_text.yview)
			self.task_des_text.config(yscrollcommand=task_des_scroll.set)
			self.task_des_text.insert(END, data[0][4])

			#Estimated Date
			frame5 = Frame(frameHolder)
			frame5.pack()
			
			est_date_label=Label(frame5,text="Est. Date:", width=20, anchor=W)
			est_date_label.pack(side=LEFT, pady=5, padx=2)

			self.est_date_name=StringVar()
			self.est_date_name.set(data[0][5])

			est_date_name_label=Label(frame5,textvariable=self.est_date_name, width = 46, anchor=W)
			est_date_name_label.pack(side=LEFT, pady=5)

			#Deadline
			frame6 = Frame(frameHolder)
			frame6.pack()
			
			deadline_label=Label(frame6,text="Deadline:", width=20, anchor=W)
			deadline_label.pack(side=LEFT, pady=5, padx=2)

			self.deadline_date_name=StringVar()
			self.deadline_date_name.set(data[0][6])

			deadline_date_name_label=Label(frame6,textvariable=self.deadline_date_name, width = 46, anchor=W)
			deadline_date_name_label.pack(side=LEFT, pady=5)

			#Comments
			frame7 = Frame(frameHolder)
			frame7.pack()

			comments_label=Label(frame7,text="Comments:", width=20, anchor=W)
			comments_label.pack(side=LEFT, padx=2, pady=5)

			comments_scroll = Scrollbar(frame7)
			self.comments_text = Text(frame7, height=4, width=43)
			comments_scroll.pack(side=RIGHT, fill=Y, padx = 5)
			self.comments_text.pack(side=LEFT, fill=Y)
			comments_scroll.config(command=self.comments_text.yview)
			self.comments_text.config(yscrollcommand=comments_scroll.set)
			self.comments_text.insert(END, data[0][7])

			#Priority
			frame8 = Frame(frameHolder)
			frame8.pack()
			
			priority_label=Label(frame8,text="Priority:", width=20, anchor=W)
			priority_label.pack(side=LEFT, pady=5, padx=2)

			self.priority_level=StringVar()
			self.priority_level.set(data[0][8])

			priority_name_label=Label(frame8,textvariable=self.priority_level, width = 46, anchor=W)
			priority_name_label.pack(side=LEFT, pady=5)

			#Remarks
			frame9 = Frame(frameHolder)
			frame9.pack()

			remarks_status_label=Label(frame9,text="Remarks:", width=20, anchor=W)
			remarks_status_label.pack(side=LEFT, padx=2, pady=5)

			remarks_scroll = Scrollbar(frame9)
			self.remarks_text = Text(frame9, height=2, width=43)
			remarks_scroll.pack(side=RIGHT, fill=Y, padx = 5)
			self.remarks_text.pack(side=LEFT, fill=Y)
			remarks_scroll.config(command=self.remarks_text.yview)
			self.remarks_text.config(yscrollcommand=remarks_scroll.set)
			self.remarks_text.insert(END, data[0][9])

			#Task Status
			frame10 = Frame(frameHolder)
			frame10.pack()
			
			task_status_label=Label(frame10,text="Status:", width=20, anchor=W)
			task_status_label.pack(side=LEFT, pady=5, padx=2)

			self.task_status_level=StringVar()
			self.task_status_level.set(data[0][10])

			task_status_name_label=Label(frame10,textvariable=self.task_status_level, width = 46, anchor=W)
			task_status_name_label.pack(side=LEFT, pady=5)

			frameLast = Frame(frameHolder)
			frameLast.pack()

			back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
			back.pack(side=LEFT, padx=2, pady=5)

			exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
			exit.pack(side=LEFT, padx=2, pady=5)

		except Exception as e:
			print(e)
	
	def go_prev(self):
		self.screen = self.prev_screen
		self.quit()

	def leave(self):
		quit()

class edit_assign_task_page(Frame):
	screen 			= 15
	
	task_conn 		= None
	task_cur  		= None
	
	name        	= None
	
	task_db  		= "./db/tasks.db"

	error_msg  		= " "

	assigned_to_users_list = []

	def __init__(self,master, name):
		super(edit_assign_task_page,self).__init__(master)
		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect(self.task_db)
		self.task_cur  = self.task_conn.cursor()

		self.name        = name
		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def assign_to_user(self, user):
		if str(user[2:len(user)-3]) not in self.assigned_to_users_list:
			self.assigned_to_users_list.append(str(user[2:len(user)-3]))
			strList = ''
			for i in self.assigned_to_users_list:
				strList = strList + str(i) + ", "
			self.assigned_to_names_str.set(strList)
			print(strList)

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		edit_status_label=Label(frame1,text="::Edit Task::")
		edit_status_label.config(width=200, font=("Courier", 25))
		edit_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#ID
		frame2 = Frame(self)
		frame2.pack()

		task_id_label=Label(frame2,text="Task ID:", width=20)
		task_id_label.pack(side=LEFT, padx=2, pady=2)

		self.task_id=StringVar()
		task_id_entry=Entry(frame2,textvariable=self.task_id, width=40)
		task_id_entry.pack(side=LEFT, padx=2, pady=2)
		task_id_entry.focus_set()

		edit_task_btn=Button(frame2,text="Edit", bg="DeepSkyBlue4", fg = "white", command=self.edit_task_window, width=15)
		edit_task_btn.pack(side=LEFT, padx=2, pady=2)

		delete_task_btn=Button(frame2,text="Delete", bg="brown3", fg = "white", command=self.delete_task_window, width=15)
		delete_task_btn.pack(side=LEFT, padx=2, pady=2)

		frame3 = Frame(self)
		frame3.pack()

		back=Button(frame3,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=2)

		exit=Button(frame3,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=2)

		#Table Head
		frame_table_head = Frame(self)
		frame_table_head.pack()

		#Task ID
		temp = Label(frame_table_head, relief=RIDGE, text="Serial", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Assigned To
		temp = Label(frame_table_head,relief=RIDGE, text="Assigned To", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task List
		temp = Label(frame_table_head,relief=RIDGE, text="Task List", bg="light blue")
		temp.config(width = 20, height = 1)
		temp.pack(side=LEFT)

		#Description
		temp = Label(frame_table_head,relief=RIDGE, text="Description", bg="light blue")
		temp.config(width = 25, height = 1)
		temp.pack(side=LEFT)

		#Dead Line
		temp = Label(frame_table_head,relief=RIDGE, text="Dead Line", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Priority
		temp = Label(frame_table_head,relief=RIDGE, text="Priority", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task Status
		temp = Label(frame_table_head,relief=RIDGE, text="Task Status", bg="light blue")
		temp.config(width = 15, height = 1)
		temp.pack(side=LEFT)

		#assigned tasks
		frame5 = Frame(self)
		frame5.pack()

		#scrolling part start
		scroll_frame = Frame(frame5)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=150, width=800)
		list_scrollbar.pack(side=RIGHT, fill=Y)
		scroll_canvas.pack(side=LEFT)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack()

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.create_task_table()
		self.task_cur.execute("SELECT ids, a_to, task_list, description, deadline, priority, status FROM tasks WHERE a_by = ?", (self.name,))
		data1 = self.task_cur.fetchall()
		data = []

		for i in range(len(data1)):
			if(data1[i][6] != 'complete'):
				data.append(data1[i])

		self.task_id_btn = []
		for i in range(len(data)):
			self.task_id_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)

			#Task ID
			self.task_id_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(i+1), command=lambda i=i : self.copy_id_to_field(i, data[i][0]), width=7)
			self.task_id_btn[i].pack(side=LEFT)

			#Assigned By
			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Task List
			temp = Label(frame_temp,relief=RIDGE, text=data[i][2], bg="white")
			temp.config(width = 20, height = 1)
			temp.pack(side=LEFT)

			#Description
			temp = Label(frame_temp,relief=RIDGE, text=data[i][3], bg="white")
			temp.config(width = 25, height = 1)
			temp.pack(side=LEFT)

			#Dead Line
			temp = Label(frame_temp,relief=RIDGE, text=data[i][4], bg="tomato")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Priority
			temp = Label(frame_temp,relief=RIDGE, text=data[i][5], bg="white")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Task Status
			temp = Label(frame_temp,relief=RIDGE, text=data[i][6], bg="white")
			temp.config(width = 15, height = 1)
			temp.pack(side=LEFT)

		self.frameBelow = Frame(self)
		self.frameBelow.pack(pady=10)


	def copy_id_to_field(self, i, id):
		#print(self.task_id_btn[i]['text'])
		self.task_id.set(id)
		#print(self.task_id.get())

	def delete_task_window(self):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			self.create_task_table()
			if(self.task_id.get() == ''):
				self.error_msg = "Necessary field(s) cannot be empty!"
				messagebox.showinfo("Error", self.error_msg)
			else:
				try:
					self.task_cur.execute("DELETE FROM tasks WHERE ids = ?", (self.task_id.get(),))
					self.task_conn.commit()
					time.sleep(0.02)
					print("Task corresponding to ID %s has been deleted successfully!" %(self.task_id.get()))
					self.screen = 15
					self.quit()
				except Exception as e:
					self.error_msg = "Error happened!\nError: "+str(e)
					messagebox.showinfo("Error", self.error_msg)

	def edit_task_window(self):
		self.task_conn.close()
		self.screen = 16
		self.quit()
	
	def go_prev(self):
		self.task_conn.close()
		self.screen = 1
		self.quit()

	def leave(self):
		self.task_conn.close()
		quit()  

class update_assign_task_page(Frame):
	screen 			= 13

	status_conn 	= None
	status_cur  	= None
	
	task_conn 		= None
	task_cur  		= None
	
	name        	= None
	task_no 		= None
	
	task_db  		= "./db/tasks.db"

	error_msg  		= " "

	assigned_to_users_list = []

	def __init__(self,master, name, task_no):
		super(update_assign_task_page,self).__init__(master)

		self.login_conn = sqlite3.connect('./db/users.db')
		self.login_cur  = self.login_conn.cursor()

		self.task_conn = sqlite3.connect(self.task_db)
		self.task_cur  = self.task_conn.cursor()

		self.name        = name
		self.task_no 	 = task_no
		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def assign_to_user(self, user):
		if str(user[2:len(user)-3]) not in self.assigned_to_users_list:
			self.assigned_to_users_list.append(str(user[2:len(user)-3]))
			strList = ''
			for i in self.assigned_to_users_list:
				strList = strList + str(i) + ", "
			self.assigned_to_names_str.set(strList)
			print(strList)

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		update_status_label=Label(frame1,text="::Update Assigned Task::")
		update_status_label.config(width=200, font=("Courier", 25))
		update_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		self.create_task_table()
		self.task_cur.execute("SELECT a_to, dates, up_time, task_list, description, est_date, deadline, comments, priority, remarks, status FROM tasks WHERE ids = ? and a_by = ?", (self.task_no, self.name))
		data = self.task_cur.fetchall()
		print(data)

		frameHolder = Frame(self)
		frameHolder.pack()

		frameLeft = Frame(frameHolder)
		frameLeft.pack(side=LEFT, padx=5)

		#Assigned To
		frame2 = Frame(frameLeft)
		frame2.pack()
		
		assigned_to_label=Label(frame2,text="Assign To:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.login_cur.execute("SELECT name FROM users")
		name_list = self.login_cur.fetchall()
		self.login_conn.close()

		self.assigned_to_name=StringVar()
		self.assigned_to_name.set(data[0][0])

		assigned_to_list=OptionMenu(frame2,self.assigned_to_name, *name_list, command = lambda x: self.assign_to_user(self.assigned_to_name.get()))
		assigned_to_list.config(width=35)
		assigned_to_list.pack(side=LEFT, padx=2, pady=5)
		assigned_to_list.focus_set()

		#Assigned List
		frame11 = Frame(frameLeft)
		frame11.pack()
		
		assigned_to_label=Label(frame11,text="Assigned To:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.assigned_to_names_str = StringVar()
		self.assigned_to_users_list = []
		assigned_to_names=Label(frame11, width=43, anchor=W, textvariable=self.assigned_to_names_str)
		assigned_to_names.pack(side=LEFT, pady=5)

		#Task List
		frame3 = Frame(frameLeft)
		frame3.pack()
		
		task_list_label=Label(frame3,text="Task List:", width=20, anchor=W)
		task_list_label.pack(side=LEFT, padx=2, pady=5)

		task_scroll = Scrollbar(frame3)
		self.task_text = Text(frame3, height=4, width=43)
		task_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.task_text.pack(side=LEFT, fill=Y)
		task_scroll.config(command=self.task_text.yview)
		self.task_text.config(yscrollcommand=task_scroll.set)
		self.task_text.insert(END, data[0][3])

		#Task Description
		frame4 = Frame(frameLeft)
		frame4.pack()

		task_des_label=Label(frame4,text="Description:", width=20, anchor=W)
		task_des_label.pack(side=LEFT, padx=2, pady=5)

		task_des_scroll = Scrollbar(frame4)
		self.task_des_text = Text(frame4, height=4, width=43)
		task_des_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.task_des_text.pack(side=LEFT, fill=Y)
		task_des_scroll.config(command=self.task_des_text.yview)
		self.task_des_text.config(yscrollcommand=task_des_scroll.set)
		self.task_des_text.insert(END, data[0][4])

		#Estimated Date
		est_date_str_list = data[0][5].split('-')
		frame5 = Frame(frameLeft)
		frame5.pack()
		
		est_date_label=Label(frame5,text="Est. Date:", width=19, anchor=W)
		est_date_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frame5,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.day_name=StringVar()
		self.day_name.set(est_date_str_list[0])

		day_list=OptionMenu(frame5,self.day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		day_list.pack(side=LEFT, padx=2, pady=5)

		month_label=Label(frame5,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.month_name=StringVar()
		self.month_name.set(est_date_str_list[1])

		month_list=OptionMenu(frame5,self.month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		month_list.pack(side=LEFT, padx=2, pady=5)

		year_label=Label(frame5,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.year_name=StringVar()
		self.year_name.set(est_date_str_list[2])

		year_list=OptionMenu(frame5,self.year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		year_list.pack(side=LEFT, padx=2, pady=5)

		#Deadline
		dead_date_str_list = data[0][6].split('-')
		frame6 = Frame(frameLeft)
		frame6.pack(side=LEFT, padx=5)
		
		deadline_label=Label(frame6,text="Deadline:", width=19, anchor=W)
		deadline_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frame6,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.deadline_day_name=StringVar()
		self.deadline_day_name.set(dead_date_str_list[0])

		deadline_day_list=OptionMenu(frame6,self.deadline_day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		deadline_day_list.pack(side=LEFT, padx=2, pady=5)

		deadline_month_label=Label(frame6,text="Month:", anchor=W)
		deadline_month_label.pack(side=LEFT, pady=5)

		self.deadline_month_name=StringVar()
		self.deadline_month_name.set(dead_date_str_list[1])

		deadline_month_list=OptionMenu(frame6,self.deadline_month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		deadline_month_list.pack(side=LEFT, padx=2, pady=5)

		deadline_year_label=Label(frame6,text="Year:", anchor=W)
		deadline_year_label.pack(side=LEFT, pady=5)

		self.deadline_year_name=StringVar()
		self.deadline_year_name.set(dead_date_str_list[2])

		deadline_year_list=OptionMenu(frame6,self.deadline_year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		deadline_year_list.pack(side=LEFT, padx=2, pady=5)

		frameRight = Frame(frameHolder)
		frameRight.pack()

		#Comments
		frame7 = Frame(frameRight)
		frame7.pack()

		comments_label=Label(frame7,text="Comments:", width=20, anchor=W)
		comments_label.pack(side=LEFT, padx=2, pady=5)

		comments_scroll = Scrollbar(frame7)
		self.comments_text = Text(frame7, height=4, width=43)
		comments_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.comments_text.pack(side=LEFT, fill=Y)
		comments_scroll.config(command=self.comments_text.yview)
		self.comments_text.config(yscrollcommand=comments_scroll.set)
		self.comments_text.insert(END, data[0][7])

		#Priority
		frame8 = Frame(frameRight)
		frame8.pack()
		
		priority_label=Label(frame8,text="Priority:", width=20, anchor=W)
		priority_label.pack(side=LEFT, pady=5, padx=2)

		self.priority_level=StringVar()
		self.priority_level.set(str(data[0][8]))

		priority_list=OptionMenu(frame8,self.priority_level, *[str(i) for i in range(1, 6)])
		priority_list.config(width=35)
		priority_list.pack(side=LEFT, padx=2, pady=5)

		#Remarks
		frame9 = Frame(frameRight)
		frame9.pack()

		remarks_status_label=Label(frame9,text="Remarks:", width=20, anchor=W)
		remarks_status_label.pack(side=LEFT, padx=2, pady=5)

		remarks_scroll = Scrollbar(frame9)
		self.remarks_text = Text(frame9, height=2, width=43)
		remarks_scroll.pack(side=RIGHT, fill=Y, padx = 5)
		self.remarks_text.pack(side=LEFT, fill=Y)
		remarks_scroll.config(command=self.remarks_text.yview)
		self.remarks_text.config(yscrollcommand=remarks_scroll.set)
		self.remarks_text.insert(END, data[0][9])

		#Task Status
		frame10 = Frame(frameRight)
		frame10.pack()
		
		task_status_label=Label(frame10,text="Status:", width=20, anchor=W)
		task_status_label.pack(side=LEFT, pady=5, padx=2)

		self.task_status_level=StringVar()
		self.task_status_level.set(str(data[0][10]))

		task_status_list=OptionMenu(frame10,self.task_status_level, *['discussion', 'in progress', 'incomplete', 'complete', 'delivered'])
		task_status_list.config(width=35)
		task_status_list.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(frameRight)
		frameLast.pack()

		assign_task_btn=Button(frameLast,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.assign_task, width=10)
		assign_task_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)
	
	def assign_task(self):
		if(self.task_text.get("1.0", "end-1c") == '' and len(self.assigned_to_users_list)==0):
			self.error_msg = "Necessary field(s) cannot be empty!"
			messagebox.showinfo("Error", self.error_msg)
		else:
			try:
				self.create_task_table()

				for users in self.assigned_to_users_list:
					ids     = self.task_no
					dates   = datetime.datetime.now().strftime("%d-%b-%Y")
					up_time = datetime.datetime.now().strftime("%H:%M:%S")

					self.task_cur.execute("INSERT INTO tasks(ids, dates, up_time, a_by, a_to, task_list, description, est_date, deadline, comments, priority, remarks, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (ids, dates, up_time, self.name, users, self.task_text.get("1.0", "end-1c"), self.task_des_text.get("1.0", "end-1c"), self.day_name.get()+"-"+self.month_name.get()+"-"+self.year_name.get(), self.deadline_day_name.get()+"-"+self.deadline_month_name.get()+"-"+self.deadline_year_name.get(), self.comments_text.get("1.0", "end-1c"), self.priority_level.get(), self.remarks_text.get("1.0", "end-1c"), self.task_status_level.get()))
					self.task_conn.commit()
					time.sleep(0.02)

				self.task_conn.close()
				print("%s, You have successfully updated assigned task to!" %(self.name))
				self.screen = 15
				self.quit()
			except Exception as e:
				self.error_msg = "Error happened!\nError: "+str(e)
				messagebox.showinfo("Error", self.error_msg)
	
	def go_prev(self):
		self.screen = 15
		self.quit()

	def leave(self):
		quit()

class all_tasks_page(Frame):

	screen = 17

	task_id = None

	task_db= "./db/tasks.db"

	def __init__(self,master):
		super(all_tasks_page,self).__init__(master)
		self.pack()

		self.login_conn= sqlite3.connect('./db/users.db')
		self.login_cur = self.login_conn.cursor()

		self.task_conn = sqlite3.connect(self.task_db)
		self.task_cur  = self.task_conn.cursor()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

	def create_task_table(self):
		self.task_cur.execute("CREATE TABLE IF NOT EXISTS tasks(ids TEXT, dates TEXT, up_time TEXT, a_by TEXT, a_to TEXT, task_list TEXT, description TEXT, est_date TEXT, deadline TEXT, comments TEXT, priority TEXT, remarks TEXT, status TEXT)")

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Tasks::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#Assigned To
		self.create_user_table()
		self.create_task_table()

		frame2 = Frame(self)
		frame2.pack()
		
		assigned_to_label=Label(frame2,text="Assigned To:", width=20, anchor=W)
		assigned_to_label.pack(side=LEFT, pady=5)

		self.login_cur.execute("SELECT name FROM users")
		name_list = self.login_cur.fetchall()
		self.login_conn.close()
		name_list.append('All')

		self.assigned_to_name=StringVar()
		self.assigned_to_name.set("All")

		assigned_to_list=OptionMenu(frame2,self.assigned_to_name, *name_list)
		assigned_to_list.config(width=35)
		assigned_to_list.pack(side=LEFT, padx=2, pady=5)
		assigned_to_list.focus_set()

		frameLast = Frame(self)
		frameLast.pack()

		search_btn=Button(frameLast,text="Search", bg="DeepSkyBlue4", fg = "white", command = lambda x=self.assigned_to_name.get(): self.assign_to_user(self.assigned_to_name.get()), width=10)
		search_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def assign_to_user(self, name):

		self.create_task_table()
		if(name=='All'):
			self.task_cur.execute("SELECT ids, a_by, task_list, description, deadline, priority, status, a_to FROM tasks")
			data = self.task_cur.fetchall()
		else:
			print(self.assigned_to_name.get()[2: len(self.assigned_to_name.get())-3])
			self.task_cur.execute("SELECT ids, a_by, task_list, description, deadline, priority, status, a_to FROM tasks WHERE a_to = ?", (self.assigned_to_name.get()[2: len(self.assigned_to_name.get())-3],))
			data = self.task_cur.fetchall()

		self.frameTable.pack_forget()
		self.frameTable = Frame(self)
		self.frameTable.pack()

		#Table Head
		frame_table_head = Frame(self.frameTable)
		frame_table_head.pack()

		#Task ID
		temp = Label(frame_table_head, relief=RIDGE, text="Serial", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Assigned By
		temp = Label(frame_table_head,relief=RIDGE, text="Assigned By", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Assigned To
		temp = Label(frame_table_head,relief=RIDGE, text="Assigned To", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task List
		temp = Label(frame_table_head,relief=RIDGE, text="Task List", bg="light blue")
		temp.config(width = 20, height = 1)
		temp.pack(side=LEFT)

		#Description
		temp = Label(frame_table_head,relief=RIDGE, text="Description", bg="light blue")
		temp.config(width = 25, height = 1)
		temp.pack(side=LEFT)

		#Dead Line
		temp = Label(frame_table_head,relief=RIDGE, text="Dead Line", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Priority
		temp = Label(frame_table_head,relief=RIDGE, text="Priority", bg="light blue")
		temp.config(width = 10, height = 1)
		temp.pack(side=LEFT)

		#Task Status
		temp = Label(frame_table_head,relief=RIDGE, text="Task Status", bg="light blue")
		temp.config(width = 15, height = 1)
		temp.pack(side=LEFT)

		#assigned tasks
		frame5 = Frame(self.frameTable)
		frame5.pack()

		#scrolling part start
		scroll_frame = Frame(frame5)
		scroll_frame.pack()

		#scroll canvas
		list_scrollbar = Scrollbar(scroll_frame)
		scroll_canvas = Canvas(scroll_frame, height=400, width=890)
		scroll_canvas.pack(side=LEFT, expand=True, fill=Y)
		list_scrollbar.pack(side=LEFT, fill=Y, padx = 5)
		
		list_scrollbar.config(command=scroll_canvas.yview)
		scroll_canvas.config(yscrollcommand=list_scrollbar.set)
		#scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

		lists = Frame(scroll_canvas)
		lists.pack(fill=X)

		scroll_canvas.create_window((0,0), window=lists, anchor="nw")

		self.task_id_btn = []
		for i in range(len(data)):
			self.task_id_btn.append(None)

		for i in range(len(data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)

			#Task ID
			self.task_id_btn[i] = Button(frame_temp, bg="white", fg="black", text=str(i+1), command=lambda i=i : self.envoke_task_details(i, data[i][0]), width=7)
			self.task_id_btn[i].pack(side=LEFT)

			#Assigned By
			temp = Label(frame_temp,relief=RIDGE, text=data[i][1], bg="white")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Assigned To
			temp = Label(frame_temp,relief=RIDGE, text=data[i][7], bg="white")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Task List
			temp = Label(frame_temp,relief=RIDGE, text=data[i][2], bg="white")
			temp.config(width = 20, height = 1)
			temp.pack(side=LEFT)

			#Description
			temp = Label(frame_temp,relief=RIDGE, text=data[i][3], bg="white")
			temp.config(width = 25, height = 1)
			temp.pack(side=LEFT)

			#Dead Line
			temp = Label(frame_temp,relief=RIDGE, text=data[i][4], bg="tomato")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Priority
			temp = Label(frame_temp,relief=RIDGE, text=data[i][5], bg="white")
			temp.config(width = 10, height = 1)
			temp.pack(side=LEFT)

			#Task Status
			temp = Label(frame_temp,relief=RIDGE, text=data[i][6], bg="white")
			temp.config(width = 15, height = 1)
			temp.pack(side=LEFT)

	def envoke_task_details(self, i, id):
		self.task_id = id
		print(self.task_id)
		self.screen = 14
		self.quit()
		#print(id)

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class export_status_report_page(Frame):

	screen = 18

	status_conn = None
	status_cur  = None
	name        = None
	db_name     = "./db/status.db"

	error_msg  = " "

	def __init__(self,master):
		super(export_status_report_page,self).__init__(master)
		self.pack()

		self.login_conn= sqlite3.connect('./db/users.db')
		self.login_cur = self.login_conn.cursor()

		self.status_conn = sqlite3.connect(self.db_name)
		self.status_cur  = self.status_conn.cursor()

		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def create_status_table(self):
		self.status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, up_time TEXT, weeks TEXT, months TEXT, years TEXT, name TEXT, team TEXT,task_list TEXT, progress_status TEXT, meeting_status TEXT, project_status TEXT, remarks TEXT)")

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Reports::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		self.create_user_table()
		self.create_status_table()

		#Status of
		frameUser = Frame(self)
		frameUser.pack()
		
		status_of_label=Label(frameUser,text="User:", anchor=W)
		status_of_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT name FROM status")
		user_list = list(set(self.status_cur.fetchall()))
		user_list.append('All')

		self.status_of_name=StringVar()
		self.status_of_name.set('All')

		status_of_box=OptionMenu(frameUser,self.status_of_name, *user_list)
		status_of_box.pack(side=LEFT, padx=2, pady=5)

		#Of Team
		team_label=Label(frameUser,text="Team:", anchor=W)
		team_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT team FROM status")
		team_list = list(set(self.status_cur.fetchall()))
		team_list.append('All')

		self.team_name=StringVar()
		self.team_name.set('All')

		team_list_box=OptionMenu(frameUser,self.team_name, *team_list)
		team_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Date	
		date_label=Label(frameUser,text="Date:",anchor=W)
		date_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT dates FROM status")
		date_list = list(set(self.status_cur.fetchall()))
		date_list.append('All')

		self.date_name=StringVar()
		self.date_name.set('All')

		date_list_box=OptionMenu(frameUser,self.date_name, *date_list)
		date_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Week
		week_label=Label(frameUser,text="Week:", anchor=W)
		week_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT weeks FROM status")
		week_list = list(set(self.status_cur.fetchall()))
		week_list.append('All')

		self.week_name=StringVar()
		self.week_name.set('All')

		week_list_box=OptionMenu(frameUser,self.week_name, *week_list)
		week_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Month
		month_label=Label(frameUser,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT months FROM status")
		month_list = list(set(self.status_cur.fetchall()))
		month_list.append('All')

		self.month_name=StringVar()
		self.month_name.set('All')

		month_list_box=OptionMenu(frameUser,self.month_name, *month_list)
		month_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Year
		year_label=Label(frameUser,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.status_cur.execute("SELECT years FROM status")
		year_list = list(set(self.status_cur.fetchall()))
		year_list.append('All')

		self.year_name=StringVar()
		self.year_name.set('All')

		year_list_box=OptionMenu(frameUser,self.year_name, *year_list)
		year_list_box.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		search_btn=Button(frameLast,text="Refresh", bg="DeepSkyBlue4", fg = "white", command = lambda : self.make_report(), width=10)
		search_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def make_report(self):
		file_name = "./status/"

		self.frameTable.pack_forget()
		self.frameTable = Frame(self)
		self.frameTable.pack()

		#Status Of
		if(self.status_of_name.get()=='All'):
			name = '*'
			file_name += 'all_'
		else:
			name = str(self.status_of_name.get()[2:len(self.status_of_name.get())-3])
			file_name += name+"_"

		#Team
		if(self.team_name.get()=='All'):
			team = '*'
			file_name += 'all_'
		else:
			team = str(self.team_name.get()[2:len(self.team_name.get())-3])
			file_name += team+"_"

		#Date
		if(self.date_name.get()=='All'):
			date = '*'
			file_name += 'all_'
		else:
			date = str(self.date_name.get()[2:len(self.date_name.get())-3])
			file_name += date+"_"

		#Week
		if(self.week_name.get()=='All'):
			week = '*'
			file_name += 'all_'
		else:
			week = str(self.week_name.get()[2:len(self.week_name.get())-3])
			file_name += week+"_"

		#Month
		if(self.month_name.get()=='All'):
			month = '*'
			file_name += 'all_'
		else:
			month = str(self.month_name.get())
			file_name += month+"_"

		#Year
		if(self.year_name.get()=='All'):
			year = '*'
			file_name += 'all'
		else:
			year = str(self.year_name.get())
			file_name += year

		file_name += ".xlsx"

		self.create_status_table()
		self.status_cur.execute("SELECT dates, name, team, task_list, progress_status, meeting_status, project_status, remarks FROM status WHERE name GLOB ? and team GLOB ? and dates GLOB ? and weeks GLOB ? and months GLOB ? and years GLOB ?", (name, team, date, week, month, year))
		self.data = self.status_cur.fetchall()

		#Table Head

		frame4 = Frame(self.frameTable)
		frame4.pack()

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Date", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="User", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Team", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Task List", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Progress Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Meeting Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Project Status", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Remarks", width=15)
		temp.pack(side=LEFT, pady=2)

		frame5 = Frame(self.frameTable)
		frame5.pack()

		status_scroll = Scrollbar(frame5)
		status_canvas = Canvas(frame5, height=250, width=1016)
		status_scroll.pack(side=RIGHT, fill=Y)
		status_canvas.pack(side=LEFT)
		status_scroll.config(command=status_canvas.yview)
		status_canvas.config(yscrollcommand=status_scroll.set)

		lists = Frame(status_canvas)
		lists.pack()

		status_canvas.create_window((0,0), window=lists, anchor="nw")

		for i in range(len(self.data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][0], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][1], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][2], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][3], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][4], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][5], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][6], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=15, height=1)
			temp.configure(text=self.data[i][7], anchor="nw")
			temp.pack(side=LEFT)

		frameReport = Frame(self.frameTable)
		frameReport.pack()

		export_btn = Button(self.frameTable,text="Export", bg="DeepSkyBlue4", fg = "white", command = lambda : self.save_report(file_name), width=10)
		export_btn.pack(pady=5)

	def save_report(self, file_name):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			try:
				with open(file_name, "w") as csv_file:
					writer = csv.writer(csv_file, delimiter=',')
					writer.writerow(['Date', 'User', 'Team', 'Task List', 'Progress Status', 'Meeting Status', 'Project Status', 'Remarks'])
					for line in self.data:
						writer.writerow(list(line))
					print("Write to ",file_name," is successful!")
					self.screen = 18
					self.quit()
			except Exception as e:
				print(e)

	def go_prev(self):
		self.screen = 22
		self.quit()

	def leave(self):
		quit()

class attendance_page(Frame):
	screen 			= 19
	
	attns_conn 		= None
	attns_cur  		= None
	
	name        	= None
	
	attns_db  		= "./db/attns.db"

	error_msg  		= " "

	def __init__(self,master, name):
		super(attendance_page,self).__init__(master)

		self.attns_conn = sqlite3.connect(self.attns_db)
		self.attns_cur  = self.attns_conn.cursor()

		self.name        = name

		self.pack()
		self.define_widgets()

	def create_attns_table(self):
		self.attns_cur.execute("CREATE TABLE IF NOT EXISTS attns(date TEXT, name TEXT, intime TEXT, outtime TEXT, dates TEXT, weeks TEXT, months TEXT, years TEXT)")

	def define_widgets(self):
		frame1 = Frame(self)
		frame1.pack()
		update_status_label=Label(frame1,text="::Attendance & Food::")
		update_status_label.config(width=200, font=("Courier", 25))
		update_status_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frameHolder = Frame(self)
		frameHolder.pack()

		#Date
		frameDate = Frame(frameHolder)
		frameDate.pack()
		
		date_label=Label(frameDate,text="Date:", width=10, anchor=W)
		date_label.pack(side=LEFT, pady=5, padx=2)

		day_label=Label(frameDate,text="Day:", anchor=W)
		day_label.pack(side=LEFT, pady=5)

		self.day_name=StringVar()
		self.day_name.set(datetime.datetime.now().strftime("%d"))

		day_list=OptionMenu(frameDate,self.day_name, *[str(i) for i in range(1, 32)])
		#day_list.config(width=5)
		day_list.pack(side=LEFT, padx=2, pady=5)

		month_label=Label(frameDate,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.month_name=StringVar()
		self.month_name.set(datetime.datetime.now().strftime("%b"))

		month_list=OptionMenu(frameDate,self.month_name, *['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
		#month_list.config(width=5)
		month_list.pack(side=LEFT, padx=2, pady=5)

		year_label=Label(frameDate,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.year_name=StringVar()
		self.year_name.set(datetime.datetime.now().strftime("%Y"))

		year_list=OptionMenu(frameDate,self.year_name, *[str(i) for i in range(2011, 2021)])
		#year_list.config(width=5)
		year_list.pack(side=LEFT, padx=2, pady=5)

		#In time
		frame5 = Frame(frameHolder)
		frame5.pack()
		
		in_time_label=Label(frame5,text="In Time:", width=25, anchor=W)
		in_time_label.pack(side=LEFT, pady=5, padx=2)

		in_hour_label=Label(frame5,text="Hour:", anchor=W)
		in_hour_label.pack(side=LEFT, pady=5)

		self.in_hour_name=StringVar()
		self.in_hour_name.set(datetime.datetime.now().strftime("%H"))

		in_hour_list=OptionMenu(frame5,self.in_hour_name, *[str(i) for i in range(1, 25)])
		in_hour_list.pack(side=LEFT, padx=2, pady=5)

		in_minute_label=Label(frame5,text="Minute:", anchor=W)
		in_minute_label.pack(side=LEFT, pady=5)

		self.in_minute_name=StringVar()
		self.in_minute_name.set(datetime.datetime.now().strftime("%M"))

		in_minute_list=OptionMenu(frame5,self.in_minute_name, *[str(i) for i in range(0, 61, 5)])
		in_minute_list.pack(side=LEFT, padx=2, pady=5)

		#Out time
		frame5 = Frame(frameHolder)
		frame5.pack()

		out_time_label=Label(frame5,text="In Time:", width=25, anchor=W)
		out_time_label.pack(side=LEFT, pady=5, padx=2)

		out_hour_label=Label(frame5,text="Hour:", anchor=W)
		out_hour_label.pack(side=LEFT, pady=5)

		self.out_hour_name=StringVar()
		self.out_hour_name.set(datetime.datetime.now().strftime("%H"))

		out_hour_list=OptionMenu(frame5,self.out_hour_name, *[str(i) for i in range(1, 25)])
		out_hour_list.pack(side=LEFT, padx=2, pady=5)

		out_minute_label=Label(frame5,text="Minute:", anchor=W)
		out_minute_label.pack(side=LEFT, pady=5)

		self.out_minute_name=StringVar()
		self.out_minute_name.set(datetime.datetime.now().strftime("%M"))

		out_minute_list=OptionMenu(frame5,self.out_minute_name, *[str(i) for i in range(0, 61, 5)])
		out_minute_list.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(frameHolder)
		frameLast.pack()

		update_btn=Button(frameLast,text="Update", bg="DeepSkyBlue4", fg = "white", command=self.attendance_done, width=10)
		update_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)
	
	def attendance_done(self):
		try:
			month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
			dates   = self.day_name.get()+"-"+self.month_name.get()+"-"+self.year_name.get()
			weeks   = datetime.date(int(self.year_name.get()), int(month_dict[self.month_name.get()]), int(self.day_name.get())).isocalendar()[1]
			months  = self.month_name.get()
			years   = self.year_name.get()

			self.create_attns_table()
			self.attns_cur.execute("SELECT * FROM attns WHERE name = ? and dates = ?", (self.name, dates))
			data = self.attns_cur.fetchall()

			if(len(data)==0):
				self.attns_cur.execute("INSERT INTO attns(name, intime, outtime, dates, weeks, months, years) VALUES (?,?,?,?,?,?,?)", (self.name, self.in_hour_name.get()+":"+self.in_minute_name.get(), self.out_hour_name.get()+":"+self.out_minute_name.get(), dates, weeks, months, years))
				self.attns_conn.commit()
				time.sleep(0.02)
			else:
				self.attns_cur.execute("UPDATE attns SET name = ?, intime = ?, outtime = ?, dates = ?, weeks = ?, months = ?, years = ? WHERE dates = ?", (self.name, self.in_hour_name.get()+":"+self.in_minute_name.get(), self.out_hour_name.get()+":"+self.out_minute_name.get(), dates, weeks, months, years, dates))
				self.attns_conn.commit()
				time.sleep(0.02)

			self.attns_conn.close()
			print("%s, You have successfully gave your attendance!" %(self.name))
			self.screen = 19
			self.quit()
		except Exception as e:
			self.error_msg = "Error happened!\nError: "+str(e)
			messagebox.showinfo("Error", self.error_msg)
	
	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

class export_attendance_report_page(Frame):

	screen = 20

	status_conn = None
	status_cur  = None
	name        = None

	error_msg  = " "

	def __init__(self,master):
		super(export_attendance_report_page,self).__init__(master)
		self.pack()

		self.login_conn= sqlite3.connect('./db/users.db')
		self.login_cur = self.login_conn.cursor()

		self.attns_conn = sqlite3.connect('./db/attns.db')
		self.attns_cur  = self.attns_conn.cursor()

		self.pack()
		self.define_widgets()

	def create_user_table(self):
		self.login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, admin_status TEXT)")

	def create_attns_table(self):
		self.attns_cur.execute("CREATE TABLE IF NOT EXISTS attns(name TEXT, intime TEXT, outtime TEXT, dates TEXT, weeks TEXT, months TEXT, years TEXT)")

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Attendance::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		self.create_user_table()
		self.create_attns_table()

		#Status of
		frameUser = Frame(self)
		frameUser.pack()
		
		status_of_label=Label(frameUser,text="User:", anchor=W)
		status_of_label.pack(side=LEFT, pady=5)

		self.attns_cur.execute("SELECT name FROM attns")
		status_of_list = list(set(self.attns_cur.fetchall()))
		status_of_list.append('All')

		self.status_of_name=StringVar()
		self.status_of_name.set('All')

		status_of_box=OptionMenu(frameUser,self.status_of_name, *status_of_list)
		status_of_box.pack(side=LEFT, padx=2, pady=5)

		#Of Date	
		date_label=Label(frameUser,text="Date:",anchor=W)
		date_label.pack(side=LEFT, pady=5)

		self.attns_cur.execute("SELECT dates FROM attns")
		date_list = list(set(self.attns_cur.fetchall()))
		date_list.append('All')

		self.date_name=StringVar()
		self.date_name.set('All')

		date_list_box=OptionMenu(frameUser,self.date_name, *date_list)
		date_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Week
		week_label=Label(frameUser,text="Week:", anchor=W)
		week_label.pack(side=LEFT, pady=5)

		self.attns_cur.execute("SELECT weeks FROM attns")
		week_list = list(set(self.attns_cur.fetchall()))
		week_list.append('All')

		self.week_name=StringVar()
		self.week_name.set('All')

		week_list_box=OptionMenu(frameUser,self.week_name, *week_list)
		week_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Month
		month_label=Label(frameUser,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.attns_cur.execute("SELECT months FROM attns")
		month_list = list(set(self.attns_cur.fetchall()))
		month_list.append('All')

		self.month_name=StringVar()
		self.month_name.set('All')

		month_list_box=OptionMenu(frameUser,self.month_name, *month_list)
		month_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Year
		year_label=Label(frameUser,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.attns_cur.execute("SELECT years FROM attns")
		year_list = list(set(self.attns_cur.fetchall()))
		year_list.append('All')

		self.year_name=StringVar()
		self.year_name.set('All')

		year_list_box=OptionMenu(frameUser,self.year_name, *year_list)
		year_list_box.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		search_btn=Button(frameLast,text="Refresh", bg="DeepSkyBlue4", fg = "white", command = lambda : self.make_report(), width=10)
		search_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def make_report(self):
		file_name = "./attendance/"

		self.frameTable.pack_forget()
		self.frameTable = Frame(self)
		self.frameTable.pack()

		#Status Of
		if(self.status_of_name.get()=='All'):
			name = '*'
			file_name += 'all_'
		else:
			name = str(self.status_of_name.get()[2:len(self.status_of_name.get())-3])
			file_name += name+"_"

		#Date
		if(self.date_name.get()=='All'):
			date = '*'
			file_name += 'all_'
		else:
			date = str(self.date_name.get()[2:len(self.date_name.get())-3])
			file_name += date+"_"

		#Week
		if(self.week_name.get()=='All'):
			week = '*'
			file_name += 'all_'
		else:
			week = str(self.week_name.get()[2:len(self.week_name.get())-3])
			file_name += week+"_"

		#Month
		if(self.month_name.get()=='All'):
			month = '*'
			file_name += 'all_'
		else:
			month = str(self.month_name.get())
			file_name += month+"_"

		#Year
		if(self.year_name.get()=='All'):
			year = '*'
			file_name += 'all'
		else:
			year = str(self.year_name.get())
			file_name += year

		file_name += ".xlsx"

		self.create_attns_table()
		self.attns_cur.execute("SELECT name, intime, outtime, dates FROM attns WHERE name GLOB ? and dates GLOB ? and weeks GLOB ? and months GLOB ? and years GLOB ?", (name, date, week, month, year))
		self.data = self.attns_cur.fetchall()

		#Table Head

		frame4 = Frame(self.frameTable)
		frame4.pack()

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Date", width=15)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="User", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="In Time", width=20)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Out Time", width=20)
		temp.pack(side=LEFT, pady=2)

		frame5 = Frame(self.frameTable)
		frame5.pack()

		status_scroll = Scrollbar(frame5)
		status_canvas = Canvas(frame5, height=250, width=518)
		status_scroll.pack(side=RIGHT, fill=Y)
		status_canvas.pack(side=LEFT)
		status_scroll.config(command=status_canvas.yview)
		status_canvas.config(yscrollcommand=status_scroll.set)

		lists = Frame(status_canvas)
		lists.pack()

		status_canvas.create_window((0,0), window=lists, anchor="nw")

		for i in range(len(self.data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=15, height=1)
			temp.configure(text=self.data[i][3], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=self.data[i][0], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][1], anchor="nw")
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=20, height=1)
			temp.configure(text=self.data[i][2], anchor="nw")
			temp.pack(side=LEFT)

		frameReport = Frame(self.frameTable)
		frameReport.pack()

		export_btn = Button(self.frameTable,text="Export", bg="DeepSkyBlue4", fg = "white", command = lambda : self.save_report(file_name), width=10)
		export_btn.pack(pady=5)

	def save_report(self, file_name):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			try:
				with open(file_name, "w") as csv_file:
					writer = csv.writer(csv_file, delimiter=',')
					writer.writerow(['Date', 'User', 'In time', 'Out Time'])
					for line in self.data:
						writer.writerow(list(line))
					print("Write to ",file_name," is successful!")
					self.screen = 20
					self.quit()
			except Exception as e:
				print(e)

	def go_prev(self):
		self.screen = 22
		self.quit()

	def leave(self):
		quit()

class export_food_report_page(Frame):

	screen = 21

	food_conn 	= None
	food_cur  	= None
	name        = None

	error_msg  = " "

	def __init__(self,master):
		super(export_food_report_page,self).__init__(master)
		self.pack()

		self.food_conn = sqlite3.connect('./db/foods.db')
		self.food_cur  = self.food_conn.cursor()

		self.pack()
		self.define_widgets()

	def create_food_table(self):
		self.food_cur.execute("CREATE TABLE IF NOT EXISTS foods(name TEXT, value TEXT, dates TEXT, weeks TEXT, months TEXT, years TEXT)")

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Food Report::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		#Status of
		frameUser = Frame(self)
		frameUser.pack()
		
		status_of_label=Label(frameUser,text="User:", anchor=W)
		status_of_label.pack(side=LEFT, pady=5)

		self.create_food_table()
		self.food_cur.execute("SELECT name FROM foods")
		user_list = list(set(self.food_cur.fetchall()))
		user_list.append('All')

		self.status_of_name=StringVar()
		self.status_of_name.set('All')

		status_of_box=OptionMenu(frameUser,self.status_of_name, *user_list)
		status_of_box.pack(side=LEFT, padx=2, pady=5)

		#Of Date	
		date_label=Label(frameUser,text="Date:",anchor=W)
		date_label.pack(side=LEFT, pady=5)

		self.food_cur.execute("SELECT dates FROM foods")
		date_list = list(set(self.food_cur.fetchall()))
		date_list.append('All')

		self.date_name=StringVar()
		self.date_name.set('All')

		date_list_box=OptionMenu(frameUser,self.date_name, *date_list)
		date_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Week
		week_label=Label(frameUser,text="Week:", anchor=W)
		week_label.pack(side=LEFT, pady=5)

		self.food_cur.execute("SELECT weeks FROM foods")
		week_list = list(set(self.food_cur.fetchall()))
		week_list.append('All')

		self.week_name=StringVar()
		self.week_name.set('All')

		week_list_box=OptionMenu(frameUser,self.week_name, *week_list)
		week_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Month
		month_label=Label(frameUser,text="Month:", anchor=W)
		month_label.pack(side=LEFT, pady=5)

		self.food_cur.execute("SELECT months FROM foods")
		month_list = list(set(self.food_cur.fetchall()))
		month_list.append('All')

		self.month_name=StringVar()
		self.month_name.set('All')

		month_list_box=OptionMenu(frameUser,self.month_name, *month_list)
		month_list_box.pack(side=LEFT, padx=2, pady=5)

		#Of Year
		year_label=Label(frameUser,text="Year:", anchor=W)
		year_label.pack(side=LEFT, pady=5)

		self.food_cur.execute("SELECT years FROM foods")
		year_list = list(set(self.food_cur.fetchall()))
		year_list.append('All')

		self.year_name=StringVar()
		self.year_name.set('All')

		year_list_box=OptionMenu(frameUser,self.year_name, *year_list)
		year_list_box.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		search_btn=Button(frameLast,text="Refresh", bg="DeepSkyBlue4", fg = "white", command = lambda : self.make_report(), width=10)
		search_btn.pack(side=LEFT, padx=2, pady=5)

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def make_report(self):
		file_name = "./food/"

		self.frameTable.pack_forget()
		self.frameTable = Frame(self)
		self.frameTable.pack()

		#Status Of
		if(self.status_of_name.get()=='All'):
			name = '*'
			file_name += 'all_'
		else:
			name = str(self.status_of_name.get()[2:len(self.status_of_name.get())-3])
			file_name += name+"_"

		#Date
		if(self.date_name.get()=='All'):
			date = '*'
			file_name += 'all_'
		else:
			date = str(self.date_name.get()[2:len(self.date_name.get())-3])
			file_name += date+"_"

		#Week
		if(self.week_name.get()=='All'):
			week = '*'
			file_name += 'all_'
		else:
			week = str(self.week_name.get()[2:len(self.week_name.get())-3])
			file_name += week+"_"

		#Month
		if(self.month_name.get()=='All'):
			month = '*'
			file_name += 'all_'
		else:
			month = str(self.month_name.get())
			file_name += month+"_"

		#Year
		if(self.year_name.get()=='All'):
			year = '*'
			file_name += 'all'
		else:
			year = str(self.year_name.get())
			file_name += year

		file_name += ".xlsx"

		self.create_food_table()
		self.food_cur.execute("SELECT name, value, dates FROM foods WHERE name GLOB ? and dates GLOB ? and weeks GLOB ? and months GLOB ? and years GLOB ?", (name, date, week, month, year))
		data1 = self.food_cur.fetchall()
		self.data = []

		for i in data1:
			if(int(i[1])==1):
				self.data.append(i)
		print(self.data)

		#Table Head

		frame4 = Frame(self.frameTable)
		frame4.pack()

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Serial", width=10)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="Date", width=15)
		temp.pack(side=LEFT, pady=2)

		temp = Label(frame4,relief=RIDGE, bg="light blue", text="User", width=30)
		temp.pack(side=LEFT, pady=2)

		frame5 = Frame(self.frameTable)
		frame5.pack()

		status_scroll = Scrollbar(frame5)
		status_canvas = Canvas(frame5, height=250, width=436)
		status_scroll.pack(side=RIGHT, fill=Y)
		status_canvas.pack(side=LEFT)
		status_scroll.config(command=status_canvas.yview)
		status_canvas.config(yscrollcommand=status_scroll.set)

		lists = Frame(status_canvas)
		lists.pack()

		status_canvas.create_window((0,0), window=lists, anchor="nw")

		for i in range(len(self.data)):
			frame_temp = Frame(lists)
			frame_temp.pack(fill=BOTH)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=10, height=1)
			temp.configure(text=str(i+1))
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=15, height=1)
			temp.configure(text=self.data[i][2])
			temp.pack(side=LEFT)
	
			temp = Label(frame_temp,relief=RIDGE, bg="white", width=30, height=1)
			temp.configure(text=self.data[i][0])
			temp.pack(side=LEFT)

		frameTotal = Frame(self.frameTable)
		frameTotal.pack()

		temp = Label(frameTotal, text= "Total: ", fg='red', width=10, height=1)
		temp.config(font=("Courier", 20))
		temp.pack(side=LEFT)

		temp = Label(frameTotal, text= str(len(self.data)), fg='red', width=10, height=1)
		temp.config(font=("Courier", 20))
		temp.pack(side=LEFT)

		frameReport = Frame(self.frameTable)
		frameReport.pack()

		export_btn = Button(self.frameTable,text="Export", bg="DeepSkyBlue4", fg = "white", command = lambda : self.save_report(file_name, str(len(self.data))), width=10)
		export_btn.pack(pady=5)

	def save_report(self, file_name, total):
		if(messagebox.askyesno("Warning", "Are you sure?")):
			try:
				with open(file_name, "w") as csv_file:
					writer = csv.writer(csv_file, delimiter=',')
					writer.writerow(['Serial', 'Date', 'User'])
					i = 1
					for line in self.data:
						writer.writerow([str(i), line[2], line[0]])
					writer.writerow(['\n'])
					writer.writerow(['', 'Total', total])
					print("Write to ",file_name," is successful!")
					self.screen = 20
					self.quit()
			except Exception as e:
				print(e)

	def go_prev(self):
		self.screen = 22
		self.quit()

	def leave(self):
		quit()

class export_report_page(Frame):

	screen = 22

	error_msg  = " "

	def __init__(self,master):
		super(export_report_page,self).__init__(master)
		self.pack()

		self.pack()
		self.define_widgets()

	def define_widgets(self):
		#for line1:
		frame1 = Frame(self)
		frame1.pack()
		dash_board_label=Label(frame1,text="::Export Reports::")
		dash_board_label.config(width=200, font=("Courier", 25))
		dash_board_label.pack(pady=5)

		canvas = Canvas(frame1, height=2, borderwidth=0, highlightthickness=0, bg="black")
		canvas.pack(fill=X, padx=80, pady=10)

		frameButton = Frame(self)
		frameButton.pack()

		export_status_btn=Button(frameButton,text="Export\nStatus\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(18), width=10, height=3)
		export_status_btn.pack(side=LEFT, padx=2, pady=5)

		export_attns_btn=Button(frameButton,text="Export\nAttendance\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(20), width=10, height=3)
		export_attns_btn.pack(side=LEFT, padx=2, pady=5)

		export_food_btn=Button(frameButton,text="Export\nFood\nReport", bg="DeepSkyBlue4", fg = "white", command = lambda : self.set_value(21), width=10, height=3)
		export_food_btn.pack(side=LEFT, padx=2, pady=5)

		frameLast = Frame(self)
		frameLast.pack()

		back=Button(frameLast,text="< Prev", command=self.go_prev, width=10)
		back.pack(side=LEFT, padx=2, pady=5)

		exit=Button(frameLast,text="Exit", bg = "brown3", fg = "white", command=self.leave, width=10)
		exit.pack(side=LEFT, padx=2, pady=5)

		self.frameTable = Frame(self)
		self.frameTable.pack()

	def set_value(self, value):
		self.screen = value
		self.quit()

	def go_prev(self):
		self.screen = 1
		self.quit()

	def leave(self):
		quit()

root=Tk()
root.title("NSL - Employee daily status update software")
root.geometry("1200x750")

header_img = PhotoImage(file='./img/nslHeader.png')
header = Button(root, relief=FLAT, image = header_img, height = 140, bg="white")
header.pack(fill=X)

bottom_text = Label(root, text = "Developed by: AKM Uday Hasan Bhuiyan. © 2018")
bottom_text.pack(pady=4, side=BOTTOM)

bottom_line = Canvas(root, height=2, borderwidth=0, highlightthickness=0, bg="black")
bottom_line.pack(fill=X, padx=80, side=BOTTOM)

window=login_page(root)
screen=window.screen

name=None
admin=None
task_id=0
prev_screen = None

while True:
	root.mainloop()

	if screen==0:
		name=window.login_name.get()
		admin=window.admin
	if screen==1:
		task_id = window.task_id

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
		window=user_dashboard(root, name, admin)
		task_id = window.task_id
		prev_screen = 1
	elif screen==2:
		window=add_user_page(root)
	elif screen==3:
		window=edit_user_admin_sts_page(root, name)
	elif screen==4:
		window=edit_user_email_page(root)
	elif screen==5:
		window=edit_user_pass_page(root, name)
	elif screen==6:
		window=delete_user_page(root, name)
	elif screen==7:
		window=forgot_pass_page(root)
	elif screen==8:
		window=update_status_page(root, name)
	elif screen==9:
		window=edit_status_page(root, name)
	elif screen==12:
		window=forgot_id_page(root)
	elif screen==13:
		window=assign_task_page(root, name)
	elif screen==14:
		task_id = window.task_id
		window=task_description_page(root, name, task_id, prev_screen)
	elif screen==15:
		window=edit_assign_task_page(root, name)
	elif screen==16:
		task_id = window.task_id.get()
		window=update_assign_task_page(root, name, task_id)
	elif screen==17:
		window=all_tasks_page(root)
		prev_screen = 17
	elif screen==18:
		window=export_status_report_page(root)
	elif screen==19:
		window=attendance_page(root, name)
	elif screen==20:
		window=export_attendance_report_page(root)
	elif screen==21:
		window=export_food_report_page(root)
	elif screen==22:
		window=export_report_page(root)
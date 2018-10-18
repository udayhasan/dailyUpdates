#!/usr/bin/python3
import sqlite3
import smtplib
import time
import datetime

login_conn = sqlite3.connect('users.db')
login_cur  = login_conn.cursor()

status_conn = sqlite3.connect('status.db')
status_cur  = status_conn.cursor()

error_msg  = " "

def create_user_table():
	login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

def add_user(name, email, password):
	if(name == '' or email == '' or password == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", (name, email, password))
			login_conn.commit()
			time.sleep(0.02)
			print("New User named %s is added to the database" %(name))
		except Exception:
			error_msg = "Invalid input"

def edit_user_name(cur_name, new_name):
	if(cur_name == '' or new_name == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("UPDATE users SET name = ? WHERE name = ?", (new_name, cur_name))
			login_conn.commit()
			print("User name %s is replaced by %s" %(cur_name, new_name))
		except Exception:
			error_msg = "Invalid search name or replacing name!"

def edit_user_email(name, new_email):
	if(name == '' or new_email == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("UPDATE users SET email = ? WHERE name = ?", (new_email, name))
			login_conn.commit()
			print("User email for %s is replaced by %s" %(name, new_email))
		except Exception:
			error_msg = "Invalid search name or replacing email address!"

def edit_user_password(name, cur_password, new_password):
	if(name == '' or cur_password == '' or new_password == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("UPDATE users SET password = ? WHERE name = ? and password = ?", (new_password, name, cur_password))
			login_conn.commit()
			print("Password for %s is changed successfully!" %(name))
		except Exception:
			error_msg = "Invalid search name or previous password or new password!"

def delete_user(name):
	if(name == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("DELETE FROM users WHERE name = ?", (name,))
			login_conn.commit()
			print("User named %s has been deleted successfully!" %(name))
		except Exception:
			error_msg = "Invalid search name!"
	print(error_msg)

def forget_password(name, email):
	if(name == '' or email == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("SELECT password FROM users WHERE name = ? and email = ?", (name, email))
			password = login_cur.fetchall()

			me  	= "noreply.nslstatus@gmail.com"
			you 	= email
			subject = "Account recovery"
			body 	= "Dear "+name+",\nYour lost password is :"+str(password[0][0])+"\nN.B: You don't need to reply this message.\nThanks."

			server  = smtplib.SMTP("smtp.gmail.com", 25)
			server.ehlo()
			server.starttls()
			server.login(me, 'a1234567890z')
			server.sendmail(me, you, body)
			server.quit()

		except Exception as e:
			print(e)
			error_msg = "Invalid search name or email!"

def login(name, password):
	if(name == '' or password == ''):
		error_msg = "Invalid input!"
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

def create_status_table():
	status_cur.execute("CREATE TABLE IF NOT EXISTS status(ids TEXT, dates TEXT, times TEXT, months TEXT, name TEXT, task_list TEXT, progress_status TEXT, meeting_status TEXT, remarks TEXT)")

def update_status(ids, dates, times, months,  name, task_list, progress_status, meeting_status, remarks):
	if(ids == '' and name == ''):
		error_msg = "Insufficient inputs!"
	else:
		try:
			status_cur.execute("INSERT INTO status(ids, dates, times, months, name, task_list, progress_status, meeting_status, remarks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (ids, dates, times, months, name, task_list, progress_status, meeting_status, remarks))
			status_conn.commit()
			time.sleep(0.02)
			print("%s, You have successfully updated your daily status!" %(name))
		except Exception:
			error_msg = "Invalid inputs!"



create_user_table()

#print("Add user.")
#name = str(input("Name: "))
#email = str(input("E-mail: "))
#password = str(input("Password: "))
#add_user(name, email, password)

#print("Change user name.")
#cur_name = str(input("Current name: "))
#new_name = str(input("New name: "))
#edit_user_name(cur_name, new_name)

#print("Change email address.")
#cur_email = str(input("Current email: "))
#new_email = str(input("New email: "))
#edit_user_email(cur_email, new_email)

#print("Change password.")
#cur_password = str(input("Current password: "))
#new_password = str(input("New password: "))
#edit_user_password(name, cur_password, new_password)

#print("Delete user.")
#name = str(input("Name: "))
#delete_user(name)

#print("Recover password.")
#name = str(input("Name: "))
#email = str(input("E-mail: "))
#forget_password(name, email)

print("Account login.")
name = str(input("Name: "))
password = str(input("Password: "))
success, admin = login(name, password)

create_status_table()

print(error_msg)

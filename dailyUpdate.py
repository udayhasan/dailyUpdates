#!/usr/bin/python3
import sqlite3

login_conn = sqlite3.connect('users.db')
login_cur  = login_conn.cursor()
error_msg  = ""

def create_user_table():
	login_cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT)")

def add_user(name, email, password):
	if(name == '' or email == '' or password == ''):
		error_msg = "Invalid input!"
	else:
		try:
			login_cur.execute("INSERT INTO users(name, email, password) VALUES (?, ?, ?)", (name, email, password))
			login_conn.commit()
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
			print("Your Password is: ", password[0][0])
		except Exception:
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
				print(check)
				print("Password Matched!")
				success = 1
				if(name == 'admin'): admin = 1
				else: admin = 0
			else:
				print("Incorrect Password!")
				error_msg = "Incorrect Password!"
				success = 0
				admin   = 0
		except Exception:
			error_msg = "Invalid login name or password!"

create_user_table()

#add_user(str(input()), str(input()), str(input()))
#edit_user_name(str(input()), str(input()))
#edit_user_email(str(input()), str(input()))
#edit_user_password(str(input()), str(input()), str(input()))
#delete_user(str(input()))
#forget_password(str(input()), str(input()))
login(str(input()), str(input()))
print(error_msg)

'''
	File    : app.py
	Project : Kuzu Bank App
	Author  : Karta Kusuma
	Version : 1.0.0
'''

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector as mysql
import os


class Login:
	def __init__(self, root):
		self.root = root
		width = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.title('KuzuBank')
		self.root.geometry(f'{width}x{height}+0+0')
		self.root.iconbitmap('logo/kuzubank-logo.ico')
		self.con = mysql.connect(host='localhost', user='root', password='12345', database='kuzubank')
		self.cur = self.con.cursor()
		self.loginForm()

	def check_login(self):
		name = self.user_field.get()
		pswd = self.pass_field.get()
		loginQuery = "SELECT `user_id` FROM `users` WHERE `username`='"+str(name)+"' AND `password`='"+pswd+"'"
		#print(loginQuery)
		getUsernameQuery = "SELECT `username` FROM `users` WHERE `username`='"+str(name)+"' AND `password`='"+pswd+"'"
		#print(getUsernameQuery)
		if name=="" or pswd=="":
			messagebox.showerror('Error', 'All fields are required\nSemua kolom diperlukan', parent=self.root)
		else:
			try:
				#print(1)
				self.cur.execute(loginQuery)
				idCurrent = self.cur.fetchone()
				if idCurrent==None:
					messagebox.showerror('Error', 'Invalid Username and Password\n\nUsername dan Password tidak valid',\
					parent=self.root)
				else:
					#cur.execute(getUserIdQuery)
					#idCurrent = cur.fetchone()
					self.cur.execute(getUsernameQuery)
					userCurrent= self.cur.fetchone()
					self.currentUserId = idCurrent[0]
					self.currentUsername = userCurrent[0]
					#print(self.currentUsername, self.currentUserId)
					self.activeUser()
					self.cleanField()
					self.con.close()
					os.system('python main.py')
			except Exception as e:
				messagebox.showerror('Error', str(e), parent=self.root)
				print(e)

	def activeUser(self):
		getUserActiveQuery = "SELECT * FROM `activeuser` WHERE `id`='1'"
		try:
			self.cur.execute(getUserActiveQuery)
		except Exception as e:
			messagebox.showerror('Error', str(e), parent=self.root)
		user_active = self.cur.fetchone()
		
		if user_active != None:
			updateActiveUserQuery = "UPDATE `activeuser` SET `user_id` ='"+str(self.currentUserId)+"' WHERE (`id` = '1')"
			try:
				self.cur.execute(updateActiveUserQuery)
				self.con.commit()
				#print('berhasil')
			except Exception as ex:
				messagebox.showerror('Error', str(ex), parent=self.root)
			print('>>Filled')
		else:
			try:
				insertUserActiveQuery = "INSERT INTO `activeuser` (`id`, `user_id`) VALUES ('1', '"+str(self.currentUserId)+"')"
				self.cur.execute(insertUserActiveQuery)
				self.con.commit()
			except Exception as exc:
				messagebox.showerror(exc)
			print('>>None')

	def reConnect(self):
		self.con.close()
		self.con = mysql.connect(host='localhost', user='root', password='12345', database='kuzubank')
		self.cur = self.con.cursor()

	def signUp(self):
		messagebox.showinfo('Information', 'Please contact our Costumer Service first to get authentication numbers\n\n'\
							'Hubungi Costumer Service kami terlebih dahulu untuk mendapatkan nomor autentikasi', parent=self.root)
		os.system('python signup.py')
		self.reConnect()

	def cleanField(self):
		self.user_field.delete(0, END)
		self.pass_field.delete(0, END)

	def loginForm(self):
		#Frame
		frame_main = Frame(self.root, bg='#81baff')
		frame_main.place(relwidth=1, relheight=1, relx=0, rely=0)
		frame_login = Frame(self.root, bg='#cacaca')
		frame_login.place(relwidth=0.6, relheight=0.7, relx=0.2, rely=0.175)
		#Gambar
		self.image_src = ImageTk.PhotoImage(Image.open('logo/kuzu-big-new-small.png'))
		legend_img = Label(frame_main, image=self.image_src, bg='#81baff')
		legend_img.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
		#Login form
		login = Label(frame_login, text='Login', fg='#eaeaea', bg='#00003a', font='Arial 50')
		login.place(relwidth=1, relheight=0.175, relx=0, rely=0)
		user_label = Label(frame_login, text='Username', fg='#00003a', bg='#cacaca', font='Arial 20')
		user_label.place(relwidth=1, relheight=0.1, relx=0, rely=0.225)
		self.user_field = Entry(frame_login, fg='#00003a', bg='#ffffff', font='Arial 20')
		self.user_field.place(relwidth=0.7, relheight=0.1, relx=0.15, rely=0.325)
		pass_label = Label(frame_login, text='Password', fg='#00003a', bg='#cacaca', font='Arial 20')
		pass_label.place(relwidth=1, relheight=0.1, relx=0, rely=0.45)
		self.pass_field = Entry(frame_login, fg='#00003a', bg='#ffffff', font='Arial 20')
		self.pass_field.config(show='*')
		self.pass_field.place(relwidth=0.7, relheight=0.1, relx=0.15, rely=0.55)
		#Button
		button_login = Button(frame_login, text='Login', fg='#eaeaea', bg='#ac0000', font='Arial 20', cursor='hand2',\
		command=self.check_login)
		button_login.place(relwidth=0.2, relheight=0.15, relx=0.4, rely=0.75)
		button_signup = Button(frame_main, text='Sign Up', fg='#eaeaea', bg='#ac0000', font='Arial 16', cursor='hand2',\
		command=self.signUp)
		button_signup.place(relwidth=0.1, relheight=0.05, relx=0.015, rely=0.025)

root = Tk()
obj = Login(root)
root.mainloop()
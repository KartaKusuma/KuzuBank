'''
	File	: signup.py
	Project	: Kuzu Bank App
	Author	: Karta Kusuma
	Version	: 1.0.0
'''

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector as mysql
import os

class SignUp:
	def __init__(self, root):
		self.root = root
		width  = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.title('Register')
		self.root.geometry(f'{width}x{height}+0+0')
		self.root.iconbitmap('logo/kuzubank-logo.ico')
		self.image_src = ImageTk.PhotoImage(Image.open('logo/kuzu-big-new.png'))
		self.connection = mysql.connect(host='localhost', user='root', password='12345', database='kuzubank')
		self.cursor = self.connection.cursor()
		self.initUI()

	def callHelp(self):
		os.system('python show_help.py')

	def goToLogin(self):
		root.quit()

	def cleanField(self, fl1, fl2, fl3, fl4, fl5, fl6):
		fl1.delete(0, END)
		fl2.delete(0, END)
		fl3.delete(0, END)
		fl4.delete(0, END)
		fl5.delete(0, END)
		fl6.delete(0, END)

	def availableUser(self):
		status = False
		username_in = str(self.username_field.get())
		#Fetching available username from database
		queryGetAvailableUser = "SELECT username FROM users"
		self.cursor.execute(queryGetAvailableUser)
		available_user = self.cursor.fetchall()
		print(available_user)
		for username in available_user:
			username = ''.join(username)
			print(username)
			if username_in == username:
				status = True
				break
		#print(username)
		if status == True:
			return True
		else:
			return False
		

	def formCheck(self):
		#Getting user fields
		self.username = str(self.username_field.get())
		self.password = str(self.password_field.get())
		confpass = str(self.confirmpass_field.get())
		self.initbal = str(self.initbal_field.get())
		creditnum = str(self.creditnum_field.get())
		self.authentic_num = str(self.authentic_field.get())
		if self.username=='' or self.password=='' or confpass=='' or self.initbal=='' or creditnum==''or self.authentic_num=='':
			messagebox.showerror('Error', 'All fields are required\nSemua kolom diperlukan', parent=self.root)
			return False
		elif self.availableUser()==True:
			print(self.availableUser())
			messagebox.showerror('Error', 'Username had already used by other user\n\nUsername telah digunakan oleh pengguna'\
								'lain', parent=self.root)
			return False
		elif self.password != confpass:
			messagebox.showerror('Error', 'Password isn\'t valid\n\nPassword tidak valid')
			return False
		else:
			return True

	def authentication(self):
		verify_num = 12345
		number = int(self.authentic_num)
		if number==verify_num:
			return True
		else:
			messagebox.showerror('Error', 'Authentication number isn\'t valid\n\nNomor autentikasi tidak valid', parent=self.root)
			return False

	def register(self):
		username=self.username
		password=self.password
		amount=self.initbal
		registerQuery = "INSERT INTO `users` (`username`, `password`) VALUES ('"+username+"', '"+password+"')"
		initbalQuery = "INSERT INTO `balances` (`username`, `amount`) VALUES ('"+username+"', '"+amount+"')"
		try:
			self.cursor.execute(registerQuery)
			self.connection.commit()
			try:
				self.cursor.execute(initbalQuery)
				self.connection.commit()
				return True
			except Exception as ex:
				messagebox.showerror('Error', str(e), parent=self.root)
		except Exception as e:
			messagebox.showerror('Error', str(e), parent=self.root)
			return False

	def registerFlow(self):
		try:
			if self.formCheck() == True:
				if self.authentication() == True:
					if self.register() == True:
						messagebox.showinfo('Information', 'Register success!\n\nPendaftaran berhasil!')
						self.cleanField(self.username_field, self.password_field, self.confirmpass_field, self.initbal_field,\
										self.creditnum_field, self.authentic_field)
		except Exception as e:
			messagebox.showerror('Error', str(e), parent=self.root)

	def initUI(self):
		main_window = Frame(self.root, bg='#81baff')
		main_window.place(relwidth=1, relheight=1, relx=0, rely=0)
		logo = Label(main_window, image=self.image_src, bg='#81baff', cursor='hand2')
		logo.place(relwidth=1, relheight=0.2, relx=0, rely=0)
		logo.bind("<Button-1>", lambda e: self.goToLogin())
		#form frame
		form_frame = Frame(main_window, bg='#002955')
		form_frame.place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.2)
		##Links
		help_link = Label(root, text='Help', bg='#81baff', fg='#000000', cursor='hand2', font='Arial 16')
		help_link.place(relwidth=0.1, relheight=0.05, relx=0.8, rely=0.15)
		help_link.bind("<Button-1>", lambda e: self.callHelp())
		login_link = Label(root, text='Login', bg='#81baff', fg='#ac0000', cursor='hand2', font='Arial 16')
		login_link.place(relwidth=0.1, relheight=0.05, relx=0.9, rely=0.025)
		login_link.bind("<Button-1>", lambda e: self.goToLogin())
		##Fields
		####Right side
		username_label = Label(form_frame, text='Username', bg='#81baff', fg='#00003b', font='Arial 20')
		username_label.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.1)
		self.username_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='left')
		self.username_field.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.175)
		password_label = Label(form_frame, text='Password', bg='#81baff', fg='#00003b', font='Arial 20')
		password_label.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.3)
		self.password_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='left')
		self.password_field.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.375)
		self.password_field.config(show='*')
		confirmpass_label = Label(form_frame, text='Confirm Password', bg='#81baff', fg='#00003b', font='Arial 20')
		confirmpass_label.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.5)
		self.confirmpass_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='left')
		self.confirmpass_field.place(relwidth=0.425, relheight=0.075, relx=0.05, rely=0.575)
		self.confirmpass_field.config(show='*')
		###Left side
		initbal_label = Label(form_frame, text='Init Balances', bg='#81baff', fg='#00003b', font='Arial 20')
		initbal_label.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.1)
		self.initbal_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.initbal_field.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.175)
		creditnum_label = Label(form_frame, text='Credit Card Number', bg='#81baff', fg='#00003b', font='Arial 20')
		creditnum_label.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.3)
		self.creditnum_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.creditnum_field.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.375)
		authentic_label = Label(form_frame, text='Authentication Number', bg='#81baff', fg='#00003b', font='Arial 20')
		authentic_label.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.5)
		self.authentic_field = Entry(form_frame, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.authentic_field.place(relwidth=0.425, relheight=0.075, relx=0.525, rely=0.575)
		self.authentic_field.config(show='#')

		submit = Button(form_frame, text='Submit', bg='#ac0000', fg='#ffffff', font='Arial 20', cursor='hand2',\
						command=self.registerFlow)
		submit.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.8)



root = Tk()
main = SignUp(root)
root.mainloop()
		
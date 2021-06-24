'''
	File    : main.py
	Project : Kuzu Bank App
	Author  : Karta Kusuma
	Version : 1.0.0
'''

from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import mysql.connector as mysql
import speech_recognition as sr
import cv2
import os

class Main:
	def __init__(self, root):
		self.root = root
		width = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.title('KuzuBank')
		self.root.geometry(f'{width}x{height}+0+0')
		self.root.iconbitmap('logo/kuzubank-logo.ico')
		self.connection = mysql.connect(host='localhost', user='root', password='12345', database='kuzubank')
		self.cursor = self.connection.cursor()
		self.cursor.execute("SELECT `user_id` FROM `activeuser`")
		activeUser = self.cursor.fetchone()	#take user_id value from activeuser in userkuzubank database 
		print(activeUser)
		self.user_active = str(activeUser[0])
		#print(self.user_active) #for debuging
		self.user_active = ''.join(self.user_active)
		self.currDate = datetime.now()
		self.initUI()
		self.showFrame(self.window_menu)

	def showFrame(self, frame):
		frame.tkraise()

	def camera(self, action):
		baser_dir = os.getcwd()
		#print(str(baser_dir)) #for debuging
		user = str(self.user_active)
		prefix = str(action)
		extension = 'jpg'
		add_path= 'images\\'
		file_format = "{:s}{:s}-{:s}-{:%Y%m%d_%H%M%S}.{:s}"
		date = datetime.now()
		filename = file_format.format(add_path, user, prefix, date, extension)
		#print(filename) #for debuging
		file_path = os.path.normpath(os.path.join(baser_dir, filename))
		#print(file_path) #for debuging
		self.camStatus = False
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		font = cv2.FONT_HERSHEY_SIMPLEX
		text = "Press 'q' for take a picture (Tekan 'q' untuk mengambil gambar)"

		try:
			cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
			while True:
				_, image = cam.read()
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				face_detect = face_cascade.detectMultiScale(gray, 1.1, 4)
				for x,y,w,h in face_detect:
					cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)
					cv2.putText(image, text, (20,50), font, 0.5, (0,255,0), 1, cv2.LINE_AA)
				cv2.imshow('Camera', image)
				key = cv2.waitKey(30)
				if key==ord('q'):
					try:
						cv2.imwrite(file_path, image)
						self.camStatus = True
						print('Success')
					except Exception as ex:
						messagebox.showerror('Error', str(ex), parent=self.root)
					break
			cam.release()
			cv2.destroyAllWindows()
		except Exception as e:
			print(e)

	def balanceCount(self):
		user_id = self.user_active
		getUserQuery="SELECT `username` FROM `users` WHERE `user_id`='"+str(user_id)+"'"
		self.cursor.execute(getUserQuery)
		username = self.cursor.fetchone()
		username = ''.join(str(username[0]))
		balQuery = "SELECT `amount` FROM `balances` WHERE `username`='"+str(username)+"'"
		#print(balQuery) #for debuging
		try:
			self.cursor.execute(balQuery)
			balance = self.cursor.fetchone()
			balance = balance[0]
			balance = str(balance)
			#print(balance) #for debuging
		except Exception as e:
			messagebox.showerror('Error', str(e), parent=self.root)
		return balance

	def showBalanceFrame(self):
		getBalance = self.balanceCount()
		balance_res = Label(self.balance_act, text=getBalance, bg='#002955', fg='#ffffff', font='Arial 45')
		balance_res.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.5)
		self.showFrame(self.window_balance)

	def updateBalance(self, change):
		user = self.user_active
		change = int(change)
		init = self.balanceCount()
		init = int(init)
		if change < 0:
			messagebox.showerror('Error', 'Invalid amount!\n\nNominal tidak valid!', parent=self.root)
			self.transaction_status= False
		elif init <= 0:
			messagebox.showerror('Error', 'Can\'t process this action. Your balances isn\'t enough'\
								'\n\nTidak dapat memroses tindakan ini. Saldo Anda tidak mencukupi', parent=self.root)
			self.transaction_status= False
		else:
			final = init - change
			final = int(final)
			if final < 0:
				messagebox.showerror('Error', 'Your balances are not enough to do this action'
									'\n\nSaldo Anda tidak cukup untuk tindakan ini', parent=self.root)
				self.transaction_status= False
			else:
				try:
					#final = str(final)
					balUpQuery = "UPDATE `balances` SET `amount`='"+str(final)+"' WHERE `user_id`='"+str(user)+"'"
					self.cursor.execute(balUpQuery)
					self.connection.commit()					
					self.transaction_status= True
				except Exception as e:
					messagebox.showerror('Error', str(e), parent=self.root)
					self.transaction_status= False
					#print(e) #for debuging

	def cleanField(self, field1, field2):
		field1.delete(0, END)
		field2.delete(0, END)

	def commitPayment(self):
		number = ''.join(str(self.payment_num.get()))
		amount = ''.join(str(self.amount_num.get()))
		if number=='' or amount=='':
			messagebox.showerror('Error', 'All fields are required\nSemua kolom diperlukan', parent=self.root)
		else:
			user = self.user_active
			#print(user) #for debuging
			payQuery=("('"+str(user)+"', '"+str(self.currDate)+"x"+str(number)+"x"+str(amount)+"')")
			#print(payQuery) #for debuging
			sqlQuery = "INSERT INTO `payment` (`user_id`, `action`) VALUES "+str(payQuery)
			#print(sqlQuery) #for debuging
			hasil = messagebox.askyesno('Confirmation', 'Pleas take a picture to confirm this action'\
										'\n\nSilakan ambil gambar untuk mengonfirmasi tindakan ini', parent=self.root)
			if hasil == True:
				try:
					self.camera('payment')
					if self.camStatus == True:			
						try:
							self.cursor.execute(sqlQuery)
							self.connection.commit()
							self.updateBalance(amount)
							if self.transaction_status == True:
								messagebox.showinfo('Information', 'Transaction success\n\nTransaksi berhasil', parent=self.root)
								self.cleanField(self.payment_num, self.amount_num)
							else:
								messagebox.showerror('Error', 'Transaction failed\n\nTransaksi gagal', parent=self.root)
						except Exception as e:
							print(e)
							messagebox.showerror('Error', str(e), parent=self.root)
				except Exception as ex:
					messagebox.showerror('Error', str(ex), parent=self.root)
			else:
				messagebox.showerror('Error','Can\'t accomplish this action\n\nTidak dapat menyelesaikan tindakan ini',\
									parent=self.root)

	def commitTransfer(self):
		number = ''.join(str(self.dest_num.get()))
		amount = ''.join(str(self.nominal_num.get()))
		if number=='' or amount=='':
			messagebox.showerror('Error', 'All fields are required\nSemua kolom diperlukan', parent=self.root)
		else:
			user = self.user_active
			#print(user) #for debuging
			tfQuery=("('"+str(user)+"', '"+str(self.currDate)+"x"+str(number)+"x"+str(amount)+"')")
			#print(tfQuery) #for debuging
			sqlQuery = "INSERT INTO `transfer` (`user_id`, `action`) VALUES "+str(tfQuery)
			#print(sqlQuery) #for debuging
			hasil = messagebox.askyesno('Confirmation', 'Pleas take a picture to confirm this action\n\n'\
										'Silakan ambil gambar untuk mengonfirmasi tindakan ini', parent=self.root)
			if hasil == True:
				try:
					self.camera('transfer')
					if self.camStatus == True:
						try:
							self.cursor.execute(sqlQuery)
							self.connection.commit()
							self.updateBalance(amount)
							if self.transaction_status == True:
								messagebox.showinfo('Information', 'Transaction success\n\nTransaksi berhasil', parent=self.root)
								self.cleanField(self.dest_num, self.nominal_num)
							else:
								messagebox.showerror('Error', 'Transaction failed\n\nTransaksi gagal', parent=self.root)
						except Exception as e:
							print(e)
							messagebox.showerror('Error', str(e), parent=self.root)
				except Exception as ex:
					messagebox.showerror('Error', str(e), parent=self.root)
			else:
				messagebox.showerror('Can\'t accomplish this action\n\nTidak dapat menyelesaikan tindakan ini', parent=self.root)

	def listen(self):
		recognizer = sr.Recognizer()
		self.data = ''

		with sr.Microphone() as source:
			print("Log:")
			print("Adjusting noise ")
			recognizer.adjust_for_ambient_noise(source, duration=1)
			print("Recording for 4 seconds")
			recorded_audio = recognizer.listen(source, timeout=4)
			print("Done recording")

		try:
			print("Recognizing the text")
			text = recognizer.recognize_google(recorded_audio, language="en-US")
			self.data = text
			print("Decoded Text : {}".format(text))
		except Exception as ex:
			print(ex)

		if self.data == 'balance' or self.data == 'balances':
			print('open balance')
			self.showBalanceFrame()
		elif self.data == 'transfer' or self.data == 'transfers':
			print('open transfer')
			self.showFrame(self.window_transfer)
		elif self.data == 'payment' or self.data == 'payment':
			print('open payment')
			self.showFrame(self.window_payment)

	def exit(self):
		self.root.quit()

	def initUI(self):
		self.window_menu = Frame(self.root, bg='#81baff')
		self.window_balance = Frame(self.root, bg='#81baff')
		self.window_payment = Frame(self.root, bg='#81baff')
		self.window_transfer = Frame(self.root, bg='#81baff')

		#logo
		self.image_src = ImageTk.PhotoImage(Image.open('logo/kuzu-big-new-small.png'))

		#loop for multiframe
		for frame in (self.window_menu, self.window_balance, self.window_payment, self.window_transfer):
			frame.place(relwidth=1, relheight=1, relx=0, rely=0)

		#Menu Window
		##frame
		frame_speech = Frame(self.window_menu, bg='#002955')
		frame_speech.place(relwidth=0.7, relheight=0.65, relx=0.05, rely=0.2)
		##logo
		logo = Label(self.window_menu, image=self.image_src, bg='#81baff')
		logo.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
		##title
		title_menu = Label(self.window_menu, text='Menu', bg='#002955', fg='#ffffff', font='Arial 40')
		title_menu.place(relwidth=0.25, relheight=0.075, relx=0, rely=0)
		label_speech = Label(frame_speech, text='Smart Assistant', fg='#ffffff', bg='#002955', font='Arial 40')
		label_speech.place(relwidth=1, relheight=0.2, relx=0, rely=0.1)
		button_speech = Button(frame_speech, text='Speak', fg='#ffffff', bg='#ac0000', font='Arial 40', cursor='hand2',\
							command=self.listen)
		button_speech.place(relwidth=0.3, relheight=0.5, relx=0.35, rely=0.35)
		##buttons
		button_logout = Button(self.window_menu, text='Logout', bg='#ac0000', fg='#ffffff', font='Arial 20',\
							cursor='hand2', command=self.exit)
		button_logout.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.2)
		button_balance = Button(self.window_menu, text='Balances', bg='#003a00', fg='#ffffff', font='Arial 20',\
							cursor='hand2', command=self.showBalanceFrame) #lambda: self.showFrame(self.window_balance))
		button_balance.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.325)
		button_payment = Button(self.window_menu, text='Payment', bg='#003a00', fg='#ffffff', font='Arial 20',\
							cursor='hand2', command=lambda: self.showFrame(self.window_payment))
		button_payment.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.45)
		button_transfer = Button(self.window_menu, text='Transfer', bg='#003a00', fg='#ffffff', font='Arial 20',\
							cursor='hand2', command=lambda: self.showFrame(self.window_transfer))
		button_transfer.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.575)

		#Balances Window
		##Frame
		self.balance_act = Frame(self.window_balance, bg='#002955')
		self.balance_act.place(relwidth=0.7, relheight=0.65, relx=0.05, rely=0.2)
		##logo
		logo = Label(self.window_balance, image=self.image_src, bg='#81baff')
		logo.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
		##title
		title_balance = Label(self.window_balance, text='Balances', bg='#002955', fg='#ffffff', font='Arial 40')
		title_balance.place(relwidth=0.25, relheight=0.075, relx=0, rely=0)
		balance_lbl = Label(self.balance_act, text='Your balances:', bg='#002955', fg='#ffffff', font='Arial 45')
		balance_lbl.place(relwidth=0.8, relheight=0.1, relx=0.1, rely=0.35)
		button_menu = Button(self.window_balance, text='Menu', bg='#003a00', fg='#ffffff', font='Arial 20', cursor='hand2',\
							command=lambda: self.showFrame(self.window_menu))
		button_menu.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.2)

		#Payment Window
		##Frame
		payment_act = Frame(self.window_payment, bg='#002955')
		payment_act.place(relwidth=0.7, relheight=0.65, relx=0.05, rely=0.2)
		##logo
		logo = Label(self.window_payment, image=self.image_src, bg='#81baff')
		logo.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
		##title
		title_payment = Label(self.window_payment, text='Payment', bg='#002955', fg='#ffffff', font='Arial 40')
		title_payment.place(relwidth=0.25, relheight=0.075, relx=0, rely=0)
		label_paynumber = Label(payment_act, text='Payment Number', bg='#81baff', fg='#00003b', font='Arial 20')
		label_paynumber.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.15)
		self.payment_num = Entry(payment_act, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.payment_num.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.225)
		label_amount = Label(payment_act, text='Amount', bg='#81baff', fg='#00003b', font='Arial 20')
		label_amount.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.4)
		self.amount_num = Entry(payment_act, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.amount_num.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.475)
		#buttons
		button_commit = Button(payment_act, text='Commit', bg='#ac0000', fg='#ffffff', font='Arial 20', cursor='hand2',\
							command=self.commitPayment)
		button_commit.place(relwidth=0.15, relheight=0.1, relx=0.75, rely=0.8)
		button_menu = Button(self.window_payment, text='Menu', bg='#003a00', fg='#ffffff', font='Arial 20', cursor='hand2',\
							command=lambda: self.showFrame(self.window_menu))
		button_menu.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.2)

		#Transfer Window
		##Frame
		transfer_act = Frame(self.window_transfer, bg='#002955')
		transfer_act.place(relwidth=0.7, relheight=0.65, relx=0.05, rely=0.2)
		##logo
		logo = Label(self.window_transfer, image=self.image_src, bg='#81baff')
		logo.place(relwidth=0.25, relheight=0.1, relx=0.75, rely=0)
		##title
		title_transfer = Label(self.window_transfer, text='Transfer', bg='#002955', fg='#ffffff', font='Arial 40')
		title_transfer.place(relwidth=0.25, relheight=0.075, relx=0, rely=0)
		label_dest = Label(transfer_act, text='Destination Number', bg='#81baff', fg='#00003b', font='Arial 20')
		label_dest.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.15)
		self.dest_num = Entry(transfer_act, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.dest_num.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.225)
		label_nominal = Label(transfer_act, text='Amount', bg='#81baff', fg='#00003b', font='Arial 20')
		label_nominal.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.4)
		self.nominal_num = Entry(transfer_act, bg='#cacaca', fg='#000000', font='Arial 20', justify='right')
		self.nominal_num.place(relwidth=0.8, relheight=0.075, relx=0.1, rely=0.475)
		##buttons
		button_commit = Button(transfer_act, text='Commit', bg='#ac0000', fg='#ffffff', font='Arial 20', cursor='hand2',\
							command=self.commitTransfer)
		button_commit.place(relwidth=0.15, relheight=0.1, relx=0.75, rely=0.8)
		button_menu = Button(self.window_transfer, text='Menu', bg='#003a00', fg='#ffffff', font='Arial 20', cursor='hand2',\
							command=lambda: self.showFrame(self.window_menu))
		button_menu.place(relwidth=0.15, relheight=0.1, relx=0.8, rely=0.2)


root = Tk()
main = Main(root)
root.mainloop()
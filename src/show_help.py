'''
	File	: show_help.py
	Project	: Kuzu Bank App
	Author	: Karta Kusuma
	Version	: 1.0.0
'''

from tkinter import *
from PIL import ImageTk, Image


class Help:
	def __init__(self, root):
		self.root = root
		width  = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.title('Help')
		self.root.geometry(f'{width}x{height}+0+0')
		self.root.iconbitmap('logo/kuzubank-logo.ico')
		self.initUI()

	def initUI(self):
		frame = Frame(self.root, bg='#81baff')
		frame.place(relwidth=1, relheight=1, relx=0, rely=0)
		help_label = Label(frame, text='Help', bg='#81baff', fg='#000000', font='Arial 50')
		help_label.place(relwidth=1, relheight=0.15, relx=0, rely=0)
		label1 = Label(frame, text='Username\n\tKolom ini digunakan untuk membuat username yang akan Anda gunakan',\
						bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label1.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.15)
		label2 = Label(frame, text='Pasword\n\tKolom ini digunakan untuk membuat password yang akan Anda gunakan',\
						bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label2.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.25)
		label3 = Label(frame, text='Confirm Password\n\tKolom ini digunakan untuk mengonfirmasi password'\
						' yang Anda daftarkan', bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label3.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.35)
		label4 = Label(frame, text='Init Balance\n\tKolom ini digunakan untuk menginisialisasi saldo (balances)'\
						' yang Anda inginkan', bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label4.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.45)
		label5 = Label(frame, text='Credit Card Number\n\tKolom ini digunakan untuk memasukkan nomor kartu kredit'\
						' untuk mengirimkan tagihan saldo awal Anda',\
						bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label5.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.55)
		label6 = Label(frame, text='Authentication Number\n\tKolom ini digunakan untuk memasukkan nomor autentikasi'\
						' dari Customer Service', bg='#81baff', fg='#000000', font='Arial 18',\
						justify='left', anchor='w')
		label6.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.65)
		label7 = Label(frame, text='Submit\n\tTombol ini digunakan untuk memeriksa keautentikan data'\
						' serta mendaftarkan akun Anda', bg='#81baff', fg='#000000', font='Arial 18', justify='left', anchor='w')
		label7.place(relwidth=0.9, relheight=0.1, relx=0.05, rely=0.75)


root = Tk()
main = Help(root)
root.mainloop()
#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
	# Python2
	from Tkinter import *
except ImportError:
	# Python3
	from tkinter import *
	from tkinter.ttk import Checkbutton
	from tkinter import messagebox
	import tkinter as tkk
	import random
	import paramiko
	import base64

##===	ssh_connect		===##
def ssh_connect(ssh_send):	#code#
	def decode_d(d_code):
		result_d = base64.b64decode(d_code).decode('utf-8')
		return result_d #возврат результата в функцию
	host = decode_d('MTEuMTEuMTEuMTI4')
	user = decode_d('ZGVta2lua3Y=')
	psw = decode_d('MTIzcXdlMTIzNA==')
	port = decode_d('MjIxMQ==')
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=host, port=port, username=user, password=psw) # Подключение
	stdin, stdout, stderr = ssh.exec_command(ssh_send) # Выполнение команды
	result = stdout.read() + stderr.read() #result = stdout.read().splitlines()	# Читаем результат так:
	ssh.close()
	return result #возврат результата в функцию
##===	Конец ssh_connect	===##

##===	Reset_settins	===##
def reset_set():			#code#
	result_pr=ssh_connect('ip a')	#вызов функции ssh_connect = внесение результат выполнения функции в переменную result_pr
	##окно перезаписи настроек##
	window_reset_set= tkk.Toplevel()
	window_reset_set.title("Чтение новых настроек")

	# конфигурируем упаковщик, чтобы текстовый виджет расширялся
	window_reset_set.grid_rowconfigure(0, weight=1)
	window_reset_set.grid_columnconfigure(0, weight=1)

	frame3_reset_set = Frame(window_reset_set,bg='green',bd=5)
	frame3_reset_set.grid(row=0, column=0, sticky='nsew')
	# конфигурируем упаковщик, чтобы текстовый виджет расширялся
	frame3_reset_set.rowconfigure(0, weight=1)
	frame3_reset_set.columnconfigure(0, weight=1)


	text3_1=Text(frame3_reset_set,font='Arial 14',wrap=WORD)
	text3_1.grid(row=0,column=0)
	text3_1.grid_columnconfigure(0, weight=1)
	text3_1.config(state=NORMAL)
	text3_1.insert(INSERT, result_pr)
	text3_1.config(state=DISABLED)
	
	
	#=====Scrollbar=====#
	sy3_1 = Scrollbar(frame3_reset_set, orient=VERTICAL, command=text3_1.yview, bg='black')
	sy3_1.grid(row=0, column=1, sticky=N+S)
	text3_1['yscrollcommand'] = sy3_1.set
##===	КонецRst_settins	===##

##===	exitRoot		===##
def exitRoot():			#code#
	root.destroy()
##===	КонецexitRoot	===##

##===	gnrt_passw		===##
def generate_passw_window():	#code#
	table_row2_1 = IntVar()
	##кнопка генерации паролей##
	def generate_passwd():

		Big = 'QWERTYUIOPASDFGHJKLZXCVBNM'
		Low = 'qwertyuiopasdfghjklzxcvbnm'
		Num = '1234567890'
		Spe = '!@#$%^&*()'

		BI = chk_state2_3.get()	# Пароль должен содержать символы в верхнем регистре (True - да | False - нет)
		LO = chk_state2_2.get()	# Пароль должен содержать символы в нижнем регистре (True - да | False - нет)
		NU = chk_state2_1.get()	# Пароль должен содержать цифры (True - да | False - нет)
		PS = chk_state2_4.get()	# Пароль должен содержать спец символы (True - да | False - нет)
		Password_len = table_row2_1.get()
#		Password_len = input('Длина пароля: ')

		if Password_len:
			if Password_len.isdigit() == True:
				Password_len = int(Password_len)
			else:
				print('Выход... Значение должно быть цифровое...')
				exit(0)
		else:
			print('Выход... Не указана Длина пароля...')
			exit(0)

		Pass_Symbol = []
		if BI == True:
			ass_Symbol.extend(list(Big))
		if LO == True:
			Pass_Symbol.extend(list(Low))
		if NU == True:
			Pass_Symbol.extend(list(Num))
		if PS == True:
			Pass_Symbol.extend(list(Spe))

		random.shuffle(Pass_Symbol)
		psw = []
		psw.append(''.join([random.choice(Pass_Symbol) for x in range(Password_len)]))
		#file_Pass = open('Password.txt', 'w')
		#file_Pass.write('\n'.join(psw))
		#file_Pass.close()

		pass_w = ('\n'.join(psw))
		txt2_2.delete(0, END)
		txt2_2.insert(INSERT, pass_w)
		root.clipboard_clear()
		root.clipboard_append(pass_w)

	window_passw = tkk.Toplevel()
	window_passw.title("Генерация паролей")
	#=====frame2_gpass=====#
	frame2_gpass=Frame(window_passw,bg='black',bd=5)
	frame2_gpass.grid(row=0, column=0, sticky='nsew')
	#=====frame2_gpass=====#
	#=====Checkbutton=====#
	chk_state2_1 = BooleanVar()
	chk_state2_1.set(True)  # задайте проверку состояния чекбокса !цифры
	chk2_1 = Checkbutton(frame2_gpass, text='0-9', var=chk_state2_1)
	chk_state2_2 = BooleanVar()
	chk_state2_2.set(True)  # задайте проверку состояния чекбокса !маленькие
	chk2_2 = Checkbutton(frame2_gpass, text='a-z', var=chk_state2_2)
	chk_state2_3 = BooleanVar()
	chk_state2_3.set(True)  # задайте проверку состояния чекбокса !большие
	chk2_3 = Checkbutton(frame2_gpass, text='A-Z', var=chk_state2_3)
	chk_state2_4 = BooleanVar()
	chk_state2_4.set(True)  # задайте проверку состояния чекбокса !спецсимволы
	chk2_4 = Checkbutton(frame2_gpass, text='#-$', var=chk_state2_4)
	lbl2_1 = Label(frame2_gpass, text="Длина пароля")
	lbl2_1.grid(row=0,column=0, sticky='nsew')
	chk2_1.grid(row=1, column=0, sticky='nsew')
	chk2_2.grid(row=2, column=0, sticky='nsew')
	chk2_3.grid(row=3, column=0, sticky='nsew')
	chk2_4.grid(row=4, column=0, sticky='nsew')
	txt2_2 = Entry(frame2_gpass,width=10)
	txt2_2.grid(row=5,column=0, columnspan=3, sticky='nsew')
	table_row2_1 = Spinbox(frame2_gpass, fg="blue", font=12, from_=4, to=10)
	table_row2_1.grid(row=0, column=1)
	button2_1=Button(frame2_gpass,text='Генерировать', command=generate_passwd)
	button2_1.grid(row=1,column=1, rowspan=3, sticky='nsew')
##===	gnrt_passw		===##

#=====def=====#
root=Tk()
root.title("Asterisk3")
root.geometry('400x350')
mainmenu = Menu(root)
root.config(menu=mainmenu)

#=====frame1_conn=====#
frame1_conn=Frame(root,bg='green',bd=5)
frame1_conn.grid(row=0, column=0, sticky='nsew')

#=====label=====#
lbl1_1 = Label(frame1_conn, text="Имя сервера")
lbl1_1.grid(row=0,column=0, sticky='nsew')
lbl1_2 = Label(frame1_conn, text="Имя пользователя")
lbl1_2.grid(row=1,column=0, sticky='nsew')
lbl1_3 = Label(frame1_conn, text="Пароль")
lbl1_3.grid(row=2,column=0, sticky='nsew')
#=====Button=====#
button1_1=Button(frame1_conn,text='Подключиться')
button1_1.grid(row=3,column=0, columnspan=2, sticky='nsew')
txt1_1 = Entry(frame1_conn,width=10)
txt1_1.grid(row=0,column=1, sticky='w')
txt1_2 = Entry(frame1_conn,width=10)
txt1_2.grid(row=1,column=1, sticky='w')
txt1_3 = Entry(frame1_conn,width=10)
txt1_3.grid(row=2,column=1, sticky='w')

#=====Menu=====#
filemenu = Menu(mainmenu, tearoff=0)
resetmenu = Menu(mainmenu, tearoff=0)
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu2 = Menu(helpmenu, tearoff=0)

filemenu.add_command(label="Открыть...")

filemenu.add_cascade(label="Перезагрузка", menu=resetmenu)
resetmenu.add_command(label="настроек", command=reset_set)

filemenu.add_command(label="Генерация паролей", command=generate_passw_window)
filemenu.add_command(label="Выход", command=exitRoot)

helpmenu.add_cascade(label="Помощь", menu=helpmenu2)
helpmenu2.add_command(label="Локальная справка")
helpmenu2.add_command(label="На сайте")

helpmenu.add_separator()
helpmenu.add_command(label="О программе")

mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

root.mainloop()

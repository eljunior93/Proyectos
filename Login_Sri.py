from email.mime import image
import glob
import os
from tkinter import Menu, StringVar, Tk, messagebox, ttk, Label, Button, Frame, Entry, filedialog, ttk, Scrollbar, VERTICAL, HORIZONTAL, PhotoImage
import math
import tkinter
import time
from tracemalloc import start
from turtle import bgcolor, color
from tkinter.font import Font
import comprobante_sri_download
#import from_ssl_import_Options
from urllib.request import urlretrieve, urlcleanup
import pandas as pd
import xlsxwriter
import pyodbc
import sqlite3
from datetime import date, time, datetime
from tkinter import * 

def conectar():
    direccion_servidor = ''
    nombre_bd = ''
    nombre_bd_main=''
    nombre_usuario = ''
    password = ''

    miConexion=sqlite3.connect("base2")
    miCursor=miConexion.cursor()
    try:
        miCursor.execute("SELECT * FROM PARAMETROS WHERE ESTATUS = 'A'")
        for row in miCursor:
            print(row)
            direccion_servidor = row[1]
            nombre_bd = row[2]
            nombre_bd_main = row[3]
            nombre_usuario = row[4]
            password = row[5]
        miConexion.commit()
    except Exception as e:
        print(e)
        pass

    try:

        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
        print("OK! conexión exitosa")
    except Exception as e:
        print("Ocurrió un error al conectar a SQL Server: ", e)

login = Tk()
df = []
login.title('Iniciar Sesion')
login.geometry('462x450')
login.iconbitmap('D:\SriTkinter\logoia.ico')
login.configure(bg="#fff")
login.resizable(False,False)
seleccion = StringVar()

def salirAplicacion():
	valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		login.destroy()

def ventanaComprobante():
    dt = datetime.now()
    vent = tkinter.Tk()
    vent.title("Descargar Comprobantes SRI")
    vent.resizable(False,False)
    vent.geometry("1150x900")
    vent.iconbitmap('D:\SriTkinter\logoia.ico')
    vent.configure(bg='white')
    step = tkinter.DoubleVar()
    step.set(0)

    frame_datos=Frame(vent,width=1140,height=190,bg='white')
    frame_datos.place(x=5,y=5)

    img3 = PhotoImage(file = "D:\\SriTkinter\\LOGO-ISHIDA32.png")
    Label(vent,image=img3).place(x=375,y=15,width=400,height=75)

    def on_enter(e):
        txtRuc.delete(0, 'end')

    def on_leave(e):
        name=txtRuc.get() 
        if name=='':
            txtRuc.insert(0,'Ruc')

    txtRuc = Entry(frame_datos, width=25,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    txtRuc.place(x=25,y=100)
    txtRuc.insert(0,'Ruc')
    txtRuc.bind('<FocusIn>', on_enter)
    txtRuc.bind('<FocusOut>', on_leave)

    Frame(frame_datos,width=150,height=2,bg='gray').place(x=25,y=122)

    def on_enter(e):
        txtClave.delete(0, 'end')

    def on_leave(e):
        name=txtClave.get() 
        if name=='':
            txtRuc.insert(0,'Clave')

    txtClave = Entry(frame_datos, width=25,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    txtClave.place(x=25,y=150)
    txtClave.insert(0,'Clave')
    txtClave.bind('<FocusIn>', on_enter)
    txtClave.bind('<FocusOut>', on_leave)

    Frame(frame_datos,width=150,height=2,bg='gray').place(x=25,y=172)

    comboYear = ttk.Combobox(frame_datos)
    comboYear["values"] = ("2022", "2021", "2020")
    comboYear.place(x=300,y=100)
    comboYear.insert(0, dt.year)
    lbl1 = Entry(frame_datos, width=5,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    lbl1.place(x=250,y=100)
    lbl1.insert(0, 'Año')

    comboMes = ttk.Combobox(frame_datos)
    comboMes["values"] = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    comboMes.place(x=525,y=100)
    comboMes.insert(0, dt.month)
    lbl2 = Entry(frame_datos, width=5,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    lbl2.place(x=475,y=100)
    lbl2.insert(0, 'Mes')

    comboDia = ttk.Combobox(frame_datos)
    comboDia["values"] = ("Todos", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
    comboDia.place(x=750,y=100)
    comboDia.insert(0, dt.day)
    lbl3 = Entry(frame_datos, width=5,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    lbl3.place(x=700,y=100)
    lbl3.insert(0, 'Dia')

    comboTipo = ttk.Combobox(frame_datos)
    comboTipo["values"] = ("Todos", "Factura", "Liquidación de compra de bienes y prestación de servicios", "Notas de Crédito", "Notas de Débito", "Comprobante de Retención")
    comboTipo.place(x=300,y=150,width=590)
    comboTipo.insert(0, 'Todos')
    lbl4 = Entry(frame_datos, width=5,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
    lbl4.place(x=250,y=150)
    lbl4.insert(0, 'Tipo')

    def carga_aut():
        path_download = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads','*.txt')
        list_of_files = glob.glob(path_download) 
        latest_file = max(list_of_files, key=os.path.getctime)
        indica['text'] = latest_file

    def start_progbar():
        ruc = txtRuc.get()
        clave = txtClave.get()
        Anio = comboYear.get()
        Mes = comboMes.get()
        Dia = comboDia.get()
        Tipo = comboTipo.get()
        comprobante_sri_download.resolver(ruc, clave, Anio, Mes, Dia, Tipo)
        carga_aut()
        datos_txt() 
    
    Button(frame_datos,width=20,pady=7,text='Descargar Comprobante',bg='red',fg='white',border=0,command=start_progbar).place(x=950,y=115)

    vent.columnconfigure(0, weight = 25)
    vent.rowconfigure(0, weight= 25)
    vent.columnconfigure(0, weight = 1)
    vent.rowconfigure(1, weight= 1)

    frame1 = Frame(vent, bg='white')
    frame1.grid(column=0,row=0,sticky='nsew')
    frame2 = Frame(vent, bg='white')
    frame2.grid(column=0,row=1,sticky='nsew')
    frame1.place(x=0,y=200,width=1150, height=450)
    frame2.place(x=0,y=655,width=1150, height=50)

    frame1.columnconfigure(0, weight = 1)
    frame1.rowconfigure(0, weight= 1)

    frame2.columnconfigure(0, weight = 1)
    frame2.rowconfigure(0, weight= 1)
    frame2.columnconfigure(1, weight = 1)
    frame2.rowconfigure(0, weight= 1)

    frame2.columnconfigure(2, weight = 1)
    frame2.rowconfigure(0, weight= 1)

    frame2.columnconfigure(3, weight = 2)
    frame2.rowconfigure(0, weight= 1)

    tabla = ttk.Treeview(frame1 , height=10)
    tabla.grid(column=0, row=0, sticky='nsew')

    ladox = Scrollbar(frame1, orient = HORIZONTAL, command= tabla.xview)
    ladox.grid(column=0, row = 1, sticky='ew') 

    ladoy = Scrollbar(frame1, orient =VERTICAL, command = tabla.yview)
    ladoy.grid(column = 1, row = 0, sticky='ns')

    tabla.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)

    estilo = ttk.Style(frame1)
    estilo.theme_use('clam') 
    estilo.configure(".",font= ('Arial', 14), foreground='black')
    estilo.configure("Treeview", font= ('Helvetica', 12), foreground='black',  background='white')
    estilo.map('Treeview',background=[('selected', 'green2')], foreground=[('selected','black')] )

    def abrir_archivo():

        archivo = filedialog.askopenfilename(initialdir ='/', 
                                                title='Selecione archivo', 
                                                filetype=(('txt files', '*.txt*'),('All files', '*.*')))
        indica['text'] = archivo

    def datos_txt():
        datos_obtenidos = indica['text']
        archivotxt = r'{}'.format(datos_obtenidos)
        df = pd.read_csv(archivotxt, usecols = ['COMPROBANTE', 'SERIE_COMPROBANTE', 'RUC_EMISOR', 'RAZON_SOCIAL_EMISOR', 'FECHA_EMISION', 'FECHA_AUTORIZACION', 'TIPO_EMISION', 'NUMERO_AUTORIZACION'], sep='\t', encoding='latin-1', on_bad_lines='skip')
        
        df_final = df.dropna(how='all')

        Limpiar()
        tabla['column'] = list(df_final.columns)
        tabla['show'] = "headings"  
        

        for columna in tabla['column']:
            tabla.heading(columna, text= columna)


        df_fila = df_final.to_numpy().tolist()
        for fila in df_fila:
            if math.isnan(float(fila[2])) is False:
                
                tabla.insert('', 'end', values =fila)

        formato = xlsxwriter.Workbook('comprobantes.xlsx')
        worksheet = formato.add_worksheet('FACTURAS')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 21)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 51)

        formato_titulo = formato.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})
        
        worksheet.write('A1', 'Comprobante', formato_titulo)

        lambda_uniques = filter(lambda c: c[0] == 'Factura', df_fila)
        lambda_uniques_retencion = filter(lambda c: c[0] == 'Comprobante de Retención', df_fila)
        lambda_uniques_credito = filter(lambda c: c[0] == 'Notas de Crédito', df_fila)
        lambda_uniques_debito = filter(lambda c: c[0] == 'Notas de Débito', df_fila)
        lambda_uniques_liquidacion = filter(lambda c: c[0] == 'Liquidación de compra de bienes y prestación de servicios', df_fila)
        df_fila_facturas = list(lambda_uniques)
        cont = 2
        for fila in df_fila_facturas:
            if math.isnan(float(fila[2])) is False:
                        
                a_var = 'A' + str(cont)
                b_var = 'B' + str(cont)
                c_var = 'C' + str(cont)
                d_var = 'D' + str(cont)
                e_var = 'E' + str(cont)
                f_var = 'F' + str(cont)
                g_var = 'G' + str(cont)
                h_var = 'H' + str(cont)
                
                worksheet.write(a_var, fila[0])
                worksheet.write(b_var, fila[1])
                worksheet.write(c_var, fila[2])
                worksheet.write(d_var, fila[3])
                worksheet.write(e_var, fila[4])
                worksheet.write(f_var, fila[5])
                worksheet.write(g_var, fila[6])
                worksheet.write(h_var, fila[7])
                cont += 1
            
        worksheet.write('B1', 'Serie de Comprobante', formato_titulo)
        worksheet.write('C1', 'Ruc Emisor', formato_titulo)
        worksheet.write('D1', 'Razon Social', formato_titulo)
        worksheet.write('E1', 'Emision', formato_titulo)
        worksheet.write('F1', 'Fecha Autorizacion', formato_titulo)
        worksheet.write('G1', 'Tipo de Emision', formato_titulo)
        worksheet.write('H1', 'Clave Acceso', formato_titulo)

        worksheet = formato.add_worksheet('RETENCIONES')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 21)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 51)

        formato_titulo = formato.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})

        
        worksheet.write('A1', 'Comprobante', formato_titulo)

        df_fila_retencion = list(lambda_uniques_retencion)
        cont = 2
        for fila in df_fila_retencion:
            if math.isnan(float(fila[2])) is False:
                        
                a_var = 'A' + str(cont)
                b_var = 'B' + str(cont)
                c_var = 'C' + str(cont)
                d_var = 'D' + str(cont)
                e_var = 'E' + str(cont)
                f_var = 'F' + str(cont)
                g_var = 'G' + str(cont)
                h_var = 'H' + str(cont)
                
                worksheet.write(a_var, fila[0])
                worksheet.write(b_var, fila[1])
                worksheet.write(c_var, fila[2])
                worksheet.write(d_var, fila[3])
                worksheet.write(e_var, fila[4])
                worksheet.write(f_var, fila[5])
                worksheet.write(g_var, fila[6])
                worksheet.write(h_var, fila[7])
                cont += 1
            
        worksheet.write('B1', 'Serie de Comprobante', formato_titulo)
        worksheet.write('C1', 'Ruc Emisor', formato_titulo)
        worksheet.write('D1', 'Razon Social', formato_titulo)
        worksheet.write('E1', 'Emision', formato_titulo)
        worksheet.write('F1', 'Fecha Autorizacion', formato_titulo)
        worksheet.write('G1', 'Tipo de Emision', formato_titulo)
        worksheet.write('H1', 'Clave Acceso', formato_titulo)

        worksheet = formato.add_worksheet('NOTAS C.')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 21)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 51)

        formato_titulo = formato.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})

        
        worksheet.write('A1', 'Comprobante', formato_titulo)

        df_fila_credito = list(lambda_uniques_credito)
        cont = 2
        for fila in df_fila_credito:
            if math.isnan(float(fila[2])) is False:
                        
                a_var = 'A' + str(cont)
                b_var = 'B' + str(cont)
                c_var = 'C' + str(cont)
                d_var = 'D' + str(cont)
                e_var = 'E' + str(cont)
                f_var = 'F' + str(cont)
                g_var = 'G' + str(cont)
                h_var = 'H' + str(cont)
                
                worksheet.write(a_var, fila[0])
                worksheet.write(b_var, fila[1])
                worksheet.write(c_var, fila[2])
                worksheet.write(d_var, fila[3])
                worksheet.write(e_var, fila[4])
                worksheet.write(f_var, fila[5])
                worksheet.write(g_var, fila[6])
                worksheet.write(h_var, fila[7])
                cont += 1
            
        worksheet.write('B1', 'Serie de Comprobante', formato_titulo)
        worksheet.write('C1', 'Ruc Emisor', formato_titulo)
        worksheet.write('D1', 'Razon Social', formato_titulo)
        worksheet.write('E1', 'Emision', formato_titulo)
        worksheet.write('F1', 'Fecha Autorizacion', formato_titulo)
        worksheet.write('G1', 'Tipo de Emision', formato_titulo)
        worksheet.write('H1', 'Clave Acceso', formato_titulo)

        worksheet = formato.add_worksheet('NOTAS D.')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 21)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 51)

        formato_titulo = formato.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})

        
        worksheet.write('A1', 'Comprobante', formato_titulo)

        df_fila_debito = list(lambda_uniques_debito)
        cont = 2
        for fila in df_fila_debito:
            if math.isnan(float(fila[2])) is False:
                        
                a_var = 'A' + str(cont)
                b_var = 'B' + str(cont)
                c_var = 'C' + str(cont)
                d_var = 'D' + str(cont)
                e_var = 'E' + str(cont)
                f_var = 'F' + str(cont)
                g_var = 'G' + str(cont)
                h_var = 'H' + str(cont)
                
                worksheet.write(a_var, fila[0])
                worksheet.write(b_var, fila[1])
                worksheet.write(c_var, fila[2])
                worksheet.write(d_var, fila[3])
                worksheet.write(e_var, fila[4])
                worksheet.write(f_var, fila[5])
                worksheet.write(g_var, fila[6])
                worksheet.write(h_var, fila[7])
                cont += 1
            
        worksheet.write('B1', 'Serie de Comprobante', formato_titulo)
        worksheet.write('C1', 'Ruc Emisor', formato_titulo)
        worksheet.write('D1', 'Razon Social', formato_titulo)
        worksheet.write('E1', 'Emision', formato_titulo)
        worksheet.write('F1', 'Fecha Autorizacion', formato_titulo)
        worksheet.write('G1', 'Tipo de Emision', formato_titulo)
        worksheet.write('H1', 'Clave Acceso', formato_titulo)

        worksheet = formato.add_worksheet('LIQUIDACIONES')
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 21)
        worksheet.set_column('G:G', 13)
        worksheet.set_column('H:H', 51)

        formato_titulo = formato.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#333f4f',
        'font_color': 'white',
        'text_wrap': True})

        
        worksheet.write('A1', 'Comprobante', formato_titulo)

        df_fila_liquidacion = list(lambda_uniques_liquidacion)
        cont = 2
        for fila in df_fila_liquidacion:
            if math.isnan(float(fila[2])) is False:
                        
                a_var = 'A' + str(cont)
                b_var = 'B' + str(cont)
                c_var = 'C' + str(cont)
                d_var = 'D' + str(cont)
                e_var = 'E' + str(cont)
                f_var = 'F' + str(cont)
                g_var = 'G' + str(cont)
                h_var = 'H' + str(cont)
                
                worksheet.write(a_var, fila[0])
                worksheet.write(b_var, fila[1])
                worksheet.write(c_var, fila[2])
                worksheet.write(d_var, fila[3])
                worksheet.write(e_var, fila[4])
                worksheet.write(f_var, fila[5])
                worksheet.write(g_var, fila[6])
                worksheet.write(h_var, fila[7])
                cont += 1
            
        worksheet.write('B1', 'Serie de Comprobante', formato_titulo)
        worksheet.write('C1', 'Ruc Emisor', formato_titulo)
        worksheet.write('D1', 'Razon Social', formato_titulo)
        worksheet.write('E1', 'Emision', formato_titulo)
        worksheet.write('F1', 'Fecha Autorizacion', formato_titulo)
        worksheet.write('G1', 'Tipo de Emision', formato_titulo)
        worksheet.write('H1', 'Clave Acceso', formato_titulo)

        formato.close()

    def Limpiar():
        tabla.delete(*tabla.get_children())

    Button(frame2,width=20,pady=7,text='Abrir',bg='red',fg='white',border=0,command=abrir_archivo).place(x=10,y=3)

    Button(frame2,width=20,pady=7,text='Mostrar',bg='red',fg='white',border=0,command=datos_txt).place(x=200,y=3)
    
    Button(frame2,width=20,pady=7,text='Limpiar',bg='red',fg='white',border=0,command=Limpiar).place(x=400,y=3)

    indica = Label(frame2, fg='gray',border=0,bg='white', text='Ubicación del archivo', font=('Microsoft YaHei UI',11))
    indica.place(x=600,y=3)

    vent.mainloop()

def signin():
    username=user.get()
    password=passw.get()

    if username=='admin' and password=='123456':
        login.destroy()
        ventanaComprobante()
        

frame=Frame(login,width=350,height=350,bg="white")
frame.place(x=50,y=70)

img2 = PhotoImage(file ="D:\\SriTkinter\\LOGO-ISHIDA32.png" )
Label(login,image=img2).place(x=35,y=30,width=400,height=75)

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get() 
    if name=='':
        user.insert(0,'Usuario')

user = Entry(frame, width=25,fg='gray',border=0,bg='white',font=('Microsoft YaHei UI',11))
user.place(x=30,y=80)
user.insert(0, 'Usuario')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='gray').place(x=25,y=107)

def on_enter(e):
    passw.delete(0, 'end')

def on_leave(e):
    name=passw.get() 
    if name=='':
        passw.insert(0,'Contraseña')

def conectar_bd():
    login.destroy()
    import registro_BD

def show_hide_psd():
    if(passw.get()):
        passw.config(show="")
    else:
        passw.config(show="*")      
    
passw = Entry(frame, width=25,fg='gray', show='*', border=0,bg='white',font=('Microsoft YaHei UI',11))
passw.place(x=30,y=150)
passw.insert(0, 'Contraseña')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='gray').place(x=25,y=177)

ojopass = PhotoImage(file = "D:\\SriTkinter\\ojo.png")

Button(frame,width=60,pady=7,text='Mostrar',image=ojopass,bg='white',fg='white',border=0,command=show_hide_psd).place(x=260,y=125)

Button(frame,width=39,pady=7,text='Iniciar Sesión',bg='red',fg='white',border=0,command=signin).place(x=35,y=225)
Button(frame,width=39,pady=7,text='Conectar Base de Datos',bg='red',fg='white',border=0,command=conectar).place(x=35,y=280)

menubar=Menu(login)
menubasedat=Menu(menubar,tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos",command=conectar_bd)
menubasedat.add_command(label="Salir",command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)
login.config(menu=menubar)

login.mainloop()
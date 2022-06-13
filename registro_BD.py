# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
import sqlite3
import random

# Desarrollo de la Interfaz grafica
root=Tk()
root.title("Base de Datos")
root.geometry("990x456")
root.resizable(False,False)

"""mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "0123456789"
base = mayus+numeros
longitud = 7
muestra = random.sample(base, longitud)
miEmpresa = "".join(muestra)
miempresa2 ="".join(muestra)"""

miId=StringVar()
miServidor=StringVar()
#miEmpresa=str(miEmpresa)
#miempresa2 = str(miempresa2)
miNombreBD=StringVar()
miNombreBDMain=StringVar()
miNombreUser=StringVar()
miContrasena=StringVar()



def conexionBBDD():
	miConexion=sqlite3.connect("base2")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE parametros (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
            SERVIDOR VARCHAR(50) NOT NULL,
			NOMBRE_BD VARCHAR(50) NOT NULL,
			NOMBRE_BD_MAIN VARCHAR(50) NOT NULL,
			NOMBRE_USER VARCHAR(50) NOT NULL,
            CONTRASENA INT NOT NULL,
			NOMBRE_EMPRESA VARCHAR(50),
			ESTATUS TEXT DEFAULT "I" NOT NULL)
			''')
		messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")
	except:
		messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")

def eliminarBBDD():
	miConexion=sqlite3.connect("base2")
	miCursor=miConexion.cursor()
	if messagebox.askyesno(message="¿Los Datos se perderan definitivamente, Desea continuar?", title="ADVERTENCIA"):
		miCursor.execute("DROP TABLE parametros")
	else:
		pass
	limpiarCampos()
	mostrar()

def salirAplicacion():
	valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		root.destroy()
		import Login_Sri

def volver_inicio():
	root.destroy()
	import Login_Sri		

def limpiarCampos():
	miId.set("")
	miServidor.set("")
	#miempresa2
	miNombreBD.set("")
	miNombreBDMain.set("")
	miNombreUser.set("")
	miContrasena.set("")

def mensaje():
	acerca='''
	Aplicación CRUD
	Version 1.0
	Tecnología Python Tkinter
	'''
	messagebox.showinfo(title="INFORMACION", message=acerca)

################################ Métodos CRUD ##############################

def crear():
    miConexion=sqlite3.connect("base2")
    miCursor=miConexion.cursor()
    try:
        datos=miServidor.get(),miNombreBD.get(),miNombreBDMain.get(),miNombreUser.get(),miContrasena.get()
        miCursor.execute("INSERT INTO parametros(SERVIDOR, NOMBRE_BD,NOMBRE_BD_MAIN, NOMBRE_USER, CONTRASENA) VALUES(?,?,?,?,?)", (datos))
        miConexion.commit()
    except Exception as e:
        messagebox.showwarning("ADVERTENCIA",e)
        pass
    limpiarCampos()
    mostrar()

def mostrar():
	miConexion=sqlite3.connect("base2")
	miCursor=miConexion.cursor()
	registros=tree.get_children()
	for elemento in registros:
		tree.delete(elemento)

	try:
		miCursor.execute("SELECT * FROM parametros")
		for row in miCursor:
			tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[7],row[6]))
	except:
		pass

                ################################## Tabla ################################

tree=ttk.Treeview(height=10, columns=('#0','#1','#2','#3','#4','#5','#6'))
style = ttk.Style()
style.configure('Treeview', rowheight=30)
tree.place(x=0, y=130)
tree.column('#0',width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="Servidor", anchor=CENTER)
tree.column('#2', width=100)
tree.heading('#2', text="Nombre BD", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Nombre BD Main", anchor=CENTER)
tree.column('#4', width=100)
tree.heading('#4', text="Nombre Usuario", anchor=CENTER)
tree.column('#5', width=100)
tree.heading('#5', text="Contraseña", anchor=CENTER)
tree.column('#6', width=100)
tree.heading('#6', text="Estatus", anchor=CENTER)
tree.heading('#7', text="Codigo", anchor=CENTER)

def seleccionarUsandoClick(event):
	item=tree.identify('item',event.x,event.y)
	miId.set(tree.item(item,"text"))
	miServidor.set(tree.item(item,"values")[0])
	miNombreBD.set(tree.item(item,"values")[1])
	miNombreBDMain.set(tree.item(item,"values")[2])
	miNombreUser.set(tree.item(item,"values")[3])
	miContrasena.set(tree.item(item,"values")[4])
	
tree.bind("<Double-1>", seleccionarUsandoClick)



def actualizar():
	miConexion=sqlite3.connect("base2")
	miCursor=miConexion.cursor()
	try:
		datos=miServidor.get(),miNombreBD.get(),miNombreBDMain.get(),miNombreUser.get(),miContrasena.get()
		miCursor.execute("UPDATE parametros SET SERVIDOR=?, NOMBRE_BD=?, NOMBRE_BD_MAIN=?, NOMBRE_USER=?, CONTRASENA=?, ESTATUS = 'A' WHERE ID="+miId.get(), (datos))
		miCursor.execute("UPDATE parametros SET ESTATUS = 'I' WHERE ID!="+miId.get())
		miConexion.commit()
	except Exception as e:
		print(e)
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
		pass
	limpiarCampos()
	mostrar()

def borrar():
	miConexion=sqlite3.connect("base2")
	miCursor=miConexion.cursor()
	try:
		if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
			miCursor.execute("DELETE FROM parametros WHERE ID="+miId.get())
			miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
		pass
	limpiarCampos()
	mostrar()
mostrar()
###################### Colocar widgets en la VISTA ######################
########## Creando Los menus ###############
menubar=Menu(root)
menubasedat=Menu(menubar,tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Volver al Inicio", command=volver_inicio)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda",menu=ayudamenu)

############## Creando etiquetas y cajas de texto ###########################
e1=Entry(root, textvariable=miId)

l2=Label(root, text="Servidor")
l2.place(x=50,y=10)
e2=Entry(root, textvariable=miServidor, width=30)
e2.place(x=100, y=10)

l3=Label(root, text="Base de Datos")
l3.place(x=300,y=10)
e3=Entry(root, textvariable=miNombreBD)
e3.place(x=380, y=10)

l7=Label(root, text="Base de Datos Main")
l7.place(x=300,y=40)
e7=Entry(root, textvariable=miNombreBDMain)
e7.place(x=415, y=40)

l4=Label(root, text="Nombre Usuario")
l4.place(x=50,y=40)
e4=Entry(root, textvariable=miNombreUser, width=23)
e4.place(x=140, y=40)

l5=Label(root, text="Contraseña")
l5.place(x=550,y=40)
e5=Entry(root, textvariable=miContrasena, width=20)
e5.place(x=620,y=40)


################# Creando botones ###########################

b1=Button(root, text="Crear Registro", command=crear)
b1.place(x=50, y=90)
b2=Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=180, y=90)
b4=Button(root, text="Eliminar Registro", command=borrar)
b4.place(x=340, y=90)
b3=Button(root, text="Guardar y Salir",bg="green", command=volver_inicio)
b3.place(x=490, y=90)


root.config(menu=menubar)


root.mainloop()
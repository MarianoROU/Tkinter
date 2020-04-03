from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

#---------FUNCIONES------------------------------------------------------------------------

def  Conexion_BBDD():

    mi_conexion = sqlite3.connect('IngresoApp')

    mi_cursor = mi_conexion.cursor()

    try:

        mi_cursor.execute('''
            CREATE TABLE EMPLEO (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_EMPLEO VARCHAR(50),
            NOMINAL_EMPLEO INTEGER,
            VALOR_HORA DECIMAL(5,2))
            ''')
        mi_cursor.execute('''
                    CREATE TABLE RECIBO (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MES_RECIBO VARCHAR(12),
                    TRABAJO_RECIBO VARCHAR(20),
                    NOMINAL_RECIBO INTEGER,
                    HORA_RECIBO INTEGER,
                    EXTRA_RECIBO INTEGER,
                    FERIADO_RECIBO INTEGER,
                    JUBILATORIO_RECIBO DECIMAL(9,2),
                    FONASA_RECIBO DECIMAL(9,2),
                    ADICIONAL_RECIBO DECIMAL(9,2),
                    FRL_RECIBO DECIMAL(9,2),
                    ADELANTO_RECIBO INTEGER,
                    FALTAS_RECIBO INTEGER,
                    AÑO_RECIBO INTEGER)
                    ''')

        messagebox.showinfo('BBDD', 'BBDD creada con exito')

    except:

        messagebox.showwarning(' ATENCION', 'La base de datos ya exixte')

def Salir_Aplicacion():

    valor = messagebox.askquestion('Salir', ' Deseas salir de la aplicacion?')

    if valor == 'yes':
        raiz.destroy()

def Get_Recibo():
    registro = tree_recibo.get_children()
    for elemento in registro:
        tree_recibo.delete(elemento)

    try:

        mi_conexion = sqlite3.connect('IngresoApp')
        mi_cursor = mi_conexion.cursor()
        mi_cursor.execute("""SELECT * FROM RECIBO ORDER BY MES_RECIBO """)
    except:
        valor = messagebox.askquestion(' ATENCION', 'No cuenta con una base de datos. Desea crearla ahora?')
        if valor == 'yes':
            Conexion_BBDD()


    for fila in mi_cursor:
        tree_recibo.insert('', END, text=fila[1:], values=fila[1:])

def VentanaNuevoEmpleo():

    def Crear():
        mi_conexion = sqlite3.connect('IngresoApp')
        mi_cursor = mi_conexion.cursor()
        hora_valor = round(float((empleo_nominal.get()/30)/8), 2)
        datos = empleo_nombre.get(), empleo_nominal.get(), hora_valor

        mi_cursor.execute("INSERT INTO EMPLEO VALUES(NULL,?,?,?)", (datos))
        mi_conexion.commit()

        messagebox.showinfo('BBDD', 'Insert realizado')
        ventana_nuevo_empleo.destroy()
        VentanaNuevoEmpleo()

    def Eliminar():

        name = tree.item(tree.selection())['values']
        nombre = name[0]
        mi_conexion = sqlite3.connect('IngresoApp')
        mi_cursor = mi_conexion.cursor()
        mi_cursor.execute("DELETE FROM EMPLEO WHERE NOMBRE_EMPLEO='" + nombre + "'")
        mi_conexion.commit()
        messagebox.showinfo('BBDD', 'Empleo eliminado')
        ventana_nuevo_empleo.destroy()
        VentanaNuevoEmpleo()

    def Get_Empleo():
        registro = tree.get_children()
        for elemento in registro:
            tree.delete(elemento)

        mi_conexion = sqlite3.connect('IngresoApp')
        mi_cursor = mi_conexion.cursor()
        mi_cursor.execute("""SELECT * FROM EMPLEO ORDER BY ID """)

        for fila in mi_cursor:
            tree.insert('', END, text=fila[1:], values=fila[1:])


    ventana_nuevo_empleo = Toplevel()
    ventana_nuevo_empleo.title("Gestion de empleo")
    ventana_nuevo_empleo.geometry("600x500+200+200")
    ventana_nuevo_empleo.config(bg="#5882FA")
    frame_nuevo_empleo = Frame(ventana_nuevo_empleo)
    frame_nuevo_empleo.grid(row=0, column=0)
    frame_lista = Frame(ventana_nuevo_empleo)
    frame_lista.grid(row=1, column=0)

    empleo_nombre = StringVar()
    empleo_nominal = IntVar()

    input_nombre = Entry(frame_nuevo_empleo, textvariable=empleo_nombre)
    input_nombre.grid(row=0, column=1, padx=10, pady=10)
    label_nombre = Label(frame_nuevo_empleo, text='Nombre empleo: ')
    label_nombre.grid(row=0, column=0, sticky='e', padx=10, pady=10)

    input_nominal = Entry(frame_nuevo_empleo, textvariable=empleo_nominal)
    input_nominal.grid(row=1, column=1, padx=10, pady=10)
    label_nominal = Label(frame_nuevo_empleo, text='Salario nominal: ')
    label_nominal.grid(row=1, column=0, sticky='e', padx=10, pady=10)

    boton_crear = Button(frame_nuevo_empleo, text='Crear', command=Crear)
    boton_crear.grid(row=3, column=1, sticky='e', padx=10, pady=10)

    tree = ttk.Treeview(frame_lista)
    tree.pack()
    tree["columns"] = ["Nombre de empleo", "Salario nominal", "Valor hora"]
    tree["show"] = "headings"
    tree.heading("#1", text="Nombre empleo")
    tree.heading("#2", text="Salario nominal")
    tree.heading("#3", text="Valor hora")
    Get_Empleo()

    boton_crear = Button(frame_lista, text='Eliminar empleo', command=Eliminar)
    boton_crear.pack()

def VentanaGenerarRecibo():
    hora_extra = IntVar()
    hora_extra_especial = IntVar()
    hora_extra_feriado = IntVar()
    adelanto = IntVar()
    dia_faltado = IntVar()

    def Get_Empleo():
        registro = tree.get_children()
        for elemento in registro:
            tree.delete(elemento)

        try:

            mi_conexion = sqlite3.connect('IngresoApp')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute("""SELECT * FROM EMPLEO ORDER BY ID """)
        except:
            valor = messagebox.askquestion(' ATENCION', 'No cuenta con una base de datos. Desea crearla ahora?')
            if valor == 'yes':
                Conexion_BBDD()

        for fila in mi_cursor:
            tree.insert('', END, text=fila[1:], values=fila[1:])

    def Crear():
        mi_conexion = sqlite3.connect('IngresoApp')
        mi_cursor = mi_conexion.cursor()
        name = tree.item(tree.selection())['values']
        hora = round((name[1]/30)/8, 2)

        jubilatorio = (0.15*(name[1]+ hora_extra.get() + hora_extra_especial.get() + hora_extra_feriado.get()))
        fonasa = (0.03*name[1])
        adicional = (0.015*name[1])
        frl = (0.00125*name[1])


        datos = input_mes.get(), name[0], name[1], hora_extra.get(), hora_extra_especial.get(), hora_extra_feriado.get(), jubilatorio, fonasa, adicional, frl, adelanto.get(), dia_faltado.get(), input_año.get()

        mi_cursor.execute("INSERT INTO RECIBO VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)", (datos))
        mi_conexion.commit()

        def CreaTxt():
            d_extra = "" + str(hora_extra.get()) + " X " + str(hora * 2) + ""
            t_extra = str((hora_extra.get() * hora) * 2)

            d_ext_e = "" + str(hora_extra_especial.get()) + " X " + str(hora * 2) + ""
            t_ext_e = str((hora_extra_especial.get() * hora) * 2)

            d_ext_f = "" + str(hora_extra_feriado.get()) + " X " + str(hora * 2) + ""
            t_ext_f = str((hora_extra_feriado.get() * hora) * 2)

            total_haberes = int(name[1]) + ((hora_extra.get() * hora) * 2) + ((hora_extra_especial.get() * hora) * 2) + (
                        (hora_extra_feriado.get() * hora) * 2)
            t_haberes = str(total_haberes)



            total_descuento = (frl - jubilatorio - fonasa - adicional - adelanto.get()) * -1
            t_descuento = str(total_descuento)
            liquido = str(total_haberes - total_descuento)

            a = open("" + name[0] + ".txt", "w")

            a.write("RECIBO DE SUELDO CORRESPONDIENTE AL MES DE " + input_mes.get() + " de "+input_año.get()+ " \n")
            a.write("\n \n \n HABERES -------------DETALLE LIQUIDACION----------------IMPORTE \n\n")
            a.write("Salario nominal:                                          " + str(name[1]) + "\n")
            a.write("Horas extra com:           " + d_extra + "                      " + t_extra + "\n")
            a.write("Horas ext. esp.:           " + d_ext_e + "                      " + t_ext_e + "\n")
            a.write("Horas ext. fer.:           " + d_ext_f + "                      " + t_ext_f + "\n")
            a.write("-----------------------------------------------------------------------\n")
            a.write("                                           Total haberes: " + t_haberes + "\n")
            a.write("-----------------------------------------------------------------------\n")

            a.write("\n \n \n DESCUENTOS ----------DETALLE DESCUENTOS-----------------IMPORTE \n\n")
            a.write("Aporte Jubilatorio      15% de " + t_haberes + "                    " + str(jubilatorio) + "\n")
            a.write("FRL                  0.125% de " + t_haberes + "                    " + str(frl) + "\n")
            a.write("FONASA                   3% de " + t_haberes + "                    " + str(fonasa) + "\n")
            a.write("ADIC                   1.5% de " + t_haberes + "                    " + str(adicional) + "\n")
            a.write("Adelantos            Adelantos de sueldo                  " + str(adelanto.get()) + "\n")
            a.write("-----------------------------------------------------------------------\n")
            a.write("                                       Total descuentos:  " + t_descuento + "\n")
            a.write("-----------------------------------------------------------------------\n")
            a.write("LIQUIDO A COBRAR: $" + liquido + " \n")
            a.close()
        CreaTxt()
        messagebox.showinfo('BBDD', 'Recibo generado')
        ventana_generar_recibo.destroy()


    ventana_generar_recibo = Toplevel()
    ventana_generar_recibo.title("Gestion de recibos")
    ventana_generar_recibo.geometry("600x500+200+200")
    ventana_generar_recibo.config(bg="#5882FA")
    frame_recibo = Frame(ventana_generar_recibo)
    frame_recibo.pack()
    frame_lista = Frame(ventana_generar_recibo)
    frame_lista.pack()

    input_mes = ttk.Combobox(frame_recibo, values=['Enero', 'Febrero', 'Marzo', 'Abril',
                                                      'Mayo', 'Junio', 'Julio', 'Agosto',
                                                      'Setiembre', 'Octubre', 'Noviembre', 'Diciembre',
                                                    ], state="readonly")
    input_mes.current(0)
    input_mes.grid(row=0, column=1, padx=10, pady=10)
    label_mes = Label(frame_recibo, text='Mes: ')
    label_mes.grid(row=0, column=0, padx=10, pady=10)

    años = list(range(2020, 2031))
    input_año = ttk.Combobox(frame_recibo, values=años, state="readonly")
    input_año.current(0)
    input_año.grid(row=0, column=3, padx=10, pady=10)
    label_año = Label(frame_recibo, text='Año: ')
    label_año.grid(row=0, column=2, padx=2, pady=10)

    input_extra = Entry(frame_recibo, textvariable=hora_extra)
    input_extra.grid(row=2, column=0, padx=10, pady=10)
    label_extra = Label(frame_recibo, text='N° horas extra:')
    label_extra.grid(row=1, column=0, padx=10)

    input_especial = Entry(frame_recibo, textvariable=hora_extra_especial)
    input_especial.grid(row=2, column=1, padx=10, pady=10)
    label_especial = Label(frame_recibo, text='N° horas extra especial:')
    label_especial.grid(row=1, column=1, padx=10)

    input_feriado = Entry(frame_recibo, textvariable=hora_extra_feriado)
    input_feriado.grid(row=2, column=2, padx=10, pady=10)
    label_feriado = Label(frame_recibo, text='N° horas extra feriado:')
    label_feriado.grid(row=1, column=2, padx=10)

    input_adelanto = Entry(frame_recibo, textvariable=adelanto)
    input_adelanto.grid(row=4, column=1, padx=10, pady=10)
    label_adelanto = Label(frame_recibo, text='Total adelantos en $')
    label_adelanto.grid(row=3, column=1, padx=10)

    input_falta = Entry(frame_recibo, textvariable=dia_faltado)
    input_falta.grid(row=4, column=0, padx=10, pady=10)
    label_falta = Label(frame_recibo, text='N° dias faltados:')
    label_falta.grid(row=3, column=0, padx=10)

    tree = ttk.Treeview(frame_lista)
    tree.pack()
    tree["columns"] = ["Nombre de empleo", "Salario nominal", "Valor hora"]
    tree["show"] = "headings"
    tree.heading("#1", text="Nombre empleo")
    tree.heading("#2", text="Salario nominal")
    tree.heading("#3", text="Valor hora")
    Get_Empleo()

    boton_generar = Button(frame_lista, text='Generar recibo', command=Crear)
    boton_generar.pack()





#------------------------------------------------------------------------------------------





#----------------------------- VENTANA PRINCIPAL-------------------------------------------
raiz = Tk()
raiz.title("Mi Ingreso App")
raiz.resizable(0, 0)
raiz.geometry("700x500")
raiz.config(bg="#5882FA")
raiz.config(cursor="hand2")
#------------------------------------------------------------------------------------------

#------------MENU SUPERIOR-----------------------------------------------------------------
#-- SE CREA EL MENUBAR
barra_menu= Menu(raiz)
raiz.config(menu=barra_menu, width=500, height=500)
#---- OPCION BBDD-----
bbdd_menu= Menu(barra_menu, tearoff=0)
bbdd_menu.add_command(label='Conectar', command=Conexion_BBDD)
bbdd_menu.add_command(label='Salir', command=Salir_Aplicacion)

#---- OPCION ACERCA DE... ------
ayuda_menu= Menu(barra_menu, tearoff=0)
ayuda_menu.add_command(label='Acerca de...')

#----- SE CREA CASCADA DE OPCIONES ----
barra_menu.add_cascade(label='BBDD', menu=bbdd_menu)
barra_menu.add_cascade(label='Ayuda', menu=ayuda_menu)
#-------------------------------------------------------------------------------------------

#------------FRAME CONTENEDOR PRINCIPAL-----------------------------------------------------
frame_empleo = Frame(raiz)
frame_recibo = Frame(raiz)
frame_recibo.place(x=80, y=50)
frame_empleo.place(x=550, y=50)

frame_empleo.config(bg='red', width=100, height=100)
frame_recibo.config(bg='green', width=100, height=100)




boton_nuevo_empleo = Button(frame_empleo, text='Empleos', command=VentanaNuevoEmpleo)
boton_nuevo_empleo.grid(row=1, column=0, sticky='e', padx=10, pady=10)

boton_nuevo_recibo = Button(frame_recibo, text='Recibos', command=VentanaGenerarRecibo)
boton_nuevo_recibo.grid(row=2, column=0, sticky='e', padx=10, pady=10)


'''frame_principal = Frame(raiz)
frame_principal.place(x=595, y=55)
frame_mostrar_recibo = Frame(raiz)
frame_mostrar_recibo.grid(row=1, column=0)

boton_nuevo_empleo = Button(frame_principal, text='Nuevo Empleo', command=VentanaNuevoEmpleo)
boton_nuevo_empleo.grid(row=1, column=0, sticky='e', padx=10, pady=10)

boton_nuevo_recibo = Button(frame_principal, text='Generar recibo', command=VentanaGenerarRecibo)
boton_nuevo_recibo.grid(row=2, column=0, sticky='e', padx=10, pady=10)

tree_recibo = ttk.Treeview(frame_mostrar_recibo)
tree_recibo.pack()
tree_recibo["columns"] = ["Mes", "Empleo", "Liquido"]
tree_recibo["show"] = "headings"
tree_recibo.heading("#1", text="Mes")
tree_recibo.heading("#2", text="Empleo")
tree_recibo.heading("#3", text="Liquido")
Get_Recibo()
'''



raiz.mainloop()
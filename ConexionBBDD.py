from tkinter import *
#import mariadb
import sys
import mysql.connector

root = Tk()
root.title("Ventana principal")
root.geometry("300x260")

try:
    conexion = mysql.connector.connect(
        user="root",
        password="Silvio123456",
        #password="",
        #host="127.0.0.1",
        host='localhost',
        port=3306,
        database="practica"
    )

    if conexion.is_connected():
        print("Conectado")

    cursor = conexion.cursor()

    #Label(root, text="Se conecto correctamente a la base de datos " +
                     #conexion.database + ".").pack()

except mysql.connector.Error as error:
    print(f"Error al conectar con la base de datos:{error}")
    sys.exit()

def registro_cliente():
    nombre = e_nombre.get()
    apellidos = e_apellidos.get()
    telefono = e_telefono.get()
    direccion = e_direccion.get()

    try:
        #cursor.execute('INSERT INTO clientes(nombre, apellidos, telefono,direccion)VALUES(%s, %s, %s, %s)',(nombre, apellidos, telefono, direccion))
        #conexion.commit()

        sql = 'INSERT INTO clientes(nombre, apellidos, telefono, direccion) VALUES (%s, %s, %s, %s)'
        datos = (nombre, apellidos, telefono, direccion)

        cursor.execute(sql, datos)
        conexion.commit()

        # Para que guarde los cambios en la base de bd
    except mysql.connector.Error as error_registro:
        print(f"Error en el registro: {error_registro}")

#Interfaz gráfica
Label(root,text="Registro para nuevos clientes", font="calibri 18", fg="red").grid(row=0, columnspan=2)

Label(root,text="Nombre").grid(row=1, column=0, pady=10)

e_nombre = Entry(root)
e_nombre.grid(row=1, column=1)

Label(root,text="Apellidos").grid(row=2, column=0, pady=10)

e_apellidos = Entry(root)
e_apellidos.grid(row=2, column=1)

Label(root,text="Dirección").grid(row=4, column=0, pady=10)

e_direccion = Entry(root)
e_direccion.grid(row=4, column=1)

Label(root,text="Teléfono").grid(row=5, column=0, pady=10)

e_telefono = Entry(root)
e_telefono.grid(row=5, column=1)

boton = Button(root, text="Registrar", command=registro_cliente).grid(row=6, columnspan=2)


# Conexión con el serv MySQL Server


# Consulta SQL que eje, en este caso un select
sqlSelect = """SELECT * FROM clientes """

# cone con el serv MySQL
#cursor = conex.cursor()
# El cursor, eje la consulta SQL
cursor.execute(sqlSelect)
# Guarda el resul de la consulta en una variable
resulSQL = cursor.fetchall()

# Cer el cursor y la cone con MySQL
cursor.close()
conexion.close()

# Mue el resul por panta
print(resulSQL)

mainloop()


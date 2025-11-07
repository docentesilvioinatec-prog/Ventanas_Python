from tkinter import *
import mariadb

root = Tk()
root.title("Ventana principal")
root.geometry("300x200")

try:
    conexión = mariadb.connect(
        user="root",
        password="",
        host="127.0.0.1",
        port=3306,
        database="practica"
    )

    Label(root, text="Se conecto correctamente a la base de datos " +
                     conexión.database + ".").pack()

except mariadb.Error as error:
    print(f"Error al conectar con la base de datos:{error}")

mainloop()

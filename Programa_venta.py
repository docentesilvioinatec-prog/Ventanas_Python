import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


# --- 1. CONFIGURACIÓN GLOBAL Y CONEXIÓN A DB ---
class AplicacionCRUD:
    def __init__(self, master):
        self.master = master
        master.title("Login de Sistema")
        self.conexion = None
        self.cursor = None

        # Intento de conexión a la base de datos
        try:
            self.conexion = mysql.connector.connect(
                user="root",
                password="Silvio123456",
                host='localhost',
                port=3306,
                database="practica"
            )
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()
                print("Conexión a la base de datos exitosa.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a MySQL: {error}")
            self.master.destroy()
            return

        self.crear_interfaz_login()

    def __del__(self):
        # Asegurarse de cerrar la conexión al salir
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            print("Conexión a la base de datos cerrada.")

    # --- 2. INTERFAZ DE LOGIN ---
    def crear_interfaz_login(self):
        self.master.geometry("300x150")

        tk.Label(self.master, text="USUARIO:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.user_entry = tk.Entry(self.master)
        self.user_entry.grid(row=0, column=1, padx=10, pady=5)
        self.user_entry.insert(0, "admin")  # Valor por defecto para prueba

        tk.Label(self.master, text="CONTRASEÑA:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.pass_entry = tk.Entry(self.master, show="*")
        self.pass_entry.grid(row=1, column=1, padx=10, pady=5)
        self.pass_entry.insert(0, "1234")  # Valor por defecto para prueba

        tk.Button(self.master, text="Iniciar Sesión", command=self.verificar_login).grid(row=2, column=0, columnspan=2,
                                                                                         pady=10)

    def verificar_login(self):
        usuario = self.user_entry.get()
        contrasena = self.pass_entry.get()

        # En un sistema real, verificarías la contraseña en la base de datos.
        # Aquí usamos un valor fijo para simplificar el ejemplo de un solo archivo.
        if usuario == "admin" and contrasena == "1234":
            self.abrir_menu_principal()
        else:
            messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

    # --- 3. VENTANA DE MENÚ PRINCIPAL ---
    def abrir_menu_principal(self):
        # Ocultar la ventana de login
        self.master.withdraw()

        self.menu_window = tk.Toplevel(self.master)
        self.menu_window.title("Menú Principal")
        self.menu_window.geometry("300x200")

        tk.Label(self.menu_window, text="Bienvenido al Sistema", font=("Arial", 16)).pack(pady=20)

        # Botón para el CRUD de Clientes
        tk.Button(self.menu_window, text="Administrar Clientes", width=20, command=self.abrir_crud_clientes).pack(
            pady=5)

        # Botón para el CRUD de Productos
        tk.Button(self.menu_window, text="Administrar Productos", width=20, command=self.abrir_crud_productos).pack(
            pady=5)

        # Al cerrar el menú, volvemos a mostrar el login o salimos
        self.menu_window.protocol("WM_DELETE_WINDOW", self.cerrar_menu)

    def cerrar_menu(self):
        self.menu_window.destroy()
        self.master.deiconify()  # Muestra la ventana de login de nuevo

    # --- 4. VENTANA DE CRUD CLIENTES ---
    def abrir_crud_clientes(self):
        crud_clientes_window = tk.Toplevel(self.menu_window)
        crud_clientes_window.title("CRUD de Clientes")
        crud_clientes_window.geometry("800x450")

        # Título
        tk.Label(crud_clientes_window, text="Gestión de Clientes", font=("Arial", 16)).pack(pady=10)

        # --- Frame para Botones ---
        frame_botones = tk.Frame(crud_clientes_window)
        frame_botones.pack(pady=10)

        # Botones de Acción
        tk.Button(frame_botones, text="➕ Agregar", command=lambda: self.abrir_formulario_cliente("Agregar", None)).pack(
            side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="✏️ Modificar",
                  command=lambda: self.abrir_formulario_cliente("Modificar", crud_clientes_window)).pack(side=tk.LEFT,
                                                                                                         padx=10)
        tk.Button(frame_botones, text="🗑️ Borrar", command=lambda: self.eliminar_cliente(crud_clientes_window)).pack(
            side=tk.LEFT, padx=10)

        # --- Treeview (Tabla) para mostrar datos ---
        columnas = ("ID", "Nombre", "Apellidos", "Teléfono", "Dirección")
        #columnas = ("Nombre", "Apellidos", "Teléfono", "Dirección")

        self.tree_clientes = ttk.Treeview(crud_clientes_window, columns=columnas, show='headings')

        # Configuración de las cabeceras
        self.tree_clientes.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_clientes.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree_clientes.heading("Apellidos", text="Apellidos", anchor=tk.W)
        self.tree_clientes.heading("Teléfono", text="Teléfono", anchor=tk.CENTER)
        self.tree_clientes.heading("Dirección", text="Dirección", anchor=tk.W)

        # Configuración del ancho de las columnas
        self.tree_clientes.column("ID", width=50, stretch=tk.NO)
        self.tree_clientes.column("Nombre", width=150)
        self.tree_clientes.column("Apellidos", width=150)
        self.tree_clientes.column("Teléfono", width=100)
        self.tree_clientes.column("Dirección", width=300)

        self.tree_clientes.pack(fill='both', expand=True, padx=10, pady=5)

        # Cargar los datos al abrir la ventana
        self.cargar_clientes()

        # Función auxiliar para cargar/actualizar los datos en la tabla

    def cargar_clientes(self):
        # Limpiar datos previos
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)

        try:
            sql = "SELECT id_cliente, nombre, apellidos, telefono, direccion FROM clientes"
            #sql = "SELECT nombre, apellidos, telefono, direccion FROM clientes"

            self.cursor.execute(sql)
            registros = self.cursor.fetchall()
            print("hola")
            print(registros)

            # Insertar los nuevos registros en la tabla
            for row in registros:
                self.tree_clientes.insert('', tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Error DB", f"Error al cargar clientes: {err}")

    def eliminar_cliente(self, parent_window):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un cliente para borrar.")
            return

        # Obtener el ID del cliente seleccionado
        item = self.tree_clientes.item(seleccion[0])
        ID_cliente = item['values'][0]

        if messagebox.askyesno("Confirmar Borrado",
                               f"¿Estás seguro de que deseas eliminar al cliente con ID: {ID_cliente}?"):
            try:
                sql = "DELETE FROM clientes WHERE id_cliente = %s"
                self.cursor.execute(sql, (ID_cliente,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.cargar_clientes()  # Recargar la tabla
            except mysql.connector.Error as err:
                messagebox.showerror("Error DB", f"Error al borrar cliente: {err}")
                self.conexion.rollback()

    def abrir_formulario_cliente(self, modo, parent_window):
        cliente_a_modificar = None

        if modo == "Modificar":
            seleccion = self.tree_clientes.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un cliente para modificar.")
                return

            # Obtener los datos actuales del cliente
            item = self.tree_clientes.item(seleccion[0])
            cliente_a_modificar = item['values']  # (ID, Nombre, Apellido, Teléfono, Dirección)

        # Crear la nueva ventana Toplevel
        formulario_window = tk.Toplevel(parent_window)
        formulario_window.title(f"{modo} Cliente")
        formulario_window.geometry("350x350")

        # Campos del formulario (usamos un diccionario para manejar las Entries fácilmente)
        campos = ["Nombre:", "Apellidos:", "Teléfono:", "Dirección:"]
        entries = {}

        for i, campo in enumerate(campos):
            tk.Label(formulario_window, text=campo).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            e = tk.Entry(formulario_window, width=35)
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[campo.strip(':')] = e

            # Si estamos modificando, rellenar los campos
            if modo == "Modificar" and cliente_a_modificar:
                # Los índices en cliente_a_modificar son: 1=Nombre, 2=Apellido, 3=Teléfono, 4=Dirección
                datos_iniciales = {
                    "Nombre": cliente_a_modificar[1],
                    "Apellidos": cliente_a_modificar[2],
                    "Teléfono": cliente_a_modificar[3],
                    "Dirección": cliente_a_modificar[4]
                }
                e.insert(0, datos_iniciales[campo.strip(':')])

        # Botón de Guardar que llama a la función de manejo
        if modo == "Agregar":
            accion = lambda: self.guardar_cliente(modo, entries, None, formulario_window)
        else:  # Modificar
            cliente_id = cliente_a_modificar[0]
            accion = lambda: self.guardar_cliente(modo, entries, cliente_id, formulario_window)

        tk.Button(formulario_window, text="Guardar", command=accion).grid(row=len(campos), column=0, columnspan=2,
                                                                          pady=20)

    # Función que maneja tanto la inserción como la actualización
    def guardar_cliente(self, modo, entries, cliente_id, formulario_window):
        # Obtener los valores de los campos
        nombre = entries["Nombre"].get()
        apellidos = entries["Apellidos"].get()
        telefono = entries["Teléfono"].get()
        direccion = entries["Dirección"].get()

        if not all([nombre, apellidos]):
            messagebox.showwarning("Datos Faltantes", "Los campos Nombre y Apellidos son obligatorios.")
            return

        try:
            if modo == "Agregar":
                sql = 'INSERT INTO clientes(nombre, apellidos, telefono, direccion) VALUES (%s, %s, %s, %s)'
                datos = (nombre, apellidos, telefono, direccion)
            else:  # Modificar
                sql = 'UPDATE clientes SET nombre = %s, apellidos = %s, telefono = %s, direccion = %s WHERE id_cliente = %s'
                datos = (nombre, apellidos, telefono, direccion, cliente_id)
                #datos = (nombre, apellidos, telefono, direccion)

            self.cursor.execute(sql, datos)
            self.conexion.commit()

            messagebox.showinfo("Éxito", f"Cliente {modo}do correctamente.")
            formulario_window.destroy()  # Cerrar el formulario
            self.cargar_clientes()  # Recargar la tabla principal

        except mysql.connector.Error as err:
            messagebox.showerror("Error DB", f"Error al guardar: {err}")
            self.conexion.rollback()

    # --- 5. VENTANA DE CRUD PRODUCTOS ---
    def abrir_crud_productos(self):
        crud_productos_window = tk.Toplevel(self.menu_window)
        crud_productos_window.title("CRUD de Productos")
        crud_productos_window.geometry("850x450")

        # Título
        tk.Label(crud_productos_window, text="Gestión de Productos", font=("Arial", 16)).pack(pady=10)

        # Frame para Botones
        frame_botones = tk.Frame(crud_productos_window)
        frame_botones.pack(pady=10)

        # Botones de Acción
        tk.Button(frame_botones, text="➕ Agregar",
                  command=lambda: self.abrir_formulario_producto("Agregar", None)).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botones, text="✏️ Modificar",
                  command=lambda: self.abrir_formulario_producto("Modificar", crud_productos_window)).pack(side=tk.LEFT,
                                                                                                           padx=10)
        tk.Button(frame_botones, text="🗑️ Borrar", command=lambda: self.eliminar_producto(crud_productos_window)).pack(
            side=tk.LEFT, padx=10)

        # Treeview (Tabla) para mostrar datos
        columnas = ("ID", "Nombre", "Descripción", "Cantidad", "Precio")
        self.tree_productos = ttk.Treeview(crud_productos_window, columns=columnas, show='headings')

        # Configuración de las cabeceras
        self.tree_productos.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_productos.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree_productos.heading("Descripción", text="Descripción", anchor=tk.W)
        self.tree_productos.heading("Cantidad", text="Cantidad", anchor=tk.CENTER)
        self.tree_productos.heading("Precio", text="Precio", anchor=tk.E)  # Alineación a la derecha

        # Configuración del ancho de las columnas
        self.tree_productos.column("ID", width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.tree_productos.column("Nombre", width=150, anchor=tk.W)
        self.tree_productos.column("Descripción", width=350, anchor=tk.W)
        self.tree_productos.column("Cantidad", width=80, anchor=tk.CENTER)
        self.tree_productos.column("Precio", width=100, anchor=tk.E)

        self.tree_productos.pack(fill='both', expand=True, padx=10, pady=5)

        # Cargar los datos al abrir la ventana
        self.cargar_productos()

    def cargar_productos(self):
        # Limpiar datos previos
        for i in self.tree_productos.get_children():
            self.tree_productos.delete(i)

        try:
            sql = "SELECT id_producto, nombre, descripcion, cantidad, precio FROM productos"
            self.cursor.execute(sql)
            registros = self.cursor.fetchall()

            # Insertar los nuevos registros en la tabla
            for row in registros:
                self.tree_productos.insert('', tk.END, values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Error DB", f"Error al cargar productos: {err}")

    # Función de borrado de producto
    def eliminar_producto(self, parent_window):
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto para borrar.")
            return

        # Obtener el ID del producto seleccionado
        item = self.tree_productos.item(seleccion[0])
        producto_id = item['values'][0]

        if messagebox.askyesno("Confirmar Borrado",
                               f"¿Estás seguro de que deseas eliminar el producto ID {producto_id}?"):
            try:
                sql = "DELETE FROM productos WHERE id_producto = %s"
                self.cursor.execute(sql, (producto_id,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.cargar_productos()  # Recargar la tabla
            except mysql.connector.Error as err:
                messagebox.showerror("Error DB", f"Error al borrar producto: {err}")
                self.conexion.rollback()

    def abrir_formulario_producto(self, modo, parent_window):
        producto_a_modificar = None

        if modo == "Modificar":
            seleccion = self.tree_productos.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un producto para modificar.")
                return

            # Obtener los datos actuales del producto
            item = self.tree_productos.item(seleccion[0])
            producto_a_modificar = item['values']  # (ID, Nombre, Descripción, Cantidad, Precio)

        # Crear la nueva ventana Toplevel
        formulario_window = tk.Toplevel(self.menu_window)
        formulario_window.title(f"{modo} Producto")
        formulario_window.geometry("400x350")

        # Campos del formulario
        campos = ["Nombre:", "Descripción:", "Cantidad:", "Precio:"]
        entries = {}

        for i, campo in enumerate(campos):
            tk.Label(formulario_window, text=campo).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            e = tk.Entry(formulario_window, width=40)
            e.grid(row=i, column=1, padx=10, pady=5)
            entries[campo.strip(':')] = e

            # Si estamos modificando, rellenar los campos
            if modo == "Modificar" and producto_a_modificar:
                # Los índices en producto_a_modificar son: 1=Nombre, 2=Desc, 3=Cant, 4=Precio
                datos_iniciales = {
                    "Nombre": producto_a_modificar[1],
                    "Descripción": producto_a_modificar[2],
                    "Cantidad": producto_a_modificar[3],
                    "Precio": producto_a_modificar[4]
                }
                e.insert(0, datos_iniciales[campo.strip(':')])

        # Botón de Guardar que llama a la función de manejo
        if modo == "Agregar":
            accion = lambda: self.guardar_producto(modo, entries, None, formulario_window)
        else:  # Modificar
            producto_id = producto_a_modificar[0]
            accion = lambda: self.guardar_producto(modo, entries, producto_id, formulario_window)

        tk.Button(formulario_window, text="Guardar", command=accion).grid(row=len(campos), column=0, columnspan=2,
                                                                          pady=20)

    # Función que maneja tanto la inserción como la actualización de productos
    def guardar_producto(self, modo, entries, producto_id, formulario_window):
        # Obtener los valores de los campos
        nombre = entries["Nombre"].get()
        descripcion = entries["Descripción"].get()

        try:
            cantidad = int(entries["Cantidad"].get())
            precio = float(entries["Precio"].get())
        except ValueError:
            messagebox.showwarning("Error de Datos",
                                   "Cantidad debe ser un número entero y Precio debe ser un número decimal.")
            return

        if not all([nombre, cantidad, precio]):
            messagebox.showwarning("Datos Faltantes", "Nombre, Cantidad y Precio son obligatorios.")
            return

        try:
            if modo == "Agregar":
                sql = 'INSERT INTO productos(nombre, descripcion, cantidad, precio) VALUES (%s, %s, %s, %s)'
                datos = (nombre, descripcion, cantidad, precio)
            else:  # Modificar
                sql = 'UPDATE productos SET nombre = %s, descripcion = %s, cantidad = %s, precio = %s WHERE id_producto = %s'
                datos = (nombre, descripcion, cantidad, precio, producto_id)

            self.cursor.execute(sql, datos)
            self.conexion.commit()

            messagebox.showinfo("Éxito", f"Producto {modo}do correctamente.")
            formulario_window.destroy()  # Cerrar el formulario
            self.cargar_productos()  # Recargar la tabla principal

        except mysql.connector.Error as err:
            messagebox.showerror("Error DB", f"Error al guardar producto: {err}")
            self.conexion.rollback()


# --- 6. INICIO DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionCRUD(root)
    root.mainloop()
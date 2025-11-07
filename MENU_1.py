import collections
import sys
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk, Menu, scrolledtext as st, filedialog as fd, messagebox as mb


class AplicacionGUI:
    def __init__(self, ventana):
        self.ventana = ventana

        #Configuración Ventana
        # ----------------------------------------------------------------------
        ventana.title("Menu de funciones")
        ventana.geometry("900x700")


        # ----------------------------------------------------------------------

        def abrir_editor_texto():
            ventana_secundaria = tk.Toplevel(ventana)
            ventana_secundaria.title("Editor de texto")
            ventana_secundaria.geometry("800x400")

            menubar1 = tk.Menu(ventana_secundaria)
            ventana_secundaria.config(menu=menubar1)

            scrolledtext1 = st.ScrolledText(ventana_secundaria, width=80, height=20)
            scrolledtext1.grid(column=0, row=0, padx=10, pady=10)

            opciones1 = tk.Menu(menubar1, tearoff=0)
            opciones1.add_command(label="Guardar archivo", command=lambda: guardar(scrolledtext1))
            opciones1.add_command(label="Recuperar archivo", command=lambda: recuperar(scrolledtext1))
            opciones1.add_separator()
            opciones1.add_command(label="Salir", command=lambda: salir(ventana_secundaria))
            menubar1.add_cascade(label="Archivo", menu=opciones1)

            def salir(ventana_cerrar):
                ventana_cerrar.destroy()

            def guardar(scrolledtext1):
                nombrearch = fd.asksaveasfilename(initialdir="/", title="Guardar como",
                                              filetypes=(("txt files", "*.txt"), ("todos los archivos", "*.*")))
                if nombrearch != '':
                    archi1 = open(nombrearch, "w", encoding="utf-8")
                    archi1.write(scrolledtext1.get("1.0", tk.END))
                    archi1.close()
                    mb.showinfo("Información", "Los datos fueron guardados en el archivo.")

            def recuperar(scrolledtext1):
                nombrearch = fd.askopenfilename(initialdir="/", title="Seleccione archivo",
                                                filetypes=(("txt files", "*.txt"), ("todos los archivos", "*.*")))
                if nombrearch != '':
                    archi1 = open(nombrearch, "r", encoding="utf-8")
                    contenido = archi1.read()
                    archi1.close()
                    scrolledtext1.delete("1.0", tk.END)
                    scrolledtext1.insert("1.0", contenido)

        def abrir_ventana_calculadora():
            ventana_secundaria = tk.Toplevel(ventana)
            ventana_secundaria.title("Calculadora Básica")
            ventana_secundaria.geometry("400x400")

            # region funciones calculadora

            def sumar():
                try:
                    num1 = float(campo_num1.get())
                    num2 = float(campo_num2.get())
                    resultado = num1 + num2
                    etiqueta_resultado.config(text=f"Resultado: {resultado}")
                except valueError:
                    etiqueta_resultado.config(text="Error: Ingresa números válidos")

            def restar():
                try:
                    num1 = float(campo_num1.get())
                    num2 = float(campo_num2.get())
                    resultado = num1 - num2
                    etiqueta_resultado.config(text=f"Resultado: {resultado}")
                except valueError:
                    etiqueta_resultado.config(text="Error: Ingresa números válidos")

            def multiplicar():
                try:
                    num1 = float(campo_num1.get())
                    num2 = float(campo_num2.get())
                    resultado = num1 * num2
                    etiqueta_resultado.config(text=f"Resultado: {resultado}")
                except valueError:
                    etiqueta_resultado.config(text="Error: Ingresa números válidos")

            def dividir():
                try:
                    num1 = float(campo_num1.get())
                    num2 = float(campo_num2.get())
                    if  num2 == 0:
                        etiqueta_resultado.config(text = "Error: No se puede dividir por cero")
                    else:
                        resultado = num1 / num2
                        etiqueta_resultado.config(text=f"Resultado: {resultado}")
                except valueError:
                    etiqueta_resultado.config(text="Error: Ingresa números válidos")

            def potencia():
                try:
                    num1 = float(campo_num1.get())
                    num2 = float(campo_num2.get())
                    resultado = num1 ** num2
                    etiqueta_resultado.config(text=f"Resultado: {resultado}")
                except valueError:
                    etiqueta_resultado.config(text="Error: Ingresa números válidos")

            # endregion

            # region configurar interfaz

            #Título
            tk.Label(ventana_secundaria, text="CALCULADORA BÁSICA", font= ("Arial", 16, "bold"), bg = "lightgreen").pack(pady = 10)

            #Primer número
            tk.Label(ventana_secundaria, text="Primer número", font=("Arial", 12)).pack(pady=5)
            campo_num1 = tk.Entry(ventana_secundaria, font=("Arial", 12), width= 20, justify = "center")
            campo_num1.pack(pady = 5)

            # Segundo número
            tk.Label(ventana_secundaria, text="Segundo número", font=("Arial", 12)).pack(pady=5)
            campo_num2 = tk.Entry(ventana_secundaria, font=("Arial", 12), width=20, justify="center")
            campo_num2.pack(pady=5)

            #Frame para organizar los botones en filas
            frame_botones = tk.Frame(ventana_secundaria)
            frame_botones.pack(pady = 20)

            #Primera fila de botones
            boton_suma = tk.Button(frame_botones, text ="+ Sumar", command = sumar, bg="lightgreen", width = 10)
            boton_suma.grid(row=0, column=0, padx=5, pady=5)

            boton_resta = tk.Button(frame_botones, text="- Restar", command= restar, bg="lightcoral", width=10)
            boton_resta.grid(row=0, column=1, padx=5, pady=5)

            boton_multiplicar = tk.Button(frame_botones, text="* Multiplicar", command= multiplicar, bg="lightblue", width=10)
            boton_multiplicar.grid(row=0, column=2, padx=5, pady=5)

            # Segunda fila de botones
            boton_dividir = tk.Button(frame_botones, text="/ Dividir", command= dividir, bg="lightyellow", width=10)
            boton_dividir.grid(row=1, column=0, padx=5, pady=5)

            boton_potencia = tk.Button(frame_botones, text="^ Potencia", command=potencia, bg="plum", width=10)
            boton_potencia.grid(row=1, column=1, padx=5, pady=5)

            #Resultado
            etiqueta_resultado = tk.Label(ventana_secundaria, text="Resultado aparecerá aquí",
                                          font= ("Arial", 14, "bold"), bg = "white",
                                          relief="sunken", width=30, height=2)
            etiqueta_resultado.pack(pady = 20)

            # endregion

            # Botón para cerrar la ventana secundaria
            #boton_cerrar = tk.Button(ventana_secundaria, text="Cerrar", command=ventana_secundaria.destroy)
            #boton_cerrar.pack(pady=10)

        def abrir_ventana_seno():
            #ventana_secundaria = tk.Toplevel(ventana)
            #ventana_secundaria.title("Función seno")
            #ventana_secundaria.geometry("400x400")

            x=np.linspace(0,10,100)
            y=np.sin(x)
            plt.plot(x,y,label = 'y=sin(x)')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Grafico')
            plt.show()

        def abrir_ventana_grafico_animado():
            data = (collections.deque([0]*100, maxlen=100))


            def data_gen():
                for k in range(100):
                    t=k/100
                    yield 0.5*np.sin(40*t)*np.exp(-2*t)

            fig= plt.figure()
            ax = plt.axes()
            ax.set_title('Señal')
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Amplitud")
            ax.set_xlim(0,100)
            ax.set_ylim(-1,1)
            lines = ax.plot([],[])[0]

            def animate(values):
                value = values
                data.append(value)
                lines.set_data(range(0,100), data)
                return lines
            anim = animation.FuncAnimation(fig, animate, data_gen, interval = 5)
            plt.show()

        def abrir_ventana_encuesta():
            ventana_secundaria = tk.Toplevel(ventana)
            ventana_secundaria.title("Encuesta")
            ventana_secundaria.geometry("400x400")

        #Configuracion Menu
        # ----------------------------------------------------------------------
        barra_menu = Menu(ventana)
        ventana.config(menu = barra_menu)

        menu_calculadora = Menu(barra_menu, tearoff = 0)

        barra_menu.add_cascade(label="Funciones",menu=menu_calculadora)
        menu_calculadora.add_command(label="Editor de texto", command = abrir_editor_texto)
        menu_calculadora.add_command(label="Calculadora basica", command = abrir_ventana_calculadora)
        menu_calculadora.add_command(label="Nuevo calculo seno", command = abrir_ventana_seno)
        menu_calculadora.add_command(label="Nuevo grafico animado", command = abrir_ventana_grafico_animado)
        menu_calculadora.add_command(label="Encuesta", command=abrir_ventana_encuesta)

        menu_calculadora.add_separator()
        menu_calculadora.add_command(label="Salir", command=ventana.quit)

        # ----------------------------------------------------------------------








#boton = tk.Button(ventana, text ="hacer clic", font = ("Arial", 12))
#boton.pack(pady = 10)

#boton = tk.Button(ventana, text ="izquierda", font = ("Arial", 12))
#boton.pack(anchor="w", pady = 10)


#def suma():
 #   etiqueta_resultado.config(text = "resultado")

#etiqueta_resultado = tk.Label(ventana, text="etiqueta verde derecha", font= ("Arial", 14), bg = "lightgreen")
#etiqueta_resultado.pack(anchor = "w", pady = 20)

#boton_resultado = tk.Button(ventana, text ="boton resultado", command = suma, font = ("Arial", 12), bg = "lightgray")
#boton_resultado.pack(pady = 10)



#Editor de texto
#Calculadora con operaciones basicas
#Encuesta
#Opcion salir.


# ----------------------------------------------------------------------
#                          EJECUCION PRINCIPAL
# ----------------------------------------------------------------------

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionGUI(ventana)
    ventana.mainloop()
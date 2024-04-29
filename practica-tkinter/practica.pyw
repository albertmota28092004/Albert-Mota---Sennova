from tkinter import *

ventana = Tk()
ventana.title("Hola")
ventana.geometry("400x200")

label = Label(ventana, text="Label prueba")
label.pack()

boton = Button(ventana, text="Presionar")
boton.pack()

ventana.mainloop()


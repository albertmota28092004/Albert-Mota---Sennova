from tkinter import Tk, Button, Label, Frame

vent = Tk()
vent.title("Ejemplo de frame")
vent.geometry("400x200")

frame1 = Frame(vent, bg="blue")
frame1.pack(expand=True, fill="both")

frame2 = Frame(vent, bg="yellow")
frame2.pack(expand=True, fill="both")
frame2.config(cursor="heart")

redbutton = Button(frame1, text="Red", fg="red")
greenbutton = Button(frame1, text="Green", fg="green")
bluebutton = Button(frame1, text="Blue", fg="blue")

redbutton.place(relx=.05, rely=.05, relwidth=.25, relheight=.9)
greenbutton.place(relx=.35, rely=.05, relwidth=.25, relheight=.9)
bluebutton.place(relx=.65, rely=.05, relwidth=.25, relheight=.9)

blackbutton = Button(frame2, text="Black", fg="black")
blackbutton.pack()

vent.mainloop()
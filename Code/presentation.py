from tkinter import *
from tkinter import messagebox
from controller import show_video, capture 
import os 

root = Tk()

def visualizar():
    img = show_video()
    lblVideo.configure(image=img)
    lblVideo.image = img
    lblVideo.after(10, visualizar)

def iniciar():
    capture()
    visualizar()
    

def on_closing():
    if messagebox.askokcancel("Salir", "¿Esta seguro que desea salir?"):
        os.remove('Code\imagenes\Frame.jpg')
        root.destroy()

btnIniciar = Button(root, text="iniciar", command=iniciar)
btnIniciar.grid(column=0, row=0, padx=5, pady=5)

lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
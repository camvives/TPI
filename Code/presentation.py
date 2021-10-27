import tkinter as tk     
from tkinter import messagebox
from controller import *
import os 

def visualizar(exit: bool):
    if not exit:
        try:       
            img = show_video()
            lbl_Video.configure(image=img)
            lbl_Video.image = img

            f = lambda: visualizar(False)
            lbl_Video.after(10, f)     

        except:
            lbl_Video.after_cancel(lbl_Video)

    else:   
        lbl_Video.after_cancel(lbl_Video)
        
def init():
    capture()
    visualizar(False)
    create_video_window()
    
def on_closing():
    if messagebox.askokcancel("Salir", "¿Esta seguro que desea salir?"):
        try:
            os.remove('Code\imagenes\Frame.jpg')
        except:
            pass

        video_window.destroy()
        root.destroy()

def on_closing_video_window():
    release()
    visualizar(True)
    video_window.withdraw()
    root.deiconify()

def create_video_window():
    video_window.deiconify()
    root.withdraw()
    video_window.state('zoomed')
    
def get_color():
    global COLOR
    if COLOR == (0,0,0):
        return "black"
    elif COLOR == (0,255,0):
        return "green"
    elif COLOR == (255,0,0):
        return "red"


# Creación de ventanas
root = tk.Tk()
video_window = tk.Toplevel(root)
video_window.withdraw()

# Ventana principal
root.geometry("800x500")
root.resizable(0,0)
root.title("FaceMask Detector")

# Imagen de fondo y texto de ventana principal
bg = tk.PhotoImage(file="Code\imagenes\\background.png")
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")
canvas.create_text(400, 150, text="FaceMask Detector", font=("Helvetica", 50))

# Botones ventana principal
frame = tk.Frame(root)
frame.pack(pady=20)

btn_init = tk.Button(root, text="Iniciar",font=("Helvetica", 15), width=40, command=init)
btn_init_window = canvas.create_window(170, 250, anchor="nw", window=btn_init)

btn_stats = tk.Button(root, text="Estadísticas", font=("Helvetica", 12), width=20)
btn_stats_window = canvas.create_window(300, 320, anchor="nw", window=btn_stats)

# Ventana de video

lbl_Video = tk.Label(video_window)
lbl_Video.grid(column=0, row=1, columnspan=2)

color = get_color()
text = TEXT

frame = tk.Frame(video_window, width=300, height=50, highlightbackground=color, highlightthickness=2)
frame.place(x=50, y=500)
label = tk.Label(frame, text="test", font=("Helvetica", 30)).pack()


# Protocolos de cierre
root.protocol("WM_DELETE_WINDOW", on_closing)
video_window.protocol("WM_DELETE_WINDOW", on_closing_video_window)

root.mainloop()
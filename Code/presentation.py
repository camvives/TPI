import tkinter as tk     
from tkinter import messagebox
from controller import show_video, capture, release
import os 

def visualizar():
    global exit 
    if not exit:
        img = show_video()
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)


def init():
    global exit
    
    exit = False
    capture()
    visualizar()
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
    global exit
    
    exit = True
    release()
    video_window.withdraw()
    root.deiconify()

def create_video_window():
    video_window.deiconify()
    root.withdraw()
    
exit = False

# Creación de ventanas
root = tk.Tk()
video_window = tk.Toplevel(root)
video_window.withdraw()

# Ventana principal
root.geometry("800x500")
root.resizable(0,0)
root.title("FaceMask Detector")

bg = tk.PhotoImage(file="Code\imagenes\\background.png")
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

canvas.create_text(400, 150, text="FaceMask Detector", font=("Helvetica", 50))

frame = tk.Frame(root)
frame.pack(pady=20)

btn_init = tk.Button(root, text="Iniciar",font=("Helvetica", 15), width=40, command=init)
btn_init_window = canvas.create_window(170, 250, anchor="nw", window=btn_init)

btn_stats = tk.Button(root, text="Estadísticas", font=("Helvetica", 12), width=20)
btn_stats_window = canvas.create_window(300, 320, anchor="nw", window=btn_stats)

# Ventana de video
lblVideo = tk.Label(video_window)
lblVideo.grid(column=0, row=1, columnspan=2)

# Protocolos de cierre
root.protocol("WM_DELETE_WINDOW", on_closing)
video_window.protocol("WM_DELETE_WINDOW", on_closing_video_window)

root.mainloop()
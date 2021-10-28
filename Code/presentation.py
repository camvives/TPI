import tkinter as tk     
from tkinter import messagebox
from controller import *
import os 

def visualizar(exit: bool):
    if not exit:
        try:       
            img, color = show_video()
            lbl_Video.configure(image=img)
            lbl_Video.image = img
            set_label(color)
            set_time()
            set_stats()

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

    
def set_label(color):
    if color == (0,0,255):
        label_acceso["fg"] = "red"
        label_acceso["text"] = "ACCESO DENEGADO"

    elif color == (0,255,0):
        label_acceso["fg"] = "green"
        label_acceso["text"] = "ACCESO PERMITIDO"

def set_time():
    active_time = get_time() - START_TIME
    label_time["text"] = active_time

def set_stats():
    (wm, wom, total) = get_session_graph(START_TIME)
    lbl_wm["text"] = wm
    lbl_wom["text"] = wom
    lbl_total["text"] = total

START_TIME = get_time()

# Creación de ventanas
root = tk.Tk()
video_window = tk.Toplevel(root)
video_window.withdraw()

#### Ventana principal ####
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

#### Ventana de video ####
video_window.title("FaceMask Detector")
bg_video = tk.PhotoImage(file="Code\\imagenes\\tk_bg.png")
lbl_bg = tk.Label(video_window, image=bg_video)
lbl_bg.place(x=0, y=0)


# Video
lbl_Video = tk.Label(video_window)
lbl_Video.grid(column=0, row=1, columnspan=2)

## Frame etiqueta de acceso ##
frame_video = tk.Frame(video_window, width=10, height=10)
frame_video.place(x=150, y=550)

label_acceso = tk.Label(frame_video, text="Detectando rostros...", font=("Consolas", 30))
label_acceso.pack(pady=2)

## Frame de tiempo ##
frame_time = tk.Frame(video_window, width=100, height=30)
frame_time.place(x=825, y=70)

lbl_time = tk.Label(frame_time, text="TIEMPO ACTIVO", font=("Consolas", 30))
label_time = tk.Label(frame_time, font=("Consolas", 20))
lbl_time.pack(pady=5)
label_time.pack(pady=10)

# Frames datos sesión # 
frame_data_wm = tk.Frame(video_window, width=10, height=10)
frame_data_wm.place(x=820, y=350)
lbl_wm = tk.Label(frame_data_wm, font=("Consolas", 40)) 
lbl_wm.pack()

frame_data_wom = tk.Frame(video_window, width=10, height=10)
frame_data_wom.place(x=1100, y=350)
lbl_wom = tk.Label(frame_data_wom, font=("Consolas", 40)) 
lbl_wom.pack()

frame_data_total = tk.Frame(video_window, width=10, height=10)
frame_data_total.place(x=1025, y=555)
lbl_total = tk.Label(frame_data_total, font=("Consolas", 30)) 
lbl_total.pack()


#### Protocolos de cierre ####
root.protocol("WM_DELETE_WINDOW", on_closing)
video_window.protocol("WM_DELETE_WINDOW", on_closing_video_window)

root.mainloop()
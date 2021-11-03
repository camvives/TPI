import tkinter as tk     
from tkinter import messagebox
from typing import Tuple
from controller import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from constants import *

class UI(tk.Frame):
    """Ventana de inicio"""
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """widgets de la ventana de inicio"""
        self.parent.title("FaceMask Detector")
        self.parent.iconbitmap('Code\\imagenes\icon.ico')

        # Imagen de fondo
        self.parent.bg_photo = bg_photo = tk.PhotoImage(file="Code\\imagenes\\background.png")
        canvas = tk.Canvas(self.parent, width=800, height=500)   
        canvas.create_image(0, 0, image=bg_photo,anchor="nw" )      
        canvas.create_text(400, 150, text="FaceMask Detector", font=("Helvetica", 50))
        canvas.pack(fill="both", expand=True)

        # Botones ventana principal
        btn_init = tk.Button(self.parent, text="Iniciar",font=("Helvetica", 15), width=40, command=self.new_video_window)
        canvas.create_window(170, 250, anchor="nw", window=btn_init)

        btn_stats = tk.Button(self.parent, text="Estadísticas", font=("Helvetica", 12), width=20, command=self.new_stats_window)
        canvas.create_window(300, 320, anchor="nw", window=btn_stats)

        # Protocolo de cierre
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def new_video_window(self):
        '''Inicia la ventana de video'''
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.grab_set()
        self.app = VideoWindow(self.newWindow)
    
    def new_stats_window(self):
        '''Inicia la ventana de estadísticas'''
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.grab_set()
        self.app = StatsWindow(self.newWindow)

    def on_closing(self):
        '''Cierra la app y elimina la foto del rostro analizada'''
        if messagebox.askokcancel("Salir", "¿Esta seguro que desea salir?"):
            try:
                os.remove('Code\imagenes\Frame.jpg')
            except:
                pass

        self.parent.destroy()

class VideoWindow:
    """Ventana de video que contiene la funcionalidad de detectar máscaras"""
    def __init__(self, parent):
        self.parent = parent
        self.parent.state('zoomed')
        self.parent.bg_photo = bg_photo = tk.PhotoImage(file="Code\\imagenes\\tk_bg.png")
        canvas = tk.Canvas(self.parent, width=800, height=500)   
        canvas.create_image(0, 0, image=bg_photo,anchor="nw" )      
        canvas.pack(fill="both", expand=True)
        
        self.lbl_Video = tk.Label(self.parent)
        self.lbl_Video.place(x=0, y=0)

        ## Frame etiqueta de acceso ##
        self.frame_video = tk.Frame(self.parent, width=10, height=10)
        self.frame_video.place(x=150, y=550)

        self.label_acceso = tk.Label(self.frame_video, text="Detectando...", font=("Consolas", 30))
        self.label_acceso.pack(pady=2)

        ## Frame de tiempo ##
        self.frame_time = tk.Frame(self.parent, width=100, height=30)
        self.frame_time.place(x=850, y=100)
        self.label_time = tk.Label(self.frame_time, font=("Consolas", 25))
        self.label_time.pack(pady=10)

        # Frames datos sesión # 
        self.frame_data_wm = tk.Frame(self.parent, width=10, height=10)
        self.frame_data_wm.place(x=820, y=350)
        self.lbl_wm = tk.Label(self.frame_data_wm, font=("Consolas", 40)) 
        self.lbl_wm.pack()

        self.frame_data_wom = tk.Frame(self.parent, width=10, height=10)
        self.frame_data_wom.place(x=1100, y=350)
        self.lbl_wom = tk.Label(self.frame_data_wom, font=("Consolas", 40)) 
        self.lbl_wom.pack()

        self.frame_data_total = tk.Frame(self.parent, width=10, height=10)
        self.frame_data_total.place(x=975, y=570)
        self.lbl_total = tk.Label(self.frame_data_total, font=("Consolas", 30)) 
        self.lbl_total.pack()

        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        capture()
        self.visualize(False)
        
    def visualize(self, exit: bool):
        '''Muestra la imagen de video con la predicción de máscara y setea los
            el estado, las estadísticas y el tiempo activo actuales'''
        if not exit:
            try:       
                img, color = show_video()
                self.lbl_Video.configure(image=img)
                self.lbl_Video.image = img
                self.set_label(color)
                self.set_time()
                self.set_stats()

                f = lambda: self.visualize(False)
                self.lbl_Video.after(10, f)    
            except:
                self.lbl_Video.after_cancel(self.lbl_Video)
        else:   
            self.lbl_Video.after_cancel(self.lbl_Video)

    def set_label(self, color: Tuple):
        '''Setea la etiqueta de acceso de acuerdo al color de acceso'''
        if color == (0,0,255):
            self.label_acceso["fg"] = "red"
            self.label_acceso["text"] = "ACCESO DENEGADO"

        elif color == (0,255,0):
            self.label_acceso["fg"] = "green"
            self.label_acceso["text"] = "ACCESO PERMITIDO"
    
    def set_time(self):
        '''Setea la etiqueta 'Tiempo Activo' con el tiempo de la sessión actual'''
        active_time = get_time() - START_TIME
        self.label_time["text"] = active_time

    def set_stats(self):
        '''Setea las etiquetas 'Con Máscara', 'Sin Máscara' y 'Total' medidas 
            durante la sesión'''
        (wm, wom, total) = get_session_data(START_TIME)
        self.lbl_wm["text"] = wm
        self.lbl_wom["text"] = wom
        self.lbl_total["text"] = total

    def on_closing(self):
        '''Libera la cámara y cierra la ventana'''
        release()
        self.parent.destroy()
       
class StatsWindow:
    """Ventana con las estadísticas del mes y de la semana"""
    def __init__(self, parent):
        self.parent = parent
        self.parent.state('zoomed')
        
        # Frame de gráficas
        self.frame_stats = tk.Frame(self.parent, width=10, height=10)
        self.frame_stats.place(x=0, y=150)

        # Protocolo de cierre
        self.parent.protocol("WM_DELETE_WINDOW", self.close_windows)

        self.graph_stats()
        
    def graph_stats(self):
        '''Obtiene las gráficas de estadísticas y las sitúa en la ventana'''
        fig = get_month_data()
        fig2 = get_week_data()
        canvas_month = FigureCanvasTkAgg(fig, master=self.frame_stats)
        canvas_month.get_tk_widget().grid(row=1, column=0,  sticky=tk.N+tk.E+tk.S+tk.W)
        canvas_week = FigureCanvasTkAgg(fig2, master=self.frame_stats)
        canvas_week.get_tk_widget().grid(row=1, column=1,  sticky=tk.N+tk.E+tk.S+tk.W)

    def close_windows(self):
        self.parent.destroy()    

def main():
    APP = UI(parent=ROOT)
    APP.mainloop()


  
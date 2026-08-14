import customtkinter as ctk
import numpy as np
from PIL import Image
from tkinter import filedialog

# Configurar el estilo visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Procesador de Imágenes")
        self.geometry("1080x920")

        self.img_original = None  # Variable para almacenar la imagen original
        self.r = None  # Variable para almacenar el canal rojo
        self.g = None  # Variable para almacenar el canal verde
        self.b = None  # Variable para almacenar el canal azul


        # 1. MARCO INFERIOR PARA BOTONES (Se empaqueta primero en 'bottom')
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(side="bottom", fill="x", padx=20, pady=20)

        # Configurar rejilla de 3 columnas dentro del marco
        self.frame_buttons.grid_columnconfigure(0, weight=1)
        self.frame_buttons.grid_columnconfigure(1, weight=1)
        self.frame_buttons.grid_columnconfigure(2, weight=1)

        # Botón Escala de Grises (Alineado a la izquierda)
        self.btn_grayscale = ctk.CTkButton(
            self.frame_buttons, 
            text="Convertir a Escala de Grises", 
            command=self.convertir_grayscale,
            width=240,
            height=50,
            font=ctk.CTkFont(family="Arial", size=15, weight="bold")
        )
        self.btn_grayscale.grid(row=0, column=0, sticky="w")

        # Botón Cargar Imagen (Centrado)
        self.btn_upload = ctk.CTkButton(
            self.frame_buttons, 
            text="Cargar Imagen (JPG/PNG)", 
            command=self.cargar_imagen,
            width=260,
            height=50,
            font=ctk.CTkFont(family="Arial", size=15, weight="bold")
        )
        self.btn_upload.grid(row=0, column=1)

        # 2. CONTENEDOR PARA LA IMAGEN (Toma todo el espacio libre arriba)
        self.lbl_imagen = ctk.CTkLabel(
            self, 
            text="Sin imagen cargada", 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.lbl_imagen.pack(expand=True, fill="both", padx=20, pady=(20, 10))

    def cargar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if path:
            img_pil = Image.open(path).convert("RGB")
            self.img_original = img_pil
            self.mostrar_imagen(img_pil)
            self.setRGBValues()  # Actualizar los valores RGB al cargar la imagen

    def mostrar_imagen(self, img_pil):
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(800, 600))
        self.lbl_imagen.configure(image=img_ctk, text="")


    def setRGBValues(self):
       if self.img_original is not None:
            img_array = np.array(self.img_original)
            self.r = img_array[:, :, 0]
            self.g = img_array[:, :, 1]
            self.b = img_array[:, :, 2]

    

    def convertir_grayscale(self):
        if self.img_original is not None:
            r = self.r
            g = self.g
            b = self.b
            gray = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)

            img_gray = Image.fromarray(gray)
            self.mostrar_imagen(img_gray)

if __name__ == "__main__":
    app = App()
    app.mainloop()
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog

# Configurar el estilo visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Procesador de Imágenes")
        self.geometry("1080x920")

        self.img_original = None # Variable para almacenar la imagen original

        # Contenedor para la imagen
        self.lbl_imagen = ctk.CTkLabel(
            self, 
            text="Sin imagen cargada", 
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.lbl_imagen.pack(expand=True, fill="both", padx=20, pady=(20, 10))

        # Botón para cargar imagen
        self.btn_upload = ctk.CTkButton(
            self, 
            text="Cargar Imagen (JPG/PNG)", 
            command=self.cargar_imagen,
            width=280,
            height=50,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold")
        )
        self.btn_upload.pack(side="bottom", pady=25)

    def cargar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if path:
            img_pil = Image.open(path).convert("RGB")  # Convertir a RGB para asegurar compatibilidad
            self.img_original = img_pil
            self.mostrar_imagen(img_pil)

    def mostrar_imagen(self, img_pil):
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(800, 600))
        self.lbl_imagen.configure(image=img_ctk, text="")

if __name__ == "__main__":
    app = App()
    app.mainloop()
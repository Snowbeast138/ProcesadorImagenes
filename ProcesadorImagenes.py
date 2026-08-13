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

        # Contenedor para la imagen (se empaqueta primero para ocupar el espacio superior)
        self.lbl_imagen = ctk.CTkLabel(
            self, 
            text="Sin imagen cargada", 
            font=("Arial", 24, "bold")
        )
        self.lbl_imagen.pack(expand=True, fill="both", padx=20, pady=(20, 10))

        # Botón para cargar imagen (se empaqueta abajo al centro con mayor tamaño)
        self.btn_upload = ctk.CTkButton(
            self, 
            text="Subir Imagen (JPG/PNG)", 
            command=self.cargar_imagen,
            width=280,
            height=60,
            font=("Arial", 30, "bold")
        )
        self.btn_upload.pack(side="bottom", pady=25)

    def cargar_imagen(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if path:
            # Cargar imagen con Pillow y adaptarla a un tamaño más grande (800x600)
            img_pil = Image.open(path)
            img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(800, 600))
            
            self.lbl_imagen.configure(image=img_ctk, text="")

if __name__ == "__main__":
    app = App()
    app.mainloop()
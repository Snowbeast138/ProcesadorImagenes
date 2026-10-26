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
        self.img_actual = None  # Imagen que se está mostrando/procesando
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
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_grayscale.grid(row=0, column=0, sticky="w")

        self.btn_linear_to_sequential = ctk.CTkButton(
            self.frame_buttons, 
            text="Linear a Secuencial", 
            command=self.linearTosequencial,
            width=240,
            height=50,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_linear_to_sequential.grid(row=0, column=2, sticky="e")

        # Botón Cargar Imagen (Centrado)
        self.btn_upload = ctk.CTkButton(
            self.frame_buttons, 
            text="Cargar Imagen (JPG/PNG)", 
            command=self.cargar_imagen,
            width=260,
            height=50,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_upload.grid(row=0, column=1)

        # Filtros espaciales con máscaras de 3x3
        self.btn_box = ctk.CTkButton(
            self.frame_buttons,
            text="Filtro Box",
            command=self.aplicar_filtro_box,
            width=240,
            height=50,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_box.grid(row=1, column=0, sticky="w", pady=(15, 0))

        self.btn_gauss = ctk.CTkButton(
            self.frame_buttons,
            text="Filtro Gauss",
            command=self.aplicar_filtro_gauss,
            width=260,
            height=50,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_gauss.grid(row=1, column=1, pady=(15, 0))

        self.btn_laplace = ctk.CTkButton(
            self.frame_buttons,
            text="Filtro Laplace",
            command=self.aplicar_filtro_laplace,
            width=240,
            height=50,
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.btn_laplace.grid(row=1, column=2, sticky="e", pady=(15, 0))

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
        self.img_actual = img_pil.copy()
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

    def aplicar_filtro_box(self):
        """Aplica una media uniforme de 3x3 para suavizar la imagen."""
        if self.img_actual is None:
            return

        imagen = np.array(self.img_actual.convert("RGB"), dtype=np.float32)
        kernel_box = np.ones((3, 3), dtype=np.float32) / 9.0
        resultado = self.aplicar_convolucion(imagen, kernel_box)
        resultado = np.clip(resultado, 0, 255).astype(np.uint8)
        self.mostrar_imagen(Image.fromarray(resultado, mode="RGB"))

    def aplicar_filtro_gauss(self):
        """Aplica un suavizado gaussiano ponderado de 3x3."""
        if self.img_actual is None:
            return

        imagen = np.array(self.img_actual.convert("RGB"), dtype=np.float32)
        kernel_gauss = np.array(
            [[1, 2, 1],
             [2, 4, 2],
             [1, 2, 1]],
            dtype=np.float32
        ) / 16.0
        resultado = self.aplicar_convolucion(imagen, kernel_gauss)
        resultado = np.clip(resultado, 0, 255).astype(np.uint8)
        self.mostrar_imagen(Image.fromarray(resultado, mode="RGB"))

    def aplicar_filtro_laplace(self):
        """Detecta bordes mediante la segunda derivada de Laplace."""
        if self.img_actual is None:
            return

        imagen_rgb = np.array(self.img_actual.convert("RGB"), dtype=np.float32)
        imagen_gris = (
            0.299 * imagen_rgb[:, :, 0]
            + 0.587 * imagen_rgb[:, :, 1]
            + 0.114 * imagen_rgb[:, :, 2]
        )
        kernel_laplace = np.array(
            [[0, -1, 0],
             [-1, 4, -1],
             [0, -1, 0]],
            dtype=np.float32
        )
        respuesta = self.aplicar_convolucion(imagen_gris, kernel_laplace)
        bordes = np.clip(np.abs(respuesta), 0, 255).astype(np.uint8)
        resultado = np.stack((bordes, bordes, bordes), axis=-1)
        self.mostrar_imagen(Image.fromarray(resultado, mode="RGB"))

    def aplicar_convolucion(self, imagen, kernel):
        """Aplica una máscara impar a una matriz 2D o a una imagen RGB."""
        alto_kernel, ancho_kernel = kernel.shape
        margen_y = alto_kernel // 2
        margen_x = ancho_kernel // 2

        if imagen.ndim == 2:
            relleno = ((margen_y, margen_y), (margen_x, margen_x))
        else:
            relleno = ((margen_y, margen_y), (margen_x, margen_x), (0, 0))

        # Replicar los bordes permite aplicar el filtro también a esos píxeles
        # y mantener exactamente las dimensiones de la imagen original.
        imagen_con_borde = np.pad(imagen, relleno, mode="edge")
        resultado = np.zeros_like(imagen, dtype=np.float32)
        alto, ancho = imagen.shape[:2]

        for desplazamiento_fila in range(alto_kernel):
            for desplazamiento_columna in range(ancho_kernel):
                resultado += kernel[desplazamiento_fila, desplazamiento_columna] * imagen_con_borde[
                    desplazamiento_fila:desplazamiento_fila + alto,
                    desplazamiento_columna:desplazamiento_columna + ancho
                ]

        return resultado

    def coeficienteLuz(self, r, g, b):
        coeficiente = 0.2126 * r + 0.7152 * g + 0.0722 * b
        ys = 1.055 * (coeficiente ** (1 / 2.4)) - 0.055
        ys = ys*255
        return ys

    def linearTosequencial(self):
        if self.img_original is not None:
           # Convertir a float para evitar pérdida de precisión en operaciones matemáticas
            rs = self.r.astype(np.float32) / 255.0
            gs = self.g.astype(np.float32) / 255.0
            bs = self.b.astype(np.float32) / 255.0

            # Aplicar la transformación usando np.where para evaluar toda la matriz píxel a píxel
            rs = np.where(rs <= 0.0031308, rs / 12.92, ((rs + 0.055) / 1.055) ** 2.4)
            gs = np.where(gs <= 0.0031308, gs / 12.92, ((gs + 0.055) / 1.055) ** 2.4)
            bs = np.where(bs <= 0.0031308, bs / 12.92, ((bs + 0.055) / 1.055) ** 2.4) # (Nota: Asegúrate de usar bs aquí, tenías gs)

            # Reescalar de vuelta a 0-255 y convertir a tipo uint8
            rs_img = np.clip(rs * 255, 0, 255).astype(np.uint8)
            gs_img = np.clip(gs * 255, 0, 255).astype(np.uint8)
            bs_img = np.clip(bs * 255, 0, 255).astype(np.uint8)
            
            gris = self.coeficienteLuz(rs, gs, bs).astype(np.uint8)

            # Imagen en escala de grises
            img_array = np.stack((gris, gris, gris), axis=-1)

            # Crear y mostrar la imagen transformada
            img_new = Image.fromarray(img_array)
            self.mostrar_imagen(img_new)
            

            

            

if __name__ == "__main__":
    app = App()
    app.mainloop()

import tkinter as tk
import re
from PIL import Image, ImageTk
import csv
from tkinter import Scrollbar

def showBook(titulo, genero, contenedor):
        containerBook = tk.Frame(contenedor, bg="red")
        containerBook.pack(fill="both", expand=True)
        image_path = "Recursos/"+genero+".jpg"  # Ruta de la imagen
        img = Image.open(image_path)
        img = img.resize((50, 50))  # Ajustar tamaño de la imagen
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(containerBook, image=img, bg="red")
        image_label.image = img  # Mantener referencia a la imagen para evitar que se elimine
        image_label.pack(padx=10, pady=10, side=tk.LEFT)
        labeltext = tk.Label(containerBook, text= titulo, font="Arial", bg="blue")
        labeltext.pack(side="left", expand=True)
        butoonAgregar = tk.Button(containerBook, bg="blue", text="Obtener")
        butoonAgregar.pack( side="left",expand=True)
        
def extraerDat(archivo, columna, valor):
    with open(archivo, newline='', encoding='latin-1') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[columna] == valor:
                return row['Genero']
    return None

def bookS(entry, parent, pagina):
    libro = entry.get()
    libroBool = buscarCsv("libros.csv", "Titulo", libro)
    if libroBool:
        genero = extraerDat("libros.csv", "Titulo", libro)
        parent.show_frame(pagina)
    else:
        entry.insert(0, "No existe")

        
def leerLibros(archivo_csv):
    nombres_libros = []
    Genero = []
    with open(archivo_csv, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            nombres_libros.append(row['Titulo'])
            Genero.append(row['Genero'])
    return nombres_libros, Genero

def mostrarLibros(contenedor, lista_libros, listaGenero):
    for i in range(len(lista_libros)):
        showBook(lista_libros[i],listaGenero[i], contenedor)

def correoValido(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo) is not None

def buscarCsv(ruta, parametro, search):
    with open(ruta, 'r', encoding='latin-1') as file:
        lineas = file.readlines()
    
    encabezados = lineas[0].strip().split(',')
    filas = []
    
    for linea in lineas[1:]:
        valores = linea.strip().split(',')
        fila = {encabezados[i]: valores[i] for i in range(len(encabezados))}
        filas.append(fila)
    
    for fila in filas:
        if search == fila[parametro]:
            return True
    
    return False

def registrarCsv(ruta, registrar):
    with open(ruta, 'a', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(registrar)
        
def logear(correo, show, password, parent):
    correo = correo.get()
    search = password.get()
    if correoValido(correo):
        UsuarioBool = buscarCsv("Usuarios.csv","correo",correo)
        contrasenaBool = buscarCsv("Usuarios.csv","password",search)
        if UsuarioBool and contrasenaBool:
            parent.show_frame(WindowLibros)
        else:
            show.config(text="Usuario no encontrado")
    else:
        show.config(text="Correo electrónico no válido")

def registrar(correo, show, password, parent):
    correo = correo.get()
    if correoValido(correo):
        registrar = [correo, password.get()]
        registrarCsv("Usuarios.csv", registrar)
        show.config(text="Registro exitoso")
        parent.show_frame(WindowInicio)
    else:
        show.config(text="Correo electrónico no válido")


def labelCreator(parent, text):
    labelAux = tk.Label(parent, text=text)
    labelAux.pack(expand=True, fill="both", padx=10, pady=10)
    return labelAux

def buttonCreator(parent, text, command):
    buttonAux = tk.Button(parent, text=text, command=command)
    buttonAux.pack(expand=True, fill="both", padx=10, pady=10)
    return buttonAux

def entryCreator(parent, show=True):
    entry = tk.Entry(parent, font=('Arial', 12), show='*' if not show else '')
    entry.pack(expand=True, fill="both", padx=10, pady=10)
    return entry

def frameCreator(window, text='', color='#4A4A4A', height=30, size=18):
    frame = tk.Frame(window, bg=color, height=height)
    frame.pack(fill="x")
    frameLabel = tk.Label(frame, text=text, bg=color, fg='white', font=('Arial', size))
    frameLabel.pack()
    return frame


class Window(tk.Tk):
    def __init__(self, name):
        super().__init__()
        self.title(name)
        self.configure(bg='#F5F5F5')
        screen_width, screen_height = self.get_screen_size()
        self.geometry(f"{int(screen_width * 1)}x{int(screen_height * 1)}")
        self.frames = {}
        
        # Configurar el grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Inicializar la ventana de inicio
        self.show_frame(WindowInicio)

    def get_screen_size(self):
        self.update_idletasks()  
        width = self.winfo_screenwidth()  
        height = self.winfo_screenheight()  
        return width, height
    
    def show_frame(self, cont):
        if cont not in self.frames:
            frame = cont(self)
            self.frames[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frames[cont]
        frame.tkraise()


class LoginWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Bienvenido a la Biblioteca Digital", height=50)
        self.labelCorreo = labelCreator(self, "Correo electronico")
        self.correo = entryCreator(self)
        self.labelContrasena = labelCreator(self, "Contraseña")
        self.contrasena = entryCreator(self, show=False)
        self.button = buttonCreator(self, "Iniciar Sesion", lambda: logear(self.correo, self.label_saludo, self.contrasena))
        self.buttonCrearCuenta = buttonCreator(self, "Crear Cuenta", lambda: parent.show_frame(WindowCrearCuenta))
        self.label_saludo = labelCreator(self, "")
        self.footer = frameCreator(self, text="© 2024 Biblioteca Digital", size=10)


class WindowInicio(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Bienvenido a e-Book", height=50)
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill="both", expand=True)

        self.sliderFrame = tk.Frame(self.mainFrame)
        self.sliderFrame.pack(side="left", fill="both", expand=True)

        self.sideFrame = tk.Frame(self.mainFrame)
        self.sideFrame.pack(side="right", fill="both", expand=True)

        self.controlFrame = tk.Frame(self.sideFrame)
        self.controlFrame.pack(fill="both", expand=True)
        self.controlFrame.pack_propagate(False)

        self.image_paths = ["Recursos/1.png", "Recursos/2.png", "Recursos/3.png", "Recursos/4.png", "Recursos/5.png"]
        self.slider = ImageSlider(self.sliderFrame, self.image_paths)

        self.labelCorreo = labelCreator(self.controlFrame, "Correo electronico")
        self.correo = entryCreator(self.controlFrame)
        self.labelContrasena = labelCreator(self.controlFrame, "Contraseña")
        self.contrasena = entryCreator(self.controlFrame, show=False)
        self.buttonIniciarSesion = buttonCreator(self.controlFrame, "Iniciar Sesion", lambda: logear(self.correo, self.labelSaludo, self.contrasena, parent))
        self.buttonCrearCuenta = buttonCreator(self.controlFrame, "Crear Cuenta", lambda: parent.show_frame(WindowCrearCuenta))
        self.labelSaludo = labelCreator(self.controlFrame, "")

        self.footer = frameCreator(self, text="© 2024 e-Book by Trickster 09", size=10)


class WindowCrearCuenta(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Registro a e-Book", height=50)
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(fill="both", expand=True)

        self.sliderFrame = tk.Frame(self.mainFrame)
        self.sliderFrame.pack(side="right", fill="both", expand=True)

        self.sideFrame = tk.Frame(self.mainFrame)
        self.sideFrame.pack(side="left", fill="both", expand=True)

        self.controlFrame = tk.Frame(self.sideFrame)
        self.controlFrame.pack(fill="both", expand=True)
        self.controlFrame.pack_propagate(False)

        self.image_paths = ["Recursos/1a.png", "Recursos/2a.png", "Recursos/3a.png"]
        self.slider = ImageSlider(self.sliderFrame, self.image_paths)

        self.labelSaludo = labelCreator(self.controlFrame, "")
        self.labelCorreo = labelCreator(self.controlFrame, "Correo electronico")
        self.correo = entryCreator(self.controlFrame)
        self.labelContrasena = labelCreator(self.controlFrame, "Contraseña")
        self.contrasena = entryCreator(self.controlFrame, show=False)
        self.buttonRegistrar = buttonCreator(self.controlFrame, "Registrar", lambda: registrar(self.correo, self.labelSaludo, self.contrasena, parent))
        self.labelSaludo1 = labelCreator(self.controlFrame, "")

        self.footer = frameCreator(self, text="© 2024 e-Book by Trickster 09", size=10)

class WindowLibros(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Registro a e-Book", height=50, color="lightgrey")
        self.header.pack(fill="x")

        self.mainFrame = tk.Frame(self, bg="blue")
        self.mainFrame.pack(fill="both", expand=True)
        
        # Contenedor externo (rojo)
        container_red = tk.Frame(self.mainFrame, bg="red")
        container_red.pack(fill="x")
        
        # Contenedor interno (verde) dentro del contenedor externo
        container_green = tk.Frame(container_red, bg="green")
        container_green.pack(fill="x")
        
        entry = tk.Entry(container_green, width=44)
        entry.pack(pady=10, padx=(10, 5), side=tk.LEFT)
        
        searchButton = tk.Button(container_green, text="Buscar", width=10, height=1, bg="blue", command=lambda: bookS(entry, parent, WindowLibroBusqueda))
        searchButton.pack(pady=10, padx=(5, 10), side=tk.LEFT, ipadx=2, ipady=2)
        
        # Contenedor Amarillo
        containerYellow = tk.Frame(container_green, bg="yellow")
        containerYellow.pack(fill="x", expand=False)
        
        perfil = tk.Button(containerYellow, text="Perfil", width=10, height=1, bg="blue")
        perfil.pack(pady=10, padx=125, side=tk.RIGHT, ipadx=2, ipady=2)
        
        # Nuevo frame que contendrá el frame de libros y la barra de desplazamiento
        libros_scroll_frame = tk.Frame(self.mainFrame)
        libros_scroll_frame.pack(fill="both", expand=True)
        
        # Crear el canvas y scrollbar dentro del frame de libros y scrollbar
        canvas = tk.Canvas(libros_scroll_frame, bg='green')
        scrollbar = tk.Scrollbar(libros_scroll_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Función para ajustar el tamaño del frameLibros al del canvas
        def adjust_frame_size(event=None):
            canvas.itemconfigure("frame", width=canvas.winfo_width())  # Ajuste de la anchura del frameLibros al del canvas

        # Contenedor de libros dentro del canvas
        frameLibros = tk.Frame(canvas, bg="green")
        canvas.create_window(0, 0, window=frameLibros, anchor="nw", tags="frame")

        # Llamar a la función para ajustar el tamaño del frameLibros al iniciar el objeto
        adjust_frame_size()

        # Vincular evento de configuración del canvas para ajustar el tamaño del frameLibros
        canvas.bind("<Configure>", adjust_frame_size)
        
        # Configurar el canvas para que se pueda desplazar
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frameLibros.bind("<Configure>", on_frame_configure)
        
        # Leer los nombres de los libros desde el archivo CSV
        nombres_libros, genero = leerLibros('libros.csv')
        
        # Mostrar los contenedores de libros en el frame
        mostrarLibros(frameLibros, nombres_libros, genero)
        
        
class WindowLibroBusqueda(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Registro a e-Book", height=50, color="lightgrey")
        self.header.pack(fill="x")

        self.mainFrame = tk.Frame(self, bg="blue")
        self.mainFrame.pack(fill="both", expand=True)
        
        # Contenedor externo (rojo)
        self.container_red = tk.Frame(self.mainFrame, bg="red")
        self.container_red.pack(fill="x")
        
        # Contenedor interno (verde) dentro del contenedor externo
        container_green = tk.Frame(self.container_red, bg="green")
        container_green.pack(fill="x")
        
        entry = tk.Entry(container_green, width=44)
        entry.pack(pady=10, padx=(10, 5), side=tk.LEFT)
        
        searchButton = tk.Button(container_green, text="Buscar", width=10, height=1, bg="blue", command=lambda: bookS(entry, parent, WindowLibroBusqueda1))
        searchButton.pack(pady=10, padx=(5, 10), side=tk.LEFT, ipadx=2, ipady=2)
        
        # Contenedor Amarillo
        containerYellow = tk.Frame(container_green, bg="yellow")
        containerYellow.pack(fill="x", expand=False)
        
        perfil = tk.Button(containerYellow, text="Perfil", width=10, height=1, bg="blue")
        perfil.pack(pady=10, padx=125, side=tk.RIGHT, ipadx=2, ipady=2)
        showBook("1984", "Distopia", self.container_red)

class WindowLibroBusqueda1(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Registro a e-Book", height=50, color="lightgrey")
        self.header.pack(fill="x")

        self.mainFrame = tk.Frame(self, bg="blue")
        self.mainFrame.pack(fill="both", expand=True)
        
        # Contenedor externo (rojo)
        self.container_red = tk.Frame(self.mainFrame, bg="red")
        self.container_red.pack(fill="x")
        
        # Contenedor interno (verde) dentro del contenedor externo
        container_green = tk.Frame(self.container_red, bg="green")
        container_green.pack(fill="x")
        
        entry = tk.Entry(container_green, width=44)
        entry.pack(pady=10, padx=(10, 5), side=tk.LEFT)
        
        searchButton = tk.Button(container_green, text="Buscar", width=10, height=1, bg="blue", command=lambda: bookS(entry, parent, WindowLibroBusqueda2))
        searchButton.pack(pady=10, padx=(5, 10), side=tk.LEFT, ipadx=2, ipady=2)
        
        # Contenedor Amarillo
        containerYellow = tk.Frame(container_green, bg="yellow")
        containerYellow.pack(fill="x", expand=False)
        
        perfil = tk.Button(containerYellow, text="Perfil", width=10, height=1, bg="blue")
        perfil.pack(pady=10, padx=125, side=tk.RIGHT, ipadx=2, ipady=2)
        showBook("Lolita", "Novela", self.container_red)
        
class WindowLibroBusqueda2(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = frameCreator(self, text="Registro a e-Book", height=50, color="lightgrey")
        self.header.pack(fill="x")

        self.mainFrame = tk.Frame(self, bg="blue")
        self.mainFrame.pack(fill="both", expand=True)
        
        # Contenedor externo (rojo)
        self.container_red = tk.Frame(self.mainFrame, bg="red")
        self.container_red.pack(fill="x")
        
        # Contenedor interno (verde) dentro del contenedor externo
        container_green = tk.Frame(self.container_red, bg="green")
        container_green.pack(fill="x")
        
        entry = tk.Entry(container_green, width=44)
        entry.pack(pady=10, padx=(10, 5), side=tk.LEFT)
        
        searchButton = tk.Button(container_green, text="Buscar", width=10, height=1, bg="blue", command=lambda: bookS(entry, parent, WindowLibroBusqueda1))
        searchButton.pack(pady=10, padx=(5, 10), side=tk.LEFT, ipadx=2, ipady=2)
        
        # Contenedor Amarillo
        containerYellow = tk.Frame(container_green, bg="yellow")
        containerYellow.pack(fill="x", expand=False)
        
        perfil = tk.Button(containerYellow, text="Perfil", width=10, height=1, bg="blue")
        perfil.pack(pady=10, padx=125, side=tk.RIGHT, ipadx=2, ipady=2)
        showBook("El alquimista", "Realismo Magico", self.container_red)
        
class ImageSlider:
    def __init__(self, root, images, speed=1):
        self.root = root
        self.images = images
        self.speed = speed
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        self.overlay = tk.Label(root, bg='black')
        self.overlay.place(x=0, y=0)
        self.overlay.lower()

        self.imageTk = [ImageTk.PhotoImage(Image.open(image)) for image in self.images]

        self.imageY = 0
        self.imageObjects = []

        self.currentImageIndex = 0
        self.transitioning = False

        self.addImages()
        self.moveImages()

    def addImages(self):
        img = self.imageTk[self.currentImageIndex]
        imageObject = self.canvas.create_image(0, self.imageY, anchor='nw', image=img, tags="image")
        self.imageObjects.append(imageObject)
        self.imageY += img.height()

    def moveImages(self):
        if self.canvas.winfo_exists():
            self.canvas.move("image", 0, -self.speed)
            self.checkPosition()
            self.root.after(30, self.moveImages)


    def checkPosition(self):
        canvasHeight = self.canvas.winfo_height()
        if canvasHeight <= 0:
            return
        for imageObject in self.imageObjects:
            coords = self.canvas.coords(imageObject)
            if coords[1] + self.imageTk[self.currentImageIndex].height() <= canvasHeight + 50:
                self.startTransition()
                break

    def startTransition(self):
        if not self.transitioning:
            self.transitioning = True
            self.fadeOut(255)

    def fadeOut(self, alpha):
        if alpha > 0 and self.canvas.winfo_exists():
            self.overlay.config(bg=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(30, self.fadeOut, alpha - 10)
        else:
            self.transportImage()

    def transportImage(self):
        if not self.canvas.winfo_exists():
            return
        self.canvas.delete("image")
        self.imageObjects.clear()
        self.imageY = 0

        self.currentImageIndex = (self.currentImageIndex + 1) % len(self.images)
        self.addImages()

        self.fadeIn(0)

    def fadeIn(self, alpha):
        if alpha < 255 and self.canvas.winfo_exists():
            self.overlay.lift()
            self.overlay.config(bg=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(30, self.fadeIn, alpha + 10)
        else:
            self.overlay.lower()
            self.transitioning = False



if __name__ == "__main__":
    app = Window("e-Book")
    app.mainloop()
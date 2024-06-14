import tkinter as tk
import re
from PIL import Image, ImageTk
import csv

def correoValido(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo) is not None

def buscarCsv(ruta, parametro, search):
    with open(ruta, 'r', encoding='utf-8') as file:
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

def logear(logear, show, password):
    correo = logear.get()
    search = password.get()
    if correoValido(correo):
        UsuarioBool = buscarCsv("Usuarios.csv","correo",correo)
        contrasenaBool = buscarCsv("Usuarios.csv","password",search)
        if UsuarioBool and contrasenaBool:
            show.config(text="Usuario encontrado")
        else:
            show.config(text="Usuario no encontrado")
    else:
        show.config(text="Correo electrónico no válido")

def registrar(logear, show, password):
    correo = logear.get()
    if correoValido(correo):
        registrar = [correo, password.get()]
        registrarCsv("Usuarios.csv", registrar)
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
    if show:
        entry = tk.Entry(parent, font=('Arial', 12))
    else:
        entry = tk.Entry(parent, font=('Arial', 12), show='*')
    entry.pack(expand=True, fill="both", padx=10, pady=10)
    return entry
    
def frame(window, color='#4A4A4A', text='', height=30, size=18):
    frame = tk.Frame(window.root, bg=color, height=height)
    frame.pack(fill="x")
    frameLabel = tk.Label(frame, text=text, bg=color, fg='white', font=('Arial', size))
    frameLabel.pack()

class Window:
    def __init__(self, name):
        self.root = tk.Tk()
        self.root.title(name)
        screen_width, screen_height = self.get_screen_size()
        self.root.geometry(f"{int(screen_width * 1)}x{int(screen_height * 1)}")
        self.root.configure(bg='#F5F5F5')
            
    def get_screen_size(self):
        self.root.update_idletasks()  
        width = self.root.winfo_screenwidth()  
        height = self.root.winfo_screenheight()  
        return width, height

class LoginWindow(Window):
    def __init__(self, name):
        super().__init__(name)
        self.login()

    def login(self):
        self.header = frame(self, text="Bienvenido a la Biblioteca Digital", height=50)
        self.labelCorreo = labelCreator(self.root, "Correo electronico")
        self.correo = entryCreator(self.root)
        self.labelContrasena = labelCreator(self.root, "Contraseña")
        self.contrasena = entryCreator(self.root, show=False)
        self.button = buttonCreator(self.root, "Iniciar Sesión", lambda: logear(self.correo, self.label_saludo, self.contrasena))
        self.button = buttonCreator(self.root, "Crear Cuenta", self.abrir_crear_cuenta)
        self.label_saludo = labelCreator(self.root, "")
        self.footer = frame(self, text="© 2024 Biblioteca Digital", size=10)

    def abrir_crear_cuenta(self):
        self.root.destroy()
        WindowCrearCuenta("Crear Cuenta")

class WindowCrearCuenta(Window):
    def __init__(self, name):
        super().__init__(name)
        self.header = frame(self, text="Registro a e-Book", height=50)
        self.mainFrame = tk.Frame(self.root)
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
        self.labelCorreo = labelCreator(self.controlFrame, text="Correo electronico")
        self.labelCorreo.config(highlightthickness=0)
        self.labelCorreo.configure(pady=3)
        self.correo = entryCreator(self.controlFrame)
        self.correo.config(highlightthickness=0)
        self.labelContrasena = labelCreator(self.controlFrame, text="Contraseña")
        self.contrasena = entryCreator(self.controlFrame, show=False)
        self.button = buttonCreator(self.controlFrame, "Registrar", lambda: registrar(self.correo, self.labelSaludo, self.contrasena))
        self.button = buttonCreator(self.controlFrame, "Regresar a Login", self.regresar_login)
    
        self.labelSaludo1 = labelCreator(self.controlFrame, "")

        self.footer = frame(self, text="© 2024 e-Book by Trickster 09", size=10)

    def regresar_login(self):
        self.root.destroy()
        LoginWindow("Login")

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
        if not self.transitioning:
            self.canvas.move("image", 0, -self.speed)
            self.checkPosition()

        self.root.after(30, self.moveImages)

    def checkPosition(self):
        canvasHeight = self.canvas.winfo_height()
        for imageObject in self.imageObjects:
            coords = self.canvas.coords(imageObject)
            if coords[1] + self.imageTk[self.currentImageIndex].height() <= canvasHeight:
                self.startTransition()

    def startTransition(self):
        self.transitioning = True
        self.fadeOut(255)

    def fadeOut(self, alpha):
        if alpha > 0:
            self.overlay.config(bg=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(30, self.fadeOut, alpha - 10)
        else:
            self.transportImage()

    def transportImage(self):
        self.canvas.delete("image")
        self.imageObjects.clear()
        self.imageY = 0

        self.currentImageIndex = (self.currentImageIndex + 1) % len(self.images)
        self.addImages()

        self.fadeIn(0)

    def fadeIn(self, alpha):
        if alpha < 255:
            self.overlay.lift()
            self.overlay.config(bg=f'#{alpha:02x}{alpha:02x}{alpha:02x}')
            self.root.after(30, self.fadeIn, alpha + 10)
        else:
            self.overlay.lower()
            self.transitioning = False

if __name__ == "__main__":
    app = LoginWindow("Login")
    app.root.mainloop()

import csv

# Datos de libros
libros = [
    ['Titulo', 'Autor', 'Ano', 'Genero'],
    ['Fundación', 'Isaac Asimov', 1968, 'Ciencia Ficción'],
    ['1984', 'George Orwell', 1949, 'Distopía'],
    ['Cien años de soledad', 'Gabriel García Márquez', 1967, 'Realismo Mágico'],
    ['El Hobbit', 'J.R.R. Tolkien', 1937, 'Fantasía'],
    ['Don Quijote de la Mancha', 'Miguel de Cervantes', 1605, 'Novela'],
    ['Crimen y castigo', 'Fyodor Dostoevsky', 1866, 'Ficción psicológica'],
    ['Matar a un ruiseñor', 'Harper Lee', 1960, 'Ficción'],
    ['Orgullo y prejuicio', 'Jane Austen', 1813, 'Novela romántica'],
    ['El gran Gatsby', 'F. Scott Fitzgerald', 1925, 'Ficción'],
    ['La Odisea', 'Homero', -800, 'Épica'],
    ['El nombre de la rosa', 'Umberto Eco', 1980, 'Misterio'],
    ['Los pilares de la tierra', 'Ken Follett', 1989, 'Ficción histórica'],
    ['La sombra del viento', 'Carlos Ruiz Zafón', 2001, 'Misterio'],
    ['El código Da Vinci', 'Dan Brown', 2003, 'Thriller'],
    ['Juego de Tronos', 'George R.R. Martin', 1996, 'Fantasía'],
    ['El señor de los anillos', 'J.R.R. Tolkien', 1954, 'Fantasía'],
    ['Harry Potter y la piedra filosofal', 'J.K. Rowling', 1997, 'Fantasía'],
    ['El alquimista', 'Paulo Coelho', 1988, 'Ficción'],
    ['Cumbres borrascosas', 'Emily Brontë', 1847, 'Novela gótica'],
    ['Las aventuras de Sherlock Holmes', 'Arthur Conan Doyle', 1892, 'Misterio'],
    ['Drácula', 'Bram Stoker', 1897, 'Terror'],
    ['Frankenstein', 'Mary Shelley', 1818, 'Terror'],
    ['La divina comedia', 'Dante Alighieri', 1320, 'Épica'],
    ['Ulises', 'James Joyce', 1922, 'Modernismo'],
    ['Moby Dick', 'Herman Melville', 1851, 'Aventura'],
    ['La isla del tesoro', 'Robert Louis Stevenson', 1883, 'Aventura'],
    ['La metamorfosis', 'Franz Kafka', 1915, 'Ficción'],
    ['Los miserables', 'Victor Hugo', 1862, 'Ficción'],
    ['Anna Karenina', 'Leo Tolstoy', 1877, 'Ficción'],
    ['Lolita', 'Vladimir Nabokov', 1955, 'Ficción']
]

# Ruta del archivo CSV
ruta_csv = 'libros.csv'

# Crear y escribir datos en el archivo CSV
with open(ruta_csv, 'w', newline='') as archivo:
    escritor_csv = csv.writer(archivo)
    escritor_csv.writerows(libros)

print(f"Archivo '{ruta_csv}' creado con éxito.")

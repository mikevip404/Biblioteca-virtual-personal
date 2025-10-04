import json
from libro import Libro

class BibliotecaDB:
    def __init__(self, archivo="libros.json"):
        self.archivo = archivo
        self.libros = self.cargar()

    def cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Libro(**lib) for lib in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([libro.to_dict() for libro in self.libros], f, indent=4, ensure_ascii=False)

    def agregar(self, libro):
        self.libros.append(libro)
        self.guardar()

    def eliminar(self, titulo):
        self.libros = [lib for lib in self.libros if lib.titulo != titulo]
        self.guardar()

    def editar(self, titulo, nuevos_datos):
        for libro in self.libros:
            if libro.titulo == titulo:
                libro.autor = nuevos_datos.get("autor", libro.autor)
                libro.genero = nuevos_datos.get("genero", libro.genero)
                libro.anio = nuevos_datos.get("anio", libro.anio)
                libro.estado = nuevos_datos.get("estado", libro.estado)
        self.guardar()

    def contar(self):
        leidos = sum(1 for lib in self.libros if lib.estado == "leído")
        pendientes = sum(1 for lib in self.libros if lib.estado == "pendiente")
        return leidos, pendientes

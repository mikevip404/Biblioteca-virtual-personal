class Libro:
    def __init__(self, titulo, autor, genero, anio, estado="pendiente"):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.anio = self.validar_anio(anio)
        self.estado = estado  # "leído" o "pendiente"

    def validar_anio(self, anio):
        try:
            anio = int(anio)
            if 0 < anio <= 2100:
                return anio
            else:
                raise ValueError("Año inválido")
        except ValueError:
            raise ValueError("El año debe ser un número válido")

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "genero": self.genero,
            "anio": self.anio,
            "estado": self.estado
        }

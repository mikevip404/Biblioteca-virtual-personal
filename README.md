# Biblioteca Virtual Personal

Este proyecto corresponde al curso de programación y consiste en el desarrollo de una aplicación en **Python** para la gestión de libros personales.  
El sistema permite registrar, organizar, consultar y eliminar libros, facilitando el control de hábitos de lectura y asegurando la persistencia de los datos.

---

## Características principales

- Registro de libros con:
  - Título
  - Autor
  - Género
  - Año de publicación
  - Estado de lectura (📘 leído / 📗 pendiente)
- Modificación y eliminación de registros existentes.
- Visualización del catálogo en forma de tabla con **filtros por género o estado**.
- Contador de libros leídos y pendientes.
- Persistencia de datos mediante archivos **JSON** (opcionalmente CSV).
- Interfaz gráfica construida con **Tkinter**.

---

## Tecnologías utilizadas

- [Python 3.10+](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – Interfaz gráfica
- [JSON](https://www.json.org/json-es.html) – Persistencia de datos
- [CSV](https://docs.python.org/3/library/csv.html) – Persistencia alternativa
- [datetime](https://docs.python.org/3/library/datetime.html) – Manejo de fechas (opcional)

---

## Estructura del proyecto

```bash
Biblioteca/
│── app.py          # Punto de entrada principal
│── interfaz.py     # Clase BibliotecaApp (interfaz gráfica con Tkinter)
│── basedatos.py    # Clase BibliotecaDB (persistencia en JSON/CSV)
│── libro.py        # Clase Libro (atributos y validaciones)
│── libros.json     # Archivo generado automáticamente con los registros

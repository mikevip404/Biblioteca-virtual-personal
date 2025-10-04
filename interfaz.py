import tkinter as tk
from tkinter import messagebox, ttk
from baseDatos import BibliotecaDB
from libro import Libro

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Biblioteca Virtual Personal")
        self.root.geometry("850x550")
        self.root.configure(bg="#ecf0f1")

        # ------------------ Estilos Modernos ------------------ #
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo para Treeview
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#2c3e50",
                        rowheight=28,
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#3498db",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))
        style.map("Treeview",
                  background=[("selected", "#2980b9")])

        # Estilo para botones
        style.configure("TButton",
                        font=("Segoe UI", 10, "bold"),
                        padding=8,
                        background="#3498db",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#2980b9")])

        style.configure("TLabel",
                        background="#ecf0f1",
                        font=("Segoe UI", 11))

        # ------------------ Base de datos ------------------ #
        self.db = BibliotecaDB()

        # ------------------ Título ------------------ #
        title = tk.Label(root, text="Mi Biblioteca Virtual 📖",
                         font=("Segoe UI", 18, "bold"),
                         bg="#ecf0f1", fg="#2c3e50")
        title.pack(pady=15)

        # ------------------ Barra de búsqueda ------------------ #
        search_frame = tk.Frame(root, bg="#ecf0f1")
        search_frame.pack(fill="x", pady=10)

        self.genero_filtro = tk.Entry(search_frame, width=65, font=("Segoe UI", 10))
        self.genero_filtro.insert(0, "🔍 Buscar por género...")
        self.genero_filtro.pack(side="left", padx=5, ipady=4)

        self.estado_filtro = ttk.Combobox(search_frame, values=["", "leído", "pendiente"], width=15)
        self.estado_filtro.set("Filtrar por estado")
        self.estado_filtro.pack(side="left", padx=5, ipady=2)

        ttk.Button(search_frame, text="Aplicar Filtro", command=self.filtrar).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Limpiar", command=self.cargar_tabla).pack(side="left", padx=5)

        # ------------------ Tabla ------------------ #
        self.tree = ttk.Treeview(root,
                                 columns=("Título", "Autor", "Género", "Año", "Estado"),
                                 show="headings",
                                 height=14)
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Año", text="Año")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill="both", padx=15, pady=10, expand=True)

        # Scroll
        scroll = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # ------------------ Botones ------------------ #
        btn_frame = tk.Frame(root, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Agregar", command=self.agregar).grid(row=0, column=0, padx=12)
        ttk.Button(btn_frame, text="✏️ Editar", command=self.editar).grid(row=0, column=1, padx=12)
        ttk.Button(btn_frame, text="🗑️ Eliminar", command=self.eliminar).grid(row=0, column=2, padx=12)
        ttk.Button(btn_frame, text="📊 Contar", command=self.mostrar_contador).grid(row=0, column=3, padx=12)

        self.cargar_tabla()

    # ------------------ Métodos ------------------ #
    def cargar_tabla(self, libros=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if libros is None:
            libros = self.db.libros
        for libro in libros:
            self.tree.insert("", "end", values=(libro.titulo, libro.autor, libro.genero, libro.anio, libro.estado))

    def agregar(self):
        self.formulario_libro("Agregar Libro")

    def editar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un libro para editar")
            return
        valores = self.tree.item(seleccionado, "values")
        titulo_original = valores[0]
        libro = next((l for l in self.db.libros if l.titulo == titulo_original), None)
        if libro:
            self.formulario_libro("Editar Libro", libro, titulo_original)

    def formulario_libro(self, titulo, libro=None, titulo_original=None):
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.configure(bg="#ecf0f1")

        campos = {
            "Título": tk.StringVar(value=libro.titulo if libro else ""),
            "Autor": tk.StringVar(value=libro.autor if libro else ""),
            "Género": tk.StringVar(value=libro.genero if libro else ""),
            "Año": tk.StringVar(value=libro.anio if libro else ""),
            "Estado": tk.StringVar(value=libro.estado if libro else "pendiente"),
        }

        for i, (campo, var) in enumerate(campos.items()):
            tk.Label(win, text=campo, bg="#ecf0f1").grid(row=i, column=0, padx=10, pady=6, sticky="e")
            if campo == "Estado":
                combo = ttk.Combobox(win, textvariable=var, values=["leído", "pendiente"])
                combo.grid(row=i, column=1, padx=10, pady=6)
            else:
                tk.Entry(win, textvariable=var, font=("Segoe UI", 10)).grid(row=i, column=1, padx=10, pady=6)

        def guardar():
            try:
                nuevo_libro = Libro(
                    campos["Título"].get(),
                    campos["Autor"].get(),
                    campos["Género"].get(),
                    campos["Año"].get(),
                    campos["Estado"].get()
                )
                if titulo.startswith("Agregar"):
                    self.db.agregar(nuevo_libro)
                else:
                    self.db.editar(titulo_original, nuevo_libro.to_dict())
                self.cargar_tabla()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Guardar ✅", command=guardar).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def eliminar(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un libro para eliminar")
            return
        valores = self.tree.item(seleccionado, "values")
        titulo = valores[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Seguro que deseas eliminar '{titulo}'?")
        if confirm:
            self.db.eliminar(titulo)
            self.cargar_tabla()

    def mostrar_contador(self):
        leidos, pendientes = self.db.contar()
        messagebox.showinfo("📊 Contador", f"📘 Leídos: {leidos}\n📗 Pendientes: {pendientes}")

    def filtrar(self):
        genero = self.genero_filtro.get().lower()
        estado = self.estado_filtro.get().lower()
        filtrados = [lib for lib in self.db.libros if
                     (genero in lib.genero.lower() if genero else True) and
                     (lib.estado.lower() == estado if estado else True)]
        self.cargar_tabla(filtrados)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

DB_NAME = "usuarios.db"


# ---------------- CLASE DE BASE DE DATOS ----------------
class UsuarioDB:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn

    @staticmethod
    def registrar(usuario, contrasena):
        with UsuarioDB._conn() as conn:
            try:
                conn.execute("INSERT INTO usuarios (nombre, contrasena) VALUES (?, ?)", (usuario, contrasena))
                return True
            except sqlite3.IntegrityError:
                return False  # Usuario duplicado

    @staticmethod
    def validar(usuario, contrasena):
        with UsuarioDB._conn() as conn:
            cur = conn.execute("SELECT * FROM usuarios WHERE nombre=? AND contrasena=?", (usuario, contrasena))
            return cur.fetchone() is not None


# ---------------- INTERFAZ GRÁFICA ----------------
ventana = tk.Tk()
ventana.title("TicketManager - Login")
ventana.geometry("400x350")
ventana.configure(bg="#0f3b53")
ventana.resizable(False, False)


def RegistrarUsuarios():
    Usuario = UsuarioNuevo.get().strip()
    Contraseña = ContrNueva.get().strip()

    if not Usuario or not Contraseña:
        messagebox.showwarning("Advertencia", "Completa todos los campos")
        return

    if UsuarioDB.registrar(Usuario, Contraseña):
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
        VentanaRegistro.destroy()
    else:
        messagebox.showerror("Error", "El usuario ya existe, inténtelo de nuevo.")


def AbrirRegistro():
    global VentanaRegistro, UsuarioNuevo, ContrNueva

    VentanaRegistro = tk.Toplevel()
    VentanaRegistro.title("Registrar usuario")
    VentanaRegistro.geometry("300x200")
    VentanaRegistro.configure(bg="#0f3b53")

    tk.Label(VentanaRegistro, text="Nuevo Usuario:", fg="white", bg="#0f3b53").pack(pady=5)
    UsuarioNuevo = tk.Entry(VentanaRegistro, bg="#00b4c6", fg="white", justify="center", relief="flat")
    UsuarioNuevo.pack(pady=5, ipady=5, ipadx=10)

    tk.Label(VentanaRegistro, text="Nueva contraseña:", fg="white", bg="#0f3b53").pack(pady=5)
    ContrNueva = tk.Entry(VentanaRegistro, show="*", bg="#00b4c6", fg="white", justify="center", relief="flat")
    ContrNueva.pack(pady=5, ipady=5, ipadx=10)

    tk.Button(
        VentanaRegistro, text="Registrar",
        bg="#00b4c6", fg="white", relief="flat",
        activebackground="#00a0b3", cursor="hand2",
        command=RegistrarUsuarios
    ).pack(pady=10)


def ValidarLogin():
    Usuario = UsuarioLogin.get().strip()
    Contraseña = ContrLogin.get().strip()

    if not Usuario or not Contraseña:
        messagebox.showwarning("Advertencia", "Completa todos los campos")
        return

    if UsuarioDB.validar(Usuario, Contraseña):
        messagebox.showinfo("Bienvenido", f"Hola {Usuario}")
        ventana.destroy()
        AbrirMenuPrincipal(Usuario)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


def AbrirMenuPrincipal(Usuario):
    menu = tk.Tk()
    menu.title("Panel de Control - TicketManager")
    menu.geometry("900x500")
    menu.configure(bg="#e9f1f5")

    '''----- MENÚ IZQUIERDO -----'''
    MenuLateral = tk.Frame(menu, bg="#0f3b53", width=200)
    MenuLateral.pack(side="left", fill="y")

    Opciones = ["Tickets", "Técnicos", "Empleados", "Categorías", "Reportes"]
    for texto in Opciones:
        tk.Button(
            MenuLateral,
            text=texto,
            bg="#0f3b53",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            activebackground="#1f5973",
            cursor="hand2"
        ).pack(fill="x", pady=5, ipady=8)

    '''----- BOTÓN CERRAR SESIÓN -----'''
    tk.Button(
        MenuLateral,
        text="Cerrar sesión",
        bg="#d9534f",
        fg="white",
        relief="flat",
        cursor="hand2",
        font=("Arial", 11, "bold"),
        command=menu.destroy
    ).pack(side="bottom", fill="x", pady=10, ipady=8)

    '''----- PANEL DERECHO -----'''
    Panel = tk.Frame(menu, bg="white")
    Panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tk.Label(
        Panel,
        text="Control de Tickets",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#0f3b53"
    ).pack(anchor="w", pady=(10, 15), padx=10)

    ''' ----- FILTROS Y BOTÓN NUEVO -----'''
    Top = tk.Frame(Panel, bg="white")
    Top.pack(fill="x", padx=10)

    tk.Button(
        Top,
        text="Nuevo Ticket",
        bg="#00b4c6",
        fg="white",
        relief="flat",
        cursor="hand2",
        font=("Arial", 11, "bold")
    ).pack(side="left", padx=10)

    Filtros = ["Estado", "Técnico", "Categoría", "Fecha"]
    for f in Filtros:
        combo = ttk.Combobox(Top, values=["Todos"], state="readonly", width=15)
        combo.set(f)
        combo.pack(side="left", padx=5)

    ''' ----- TABLA DE TICKETS -----'''
    Tablat = tk.Frame(Panel, bg="white")
    Tablat.pack(fill="both", expand=True, padx=10, pady=10)

    Columnas = ("ID", "Título", "Estado", "Técnico", "Fecha", "Prioridad")
    Tabla = ttk.Treeview(Tablat, columns=Columnas, show="headings", height=10)
    for col in Columnas:
        Tabla.heading(col, text=col)
        Tabla.column(col, width=120, anchor="center")

    ''' ----- DATOS DE EJEMPLO -----'''
    datos = [
        (10, "Post. Jerter", "Open", "Juan Pérez", "19 Mar", "Alta"),
        (20, "Repare rgn", "Open", "María Lopez", "29 Mar", "Media"),
        (30, "Mart rgn", "Media", "Pedro Gonzalez", "19 Mar", "Baja"),
        (40, "Mantenimiento", "Baja", "Sergio Mertra", "19 Abr", "Baja")
    ]
    for fila in datos:
        Tabla.insert("", "end", values=fila)

    Tabla.pack(fill="both", expand=True)

    '''' ----- BOTONES DE ACCIÓN -----'''
    Botones = tk.Frame(Panel, bg="white")
    Botones.pack(pady=5)

    tk.Button(Botones, text="Editar", bg="#00b4c6", fg="white", width=12, relief="flat").pack(side="left", padx=10)
    tk.Button(Botones, text="Eliminar", bg="#d9534f", fg="white", width=12, relief="flat").pack(side="left", padx=10)
    tk.Button(Botones, text="Cambiar técnico", bg="#5cb85c", fg="white", width=15, relief="flat").pack(side="left", padx=10)

    menu.mainloop()


'''Interfaz Login'''
tk.Label(
    ventana,
    text="TicketManager",
    bg="#0f3b53",
    fg="white",
    font=("Arial", 22, "bold")
).pack(pady=30)

tk.Label(ventana, text="Usuario:", bg="#0f3b53", fg="white", font=("Arial", 10, "bold")).pack()
UsuarioLogin = tk.Entry(ventana, bg="#00b4c6", fg="white", justify="center", relief="flat", font=("Arial", 10))
UsuarioLogin.pack(pady=5, ipady=5, ipadx=10)

tk.Label(ventana, text="Contraseña:", bg="#0f3b53", fg="white", font=("Arial", 10, "bold")).pack()
ContrLogin = tk.Entry(ventana, show="*", bg="#00b4c6", fg="white", justify="center", relief="flat", font=("Arial", 10))
ContrLogin.pack(pady=5, ipady=5, ipadx=10)

tk.Button(
    ventana,
    text="Iniciar Sesión",
    bg="#00b4c6",
    fg="white",
    relief="flat",
    font=("Arial", 11, "bold"),
    activebackground="#00a0b3",
    cursor="hand2",
    command=ValidarLogin
).pack(pady=20)

tk.Button(
    ventana,
    text="Registrarse",
    bg="#0f3b53",
    fg="#00b4c6",
    relief="flat",
    font=("Arial", 10, "underline"),
    cursor="hand2",
    command=AbrirRegistro
).pack()

ventana.mainloop()
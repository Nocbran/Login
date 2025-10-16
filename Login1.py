import tkinter as tk
from tkinter import messagebox
import os

ventana = tk.Tk()
ventana.title("TicketManager - Login")
ventana.geometry("400x350")
ventana.configure(bg="#0f3b53")
ventana.resizable(False, False)

ArchivoDeUsuarios = "usuarios.txt"


def RegistrarUsuarios():
    Usuario = UsuarioNuevo.get().strip()
    Contraseña = ContrNueva.get().strip()

    if not os.path.exists(ArchivoDeUsuarios):
        with open(ArchivoDeUsuarios, "w") as f:
            pass

    if not Usuario or not Contraseña:
        messagebox.showwarning("Advertencia", "Completa todos los campos")
        return

    with open(ArchivoDeUsuarios, "r") as f:
        for linea in f:
            if not linea.strip():
                continue
            user, _ = linea.strip().split(",")
            if user == Usuario:
                messagebox.showerror("Error", "El usuario ya existe, inténtelo de nuevo.")
                return

    with open(ArchivoDeUsuarios, "a") as f:
        f.write(f"{Usuario},{Contraseña}\n")

    messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    VentanaRegistro.destroy()


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

    if not os.path.exists(ArchivoDeUsuarios):
        messagebox.showerror("Error", "No hay usuarios registrados aún.")
        return

    with open(ArchivoDeUsuarios, "r") as f:
        for linea in f:
            if not linea.strip():
                continue
            user, passw = linea.strip().split(",")
            if user == Usuario and passw == Contraseña:
                messagebox.showinfo("Bienvenido", f"Hola {Usuario}")
                ventana.destroy()
                AbrirMenuPrincipal(Usuario)
                return

    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


def AbrirMenuPrincipal(Usuario):
    menu = tk.Tk()
    menu.title("Menú Principal")
    menu.geometry("300x200")
    menu.configure(bg="#0f3b53")
    tk.Label(menu, text=f"Bienvenido, {Usuario}", font=("Arial", 14), bg="#0f3b53", fg="white").pack(pady=40)
    tk.Button(menu, text="Salir", bg="#00b4c6", fg="white", relief="flat", command=menu.destroy).pack(pady=10)
    menu.mainloop()


# ---------- INTERFAZ LOGIN ----------
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
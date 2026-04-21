import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from Variables import USUARIOS
from datetime import datetime

from MaxtimeBot import automatizar_maxtime 


class MaxTimeUI:

    COLOR_BG      = "#f4f6f8"
    COLOR_ACCENT  = "#8bc34a"
    COLOR_TEXT    = "#2c2c2c"
    COLOR_MUTED   = "#757575"
    COLOR_BORDER  = "#e0e0e0"

    def __init__(self, root):
        self.root = root
        self.root.title("MaxTime UI")
        self.root.geometry("680x720")
        self.root.configure(bg=self.COLOR_BG)

        self.usuario_default, self.pass_default = self._get_default_user()

        self._build_ui()

    # ─────────────────────────────────────────────
    def _get_default_user(self):
        if USUARIOS:
            usuario = list(USUARIOS.keys())[0]
            return usuario, USUARIOS[usuario]
        return "", ""

    # ─────────────────────────────────────────────
    def _build_ui(self):

        container = tk.Frame(self.root, bg=self.COLOR_BG)
        container.pack(fill="both", expand=True)

        self.card = tk.Frame(container, bg="white")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=600, height=680)
        self.card.configure(highlightbackground=self.COLOR_BORDER, highlightthickness=1)

        # ── Título
        tk.Label(
            self.card,
            text="Crear registro de tiempo",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#7cb342"
        ).pack(pady=(18, 10))

        content = tk.Frame(self.card, bg="white")
        content.pack(fill="both", expand=True, padx=20)

        # ── Credenciales
        self._section(content, "Credenciales")

        self.entry_usuario = self._input(content, "Usuario")
        self.entry_usuario.insert(0, self.usuario_default)

        # ── Contraseña con toggle 👁
        pass_frame = tk.Frame(content, bg="white")
        pass_frame.pack(fill="x", pady=5)

        tk.Label(
            pass_frame,
            text="Contraseña",
            bg="white",
            fg=self.COLOR_MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        inner = tk.Frame(pass_frame, bg="white")
        inner.pack(fill="x")

        self.entry_pass = tk.Entry(
            inner,
            show="●",
            font=("Segoe UI", 11),
            relief="flat"
        )
        self.entry_pass.insert(0, self.pass_default)
        self.entry_pass.configure(
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
            highlightcolor=self.COLOR_ACCENT
        )
        self.entry_pass.pack(side="left", fill="x", expand=True)

        self.show_pass = False
        tk.Button(
            inner,
            text="Mostrar contraseña",
            bg="white",
            relief="flat",
            cursor="hand2",
            command=self._toggle_password
        ).pack(side="right", padx=5)

        # ── Comentario
        self._section(content, "Comentario")

        self.txt_comentario = scrolledtext.ScrolledText(
            content,
            height=4,
            wrap="word",
            bg="white",
            fg="#333",
            font=("Segoe UI", 10),
            relief="flat"
        )
        self.txt_comentario.configure(
            highlightthickness=1,
            highlightbackground="#000000"
        )
        self.txt_comentario.pack(fill="x", pady=8)

        # ── Botones
        footer = tk.Frame(self.card, bg="white")
        footer.pack(fill="x", padx=20, pady=(5, 10))

        tk.Button(
            footer,
            text="CANCELAR",
            bg="white",
            fg="#555",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.root.quit
        ).pack(side="right", padx=5)

        self.btn_guardar = tk.Button(
            footer,
            text="GUARDAR",
            bg=self.COLOR_ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self._ejecutar
        )
        self.btn_guardar.pack(side="right")

        # ── LOG (🔥 LO IMPORTANTE QUE FALTABA)
        self._section(content, "Log de ejecución")

        self.txt_log = scrolledtext.ScrolledText(
            content,
            height=10,
            width=10,
            bg="#111",
            fg="#00ff88",
            font=("Consolas", 9),
            state="disabled"
        )
        self.txt_log.pack(fill="x", pady=5)

    # ─────────────────────────────────────────────
    def _toggle_password(self):
        self.show_pass = not self.show_pass
        self.entry_pass.config(show="" if self.show_pass else "●")

    # ─────────────────────────────────────────────
    def _log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.root.after(0, self._log_ui, f"[{timestamp}] {msg}")

    def _log_ui(self, msg):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    # ─────────────────────────────────────────────
    def _ejecutar(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_pass.get().strip()
        comentario = self.txt_comentario.get("1.0", "end-1c").strip()

        if not usuario or not password:
            messagebox.showwarning("Campos requeridos", "Completa usuario y contraseña")
            return
        
        if not comentario:
            messagebox.showwarning("Campo requerido", "Debes ingresar un comentario")
            return

        # limpiar log
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")

        self._log(f"Iniciando proceso para {usuario}")
        hora_actual = datetime.now().hour

        if hora_actual < 13:
            horas = 4.5
            jornada = "mañana"
        else:
            horas = 4.0
            jornada = "tarde"

        self._log(f"Ejecutando jornada de {jornada} ({horas}h)")

        self.btn_guardar.config(state="disabled", text="Ejecutando...")

        def done(success, error=""):
            self.root.after(0, self._fin_proceso, success, error)

        hilo = threading.Thread(
            target=automatizar_maxtime,
            args=(usuario, password, comentario, horas, self._log, done),
            daemon=True
        )
        hilo.start()

    def _fin_proceso(self, success, error):
        self.btn_guardar.config(state="normal", text="GUARDAR")

        if success:
            messagebox.showinfo("Éxito", "Registro completado correctamente")
        else:
            messagebox.showerror("Error", error)

    # ─────────────────────────────────────────────
    def _section(self, parent, titulo):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=(12, 4))

        tk.Label(
            frame,
            text=titulo,
            bg="white",
            fg="#4caf50",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        tk.Frame(frame, bg="#8bc34a", height=2).pack(fill="x", pady=(3, 0))

    # ─────────────────────────────────────────────
    def _input(self, parent, label):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=5)

        tk.Label(
            frame,
            text=label,
            bg="white",
            fg=self.COLOR_MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        entry = tk.Entry(frame, font=("Segoe UI", 11), relief="flat")
        entry.configure(
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
            highlightcolor=self.COLOR_ACCENT
        )
        entry.pack(fill="x", pady=3)

        return entry


# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = MaxTimeUI(root)
    root.mainloop()
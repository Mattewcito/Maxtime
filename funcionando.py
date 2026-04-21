"""
MaxTime Automation Bot
Automatiza el registro de entrada/salida en maxtime.choucairtesting.com
Requiere: pip install selenium webdriver-manager
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime

# ─────────────────────────────────────────────
# Selenium imports (se validan al ejecutar)
# ─────────────────────────────────────────────
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_OK = True
except ImportError:
    SELENIUM_OK = False


# ══════════════════════════════════════════════
#  CREDENCIALES PREDEFINIDAS (editables)
# ══════════════════════════════════════════════
USUARIOS_PREDEFINIDOS = {
    "elopezp": "123",
    # Agrega más compañeros aquí:
    # "jperezm": "456",
    # "amartinez": "789",
}

URL_MAXTIME = "https://maxtime.choucairtesting.com"


# ══════════════════════════════════════════════
#  LÓGICA DE AUTOMATIZACIÓN
# ══════════════════════════════════════════════
def automatizar_maxtime(usuario, contrasena, accion, comentario, log_fn, done_fn):
    """
    Corre en hilo separado.
    accion: "entrada" | "salida"
    log_fn: callback para escribir en el log de la UI
    done_fn: callback al terminar (éxito/error)
    """
    def log(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_fn(f"[{timestamp}] {msg}")

    try:
        log("Iniciando Chrome...")
        options = webdriver.ChromeOptions()
        # Descomenta la siguiente línea para correr sin ventana del navegador:
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        wait = WebDriverWait(driver, 20)

        # ── 1. Abrir página ──────────────────────────────
        log(f"Abriendo {URL_MAXTIME} ...")
        driver.get(URL_MAXTIME)
        time.sleep(2)

        # ── 2. Login ─────────────────────────────────────
        log(f"Iniciando sesión como '{usuario}'...")

        # Busca campos de login (ajusta selectores si la página cambia)
        campo_usuario = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='text' or @name='username' or @id='username' or @placeholder]")
            )
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_pass = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password']")
            )
        )
        campo_pass.clear()
        campo_pass.send_keys(contrasena)

        # Botón login
        btn_login = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' or contains(text(),'Login') or contains(text(),'Ingresar') or contains(text(),'Entrar')]")
            )
        )
        btn_login.click()
        time.sleep(3)
        log("Login exitoso ✓")

        # ── 3. Navegar al módulo de tiempo ───────────────
        log("Buscando módulo de registro de tiempo...")

        # Intenta varios selectores comunes para registro de tiempo
        selectores_tiempo = [
            "//a[contains(@href,'time') or contains(@href,'registro')]",
            "//*[contains(text(),'Registro') or contains(text(),'Tiempo') or contains(text(),'Marcar')]",
            "//button[contains(text(),'Registro') or contains(text(),'Check')]",
        ]

        elemento_tiempo = None
        for selector in selectores_tiempo:
            try:
                elemento_tiempo = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                elemento_tiempo.click()
                log("Módulo de tiempo encontrado ✓")
                time.sleep(2)
                break
            except Exception:
                continue

        # ── 4. Registrar entrada o salida ────────────────
        log(f"Registrando {accion.upper()}...")

        if accion == "entrada":
            selectores_accion = [
                "//*[contains(text(),'Entrada') or contains(text(),'entrada') or contains(text(),'Check In') or contains(text(),'Inicio')]",
                "//button[contains(@class,'entrada') or contains(@id,'entrada')]",
            ]
        else:
            selectores_accion = [
                "//*[contains(text(),'Salida') or contains(text(),'salida') or contains(text(),'Check Out') or contains(text(),'Fin')]",
                "//button[contains(@class,'salida') or contains(@id,'salida')]",
            ]

        btn_accion = None
        for selector in selectores_accion:
            try:
                btn_accion = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                break
            except Exception:
                continue

        if btn_accion:
            btn_accion.click()
            time.sleep(2)
            log(f"{accion.capitalize()} marcada ✓")
        else:
            log(f"⚠ No se encontró botón de {accion}. Verifica los selectores manualmente.")

        # ── 5. Ingresar comentario ───────────────────────
        if comentario.strip():
            log("Ingresando comentario...")
            selectores_comentario = [
                "//textarea",
                "//input[@name='comentario' or @name='comment' or @name='description' or @placeholder]",
                "//*[@contenteditable='true']",
            ]
            campo_comentario = None
            for selector in selectores_comentario:
                try:
                    campo_comentario = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except Exception:
                    continue

            if campo_comentario:
                campo_comentario.clear()
                campo_comentario.send_keys(comentario)
                log("Comentario ingresado ✓")
            else:
                log("⚠ No se encontró campo de comentario.")

        # ── 6. Confirmar / Guardar ───────────────────────
        selectores_guardar = [
            "//button[@type='submit']",
            "//button[contains(text(),'Guardar') or contains(text(),'Confirmar') or contains(text(),'OK') or contains(text(),'Aceptar')]",
        ]
        for selector in selectores_guardar:
            try:
                btn_guardar = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                btn_guardar.click()
                log("Registro guardado ✓")
                time.sleep(2)
                break
            except Exception:
                continue

        log("─" * 40)
        log(f"✅ Proceso completado: {accion.upper()} registrada para '{usuario}'")
        done_fn(success=True)

    except Exception as e:
        log(f"❌ Error: {e}")
        done_fn(success=False, error=str(e))
    finally:
        try:
            time.sleep(3)
            driver.quit()
        except Exception:
            pass


# ══════════════════════════════════════════════
#  INTERFAZ GRÁFICA
# ══════════════════════════════════════════════
class MaxTimeApp:
    COLOR_PANEL   = "#e0e0e0"
    COLOR_ENTRADA = "#10b981"
    COLOR_SALIDA  = "#ef4444"
    COLOR_BG      = "#f4f6f8"
    COLOR_ACCENT  = "#8bc34a"
    COLOR_TEXT    = "#2c2c2c"
    COLOR_MUTED   = "#757575"
    COLOR_BORDER  = "#e0e0e0"

    def __init__(self, root):
        self.root = root
        self.root.title("Registro de tiempo en MaxTime")
        self.root.geometry("620x700")
        self.root.configure(bg=self.COLOR_BG)
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # ── Header ───────────────────────────────────────
        header = tk.Frame(self.root, bg=self.COLOR_ACCENT, height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Registro de tiempo en MaxTime",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLOR_ACCENT,
            fg="white",
        ).pack(pady=15)

        main = tk.Frame(self.root, bg=self.COLOR_BG, padx=24, pady=16)
        main.pack(fill="both", expand=True)

        # ── Credenciales ─────────────────────────────────
        self._section(main, "👤  Credenciales")

        cred_frame = tk.Frame(main, bg=self.COLOR_PANEL, relief="flat", bd=0)
        cred_frame.pack(fill="x", pady=(0, 12))
        cred_frame.configure(highlightbackground=self.COLOR_BORDER, highlightthickness=1)

        inner = tk.Frame(cred_frame, bg=self.COLOR_PANEL, padx=16, pady=12)
        inner.pack(fill="x")

        # Selector de usuario predefinido
        tk.Label(inner, text="Usuario predefinido:", bg=self.COLOR_PANEL,
                 fg=self.COLOR_MUTED, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")

        self.var_preset = tk.StringVar(value="Manual")
        opciones = ["Manual"] + list(USUARIOS_PREDEFINIDOS.keys())
        combo = ttk.Combobox(inner, textvariable=self.var_preset,
                             values=opciones, state="readonly", width=20)
        combo.grid(row=0, column=1, sticky="w", padx=(8, 0))
        combo.bind("<<ComboboxSelected>>", self._on_preset_change)

        # Usuario
        tk.Label(inner, text="Usuario:", bg=self.COLOR_PANEL,
                 fg=self.COLOR_MUTED, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.entry_usuario = tk.Entry(inner, width=28, bg=self.COLOR_BG,
                                      fg=self.COLOR_TEXT, insertbackground="white",
                                      relief="flat", font=("Segoe UI", 10))
        self.entry_usuario.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        self.entry_usuario.insert(0, "elopezp")

        # Contraseña
        tk.Label(inner, text="Contraseña:", bg=self.COLOR_PANEL,
                 fg=self.COLOR_MUTED, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.entry_pass = tk.Entry(inner, width=28, show="●", bg=self.COLOR_BG,
                                   fg=self.COLOR_TEXT, insertbackground="white",
                                   relief="flat", font=("Segoe UI", 10))
        self.entry_pass.grid(row=2, column=1, sticky="w", padx=(8, 0), pady=(6, 0))
        self.entry_pass.insert(0, "123")

        # Mostrar contraseña
        self.var_mostrar = tk.BooleanVar()
        tk.Checkbutton(inner, text="Mostrar contraseña", variable=self.var_mostrar,
                       bg=self.COLOR_PANEL, fg=self.COLOR_MUTED, selectcolor=self.COLOR_BG,
                       activebackground=self.COLOR_PANEL, font=("Segoe UI", 8),
                       command=self._toggle_pass).grid(row=3, column=1, sticky="w", padx=(8, 0), pady=(4, 0))

        # ── Acción ───────────────────────────────────────
        self._section(main, "🕐  Acción a registrar")

        btn_frame = tk.Frame(main, bg=self.COLOR_BG)
        btn_frame.pack(fill="x", pady=(0, 12))

        self.var_accion = tk.StringVar(value="entrada")

        self.btn_entrada = tk.Button(
            btn_frame, text="▶  ENTRADA", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_ENTRADA, fg="white", relief="flat", cursor="hand2",
            padx=20, pady=10,
            command=lambda: self._seleccionar_accion("entrada")
        )
        self.btn_entrada.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_salida = tk.Button(
            btn_frame, text="⏹  SALIDA", font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_PANEL, fg=self.COLOR_MUTED, relief="flat", cursor="hand2",
            padx=20, pady=10,
            command=lambda: self._seleccionar_accion("salida")
        )
        self.btn_salida.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # ── Comentario ───────────────────────────────────
        self._section(main, "💬  Comentario del día")

        self.txt_comentario = scrolledtext.ScrolledText(
            main, height=5, wrap="word",
            bg=self.COLOR_PANEL, fg=self.COLOR_TEXT,
            insertbackground="white", relief="flat",
            font=("Segoe UI", 10),
            padx=10, pady=8
        )
        self.txt_comentario.pack(fill="x", pady=(0, 12))
        self.txt_comentario.insert("1.0", "Ej: Desarrollo de módulo X, reunión con equipo...")

        self.txt_comentario.bind("<FocusIn>", self._limpiar_placeholder)

        # ── Botón ejecutar ───────────────────────────────
        self.btn_ejecutar = tk.Button(
            main, text="🚀  REGISTRAR AHORA",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLOR_ACCENT, fg="white",
            relief="flat", cursor="hand2",
            padx=20, pady=12,
            command=self._ejecutar
        )
        self.btn_ejecutar.pack(fill="x", pady=(0, 12))

        # ── Log ──────────────────────────────────────────
        self._section(main, "📋  Log de ejecución")

        self.txt_log = scrolledtext.ScrolledText(
            main, height=8, wrap="word",
            bg="#0f0f1a", fg="#a0e0a0",
            insertbackground="white", relief="flat",
            font=("Consolas", 9),
            padx=10, pady=8,
            state="disabled"
        )
        self.txt_log.pack(fill="x")

        # Footer
        tk.Label(
            self.root,
            text="Choucair Testing · MaxTime Automation v1.0",
            bg=self.COLOR_BG, fg=self.COLOR_BORDER,
            font=("Segoe UI", 8)
        ).pack(pady=6)

    # ── Helpers UI ───────────────────────────────────────

    def _section(self, parent, titulo):
        tk.Label(parent, text=titulo, bg=self.COLOR_BG,
                 fg=self.COLOR_MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 4))

    def _on_preset_change(self, event=None):
        preset = self.var_preset.get()
        if preset != "Manual" and preset in USUARIOS_PREDEFINIDOS:
            self.entry_usuario.delete(0, "end")
            self.entry_usuario.insert(0, preset)
            self.entry_pass.delete(0, "end")
            self.entry_pass.insert(0, USUARIOS_PREDEFINIDOS[preset])

    def _toggle_pass(self):
        self.entry_pass.config(show="" if self.var_mostrar.get() else "●")

    def _seleccionar_accion(self, accion):
        self.var_accion.set(accion)
        if accion == "entrada":
            self.btn_entrada.config(bg=self.COLOR_ENTRADA, fg="white")
            self.btn_salida.config(bg=self.COLOR_PANEL, fg=self.COLOR_MUTED)
        else:
            self.btn_salida.config(bg=self.COLOR_SALIDA, fg="white")
            self.btn_entrada.config(bg=self.COLOR_PANEL, fg=self.COLOR_MUTED)

    def _limpiar_placeholder(self, event=None):
        if self.txt_comentario.get("1.0", "end-1c").startswith("Ej:"):
            self.txt_comentario.delete("1.0", "end")

    def _log(self, msg):
        self.root.after(0, self._log_ui, msg)

    def _log_ui(self, msg):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _set_ui_running(self, running: bool):
        state = "disabled" if running else "normal"
        self.btn_ejecutar.config(
            state=state,
            text="⏳  Ejecutando..." if running else "🚀  REGISTRAR AHORA",
            bg="#4a1a9e" if running else self.COLOR_ACCENT
        )

    def _ejecutar(self):
        if not SELENIUM_OK:
            messagebox.showerror(
                "Dependencias faltantes",
                "Instala las dependencias primero:\n\npip install selenium webdriver-manager"
            )
            return

        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_pass.get().strip()
        accion = self.var_accion.get()
        comentario = self.txt_comentario.get("1.0", "end-1c").strip()

        if comentario.startswith("Ej:"):
            comentario = ""

        if not usuario or not contrasena:
            messagebox.showwarning("Campos requeridos", "Ingresa usuario y contraseña.")
            return

        # Limpiar log
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")

        self._log(f"Usuario: {usuario} | Acción: {accion.upper()}")
        self._log("─" * 40)
        self._set_ui_running(True)

        def done(success, error=""):
            self.root.after(0, self._set_ui_running, False)
            if success:
                self.root.after(0, messagebox.showinfo, "✅ Éxito",
                                f"{accion.capitalize()} registrada correctamente para '{usuario}'.")
            else:
                self.root.after(0, messagebox.showerror, "❌ Error",
                                f"Ocurrió un error:\n{error}\n\nRevisa el log para más detalles.")

        hilo = threading.Thread(
            target=automatizar_maxtime,
            args=(usuario, contrasena, accion, comentario, self._log, done),
            daemon=True
        )
        hilo.start()


# ══════════════════════════════════════════════
#  PUNTO DE ENTRADA
# ══════════════════════════════════════════════
if __name__ == "__main__":
    if not SELENIUM_OK:
        print("=" * 50)
        print("ERROR: Faltan dependencias. Ejecuta:")
        print("  pip install selenium webdriver-manager")
        print("=" * 50)

    root = tk.Tk()
    app = MaxTimeApp(root)
    root.mainloop()
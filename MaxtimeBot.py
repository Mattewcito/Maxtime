import time
from datetime import datetime
from Variables import URL_MAXTIME
import locale
from datetime import datetime


# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Variables import PROYECTO, TIPO_HORA,HORA_INICIO, SERVICIO, ACTIVIDAD
from selenium.webdriver.common.keys import Keys

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # En Windows puede variar

def automatizar_maxtime(usuario, contrasena, comentario, horas, log_fn, done_fn):

    def log(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_fn(f"[{timestamp}] {msg}")

    driver = None

    try:
        log("Iniciando Chrome...")

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.maximize_window()

        wait = WebDriverWait(driver, 20)

        # ── 1. Abrir página
        log(f"Abriendo {URL_MAXTIME}")
        driver.get(URL_MAXTIME)
        time.sleep(2)

        # ── 2. Login
        log(f"Usuario: {usuario}")

        campo_usuario = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='text' or @name='username' or @id='username']")
            )
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_pass = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        campo_pass.clear()
        campo_pass.send_keys(contrasena)

        #botón Ingresar
        btn_login = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Login') or contains(text(),'Ingresar') or contains(text(),'Entrar')]")
            )
        )
        btn_login.click()

        time.sleep(3)
        log("Inicio de sesión exitoso")

        hoy = datetime.now().strftime("%A, %d de %B de %Y").lower()

        # ── 3. Buscando donde registrar el tiempo
        log("Buscando donde registrar el tiempo...")

        # ── 4. Buscar fila del día actual
        log("Buscando registro del día actual...")

        hoy = datetime.now().strftime("%A, %d de %B de %Y").lower()
        log(f"Fecha buscada: {hoy}")

        # Esperar que la tabla cargue
        wait.until(EC.presence_of_element_located((By.XPATH, "//tr")))

        # Buscar el TD que contiene la fecha
        celda_fecha = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//td[contains(text(), '{hoy}')]")
            )
        )

        # Subir al TR (fila completa)
        fila = celda_fecha.find_element(By.XPATH, "./ancestor::tr")

        log("Fila del día encontrada ✓")

        # 🔥 Buscar botón dentro de esa fila (el de agregar)
        try:
            boton = fila.find_element(
                By.XPATH,
                ".//button[contains(@aria-label,'Agregar')]"
            )
            boton.click()
            log("Botón de registro clickeado ✓")
        except:
            log("No se encontró botón dentro de la fila")

        log("Llenando formulario")

        #Llenar formulario

        #Campo proyecto
        campo_proyecto = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='Proyecto']")))
        campo_proyecto.click()
        time.sleep(1)
        campo_proyecto.clear()
        campo_proyecto.send_keys(PROYECTO)
        time.sleep(1)
        campo_proyecto.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)

        campo_proyecto.send_keys(Keys.ENTER)

        log(f"Proyecto seleccionado: {PROYECTO}")

        #Campo tipo hora
        tipo_hora = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='TipoHora']/preceding-sibling::div"))
        )
        tipo_hora.click()
        time.sleep(1)

        try:
            opcion = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li[contains(text(), '{TIPO_HORA}')]")
                )
            )
            opcion.click()
        except:
            campo_proyecto.send_keys(Keys.ENTER)

        log(f"Tipo hora seleccionada: {TIPO_HORA}")

        #Campo Hora inicio
        hora_inicio = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='HoraInicioNocturna']")))
        hora_inicio.click()
        time.sleep(1)
        hora_inicio.send_keys(HORA_INICIO)
        hora_inicio.send_keys(Keys.TAB)
        log(f"Hora de inicio ingresada: {HORA_INICIO}")

       # Campo servicio (SELECT REAL)
        servicio = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@role='combobox'])[3]")))
        servicio.click()
        time.sleep(1)

        opcion = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//li[normalize-space()='{SERVICIO}']")
            )
        )

        opcion.click()

        log(f"Servicio seleccionado: {SERVICIO}")

        #Campo actividad
        campo_actividad = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='Actividad']")))
        campo_actividad.click()
        time.sleep(1)
        campo_actividad.clear()
        campo_actividad.send_keys(ACTIVIDAD)
        campo_actividad.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        campo_actividad.send_keys(Keys.ENTER)

        log(f"Actividad seleccionada: {ACTIVIDAD}")

        #Campo horas
        campo_horas = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='Horas']"))
        )
        campo_horas.clear()
        campo_horas.send_keys(str(horas))

        log(f"Horas ingresadas: {horas}")

        # Campo comentario/Descripción
        if comentario:
            campo = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//textarea[@name='Comentario']"))
            )

            campo.click()
            time.sleep(0.5)

            campo.clear()
            campo.send_keys(str(comentario))

            campo.send_keys(Keys.TAB)

            log(f"Comentario ingresado: {comentario}")


        # ── 6. Guardar (FIX IMPORTANTE)
        selectores_guardar = [
            "//button[@type='submit']",
            "//button[contains(text(),'Guardar') or contains(text(),'Aceptar')]"
        ]

        for selector in selectores_guardar:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                btn.click()
                log("Guardado OK")
                break
            except:
                continue

        log("Proceso completado")
        done_fn(True)

    except Exception as e:
        log(f"ERROR: {e}")
        done_fn(False, str(e))

    finally:
        if driver:
            time.sleep(2)
            driver.quit()

    def log(msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_fn(f"[{timestamp}] {msg}")

    driver = None
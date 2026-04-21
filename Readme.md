🕐 MaxTime Automation Bot

Automatiza el registro de tiempos en maxtime.choucairtesting.com usando una interfaz gráfica simple + Selenium.

⚙️ Requisitos
Python 3.8+
Google Chrome instalado
Conexión a internet

📦 Instalación (una sola vez)
pip install selenium webdriver-manager

El bot descarga automáticamente el ChromeDriver compatible.

🚀 Ejecución
python UI.py

🖥️ Uso de la interfaz
Ingresa tu usuario.
Ingresa tu contraseña.
✍️ Escribe el comentario (OBLIGATORIO).
Haz clic en GUARDAR.

👉 El bot:

Abre Chrome
Hace login
Busca el día actual
Abre el formulario
Llena automáticamente los campos
Guarda el registro
⏱️ Jornadas automáticas

El sistema detecta la jornada según la hora:

Hora	Jornada	Horas registradas
Antes de 13:00	Mañana	4.5
Después de 13:00	Tarde	4.0

👉 No necesitas cambiar esto manualmente.

🔑 Configuración (MUY IMPORTANTE)

Toda la personalización se hace en:

Variables.py
🧩 Variables configurables
USUARIOS = {
    "elopezp": "tu_password"
}

URL_MAXTIME = "https://maxtime.choucairtesting.com"

PROYECTO = "Conexión Radicación de Siniestros (APM 1099)"
TIPO_HORA = "H. PROYECTO"
SERVICIO = "PRUEBAS GENERALES ÁGILES"
ACTIVIDAD = "EJECUCIÓN DE PRUEBAS"
HORA_INICIO = "07:00"
🧠 Cómo funcionan estas variables

El bot busca coincidencias exactas en la UI de MaxTime, por lo tanto:

⚠️ IMPORTANTE

Los textos deben coincidir EXACTAMENTE con lo que aparece en la plataforma.

Ejemplo:

Si en la web dice:

PRUEBAS GENERALES ÁGILES

Debes escribir exactamente:

SERVICIO = "PRUEBAS GENERALES ÁGILES"

❌ Incorrecto:

SERVICIO = "Pruebas"


💬 Comentario
Se ingresa desde la UI
Es dinámico (no va en Variables.py)
Es obligatorio para ejecutar el bot

👥 Agregar más usuarios
USUARIOS = {
    "elopezp": "123",
    "jperezm": "456",
}

👉 El primero se carga automáticamente en la UI.

🔧 Notas técnicas
El bot usa Selenium con selectores XPath específicos.
Si la página cambia, puede requerir ajustes en:
MaxtimeBot.py

🧪 Solución de problemas
❌ No selecciona opciones en listas
Verifica que el texto en Variables.py sea exacto
Asegúrate de que exista en el sistema
❌ No encuentra el día
Verifica configuración regional (locale)
Debe estar en español:
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
❌ Campos no se llenan
La UI de MaxTime usa componentes dinámicos (MUI)
A veces requiere ajustes en XPath
🚀 Mejoras futuras (opcional)
Ejecución automática con tareas programadas
Historial de registros
Validación de registro duplicado


🧹 Recomendaciones
No dupliques lógica en el bot
Mantén Variables.py como fuente de configuración
No modifiques el flujo principal si ya funciona
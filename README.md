# Droid_X
![image alt](https://github.com/DogoTalei/Droid_X/blob/1ef70abacd0bee5421e845155bb8d705ca282eed/9701927f7ec084996d44b7119ef3bd90.jpg)

Droid_X es una potente herramienta de seguridad para Windows, diseñada para analizar a fondo las aplicaciones de tu dispositivo Android a través de ADB (Android Debug Bridge). Te ayuda a identificar y gestionar aplicaciones potencialmente peligrosas, protegiéndote de malware, adware y permisos intrusivos.


Características Principales
Análisis Avanzado del Sistema: Escanea el dispositivo para detectar aplicaciones con permisos de administrador o servicios de accesibilidad activos, ya que a menudo son utilizados por software malicioso.

Detección de Amenazas por Permisos: Clasifica las aplicaciones en categorías como "Alto Riesgo" y "Potencial Adware" al comparar sus permisos con listas predefinidas y personalizables en el archivo config.json.

Verificación con VirusTotal: Para una capa extra de seguridad, la herramienta consulta la API de VirusTotal para verificar la reputación de las aplicaciones de alto riesgo.

Gestión de Falsos Positivos: Puedes personalizar la lista de aplicaciones seguras del sistema o de fabricantes de confianza en config.json para que sean ignoradas en el análisis, logrando resultados más precisos.

Desinstalación Selectiva e Interactiva: Presenta una lista clara de las aplicaciones detectadas como peligrosas y te permite elegir cuáles quieres desinstalar de forma segura directamente desde el dispositivo.

Gestión de Falsos Positivos: Puedes personalizar la lista de aplicaciones seguras del sistema o de fabricantes de confianza en config.json para que sean ignoradas en el análisis, logrando resultados más precisos.

¿Cómo Funciona?
Conexión con ADB: El programa se conecta a tu dispositivo Android a través de ADB, que debe estar previamente configurado y autorizado.

Obtención de Información: Consulta el dispositivo para obtener una lista completa de aplicaciones, sus permisos, versiones y, lo más importante, sus nombres amigables (etiquetas de la aplicación), sin necesidad de que tú los definas manualmente.

Análisis Dinámico: El programa utiliza la información de config.json para escanear y clasificar cada aplicación. Si una aplicación tiene permisos sospechosos o está marcada como adware, se agrega a la lista de resultados.

Presentación de Resultados: Al finalizar el escaneo, te muestra un resumen claro del análisis y una lista interactiva de las aplicaciones que puedes desinstalar.


Uso
Para usar el programa, simplemente ejecuta el archivo AnalizadorDogo_CS.exe desde la carpeta portable. La herramienta se encargará del resto del proceso.

Pasos para Activar la Depuración USB en Android

1. Activar el Modo de Desarrollador
Primero, deben ir a los Ajustes del dispositivo y encontrar la sección "Acerca del teléfono" o "Acerca del dispositivo". Una vez allí, buscarán un apartado llamado "Número de compilación" o "Versión de MIUI" (dependiendo de la marca del teléfono). Deben presionar sobre esta opción siete veces seguidas hasta que aparezca un mensaje indicando que el "Modo de desarrollador" está activado.

![image_alt](https://github.com/DogoTalei/Droid_X/blob/12faac3cdb1ea156827634fa4669a2f35f3920af/como-activar-opciones-desarrollador-movil-android-1958761.png)

3. Activar la Depuración USB
Después de activar el modo de desarrollador, regresarán al menú principal de Ajustes y buscarán una nueva opción llamada "Opciones de desarrollador". Dentro de este menú, deberán desplazarse hasta encontrar y activar la opción "Depuración USB".

![image_alt](https://github.com/DogoTalei/Droid_X/blob/7ceb0c3d94e7578f5cf2559ef12f277d4efdf0b4/samsung-activar-depuracion-usb.png)

Una vez que estos pasos estén completos, el usuario puede conectar su dispositivo a la computadora y ejecutar tu programa. Si aparece una ventana en el teléfono pidiendo autorización para la depuración USB, deberán aceptarla.
                ![image_alt](https://github.com/DogoTalei/Droid_X/blob/a89e15ac14776ca1c060a73500fe51396663c5b6/450_1000.png)

Demostración 



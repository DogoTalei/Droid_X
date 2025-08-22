import subprocess
import sys
import time
import os
import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import shutil
import importlib.util
from halo import Halo
import colorama

# --- FUNCIÓN DE RUTA Y CARGA DE VARIABLES DE ENTORNO ---
def obtener_ruta_recurso(ruta_relativa):
    """ Obtiene la ruta absoluta a un recurso, funciona para script y para .exe """
    try:
        ruta_base = sys._MEIPASS
    except Exception:
        ruta_base = os.path.abspath(".")
    return os.path.join(ruta_base, ruta_relativa)

load_dotenv(dotenv_path=obtener_ruta_recurso('.env'))

# --- MODO STEALTH Y COLORES ---
STEALTH = "--stealth" in sys.argv
if STEALTH:
    RESET = ROJO = VERDE = AMARILLO = AZUL = MAGENTA = CIAN = BLANCO = GRIS = ''
else:
    RESET = '\033[0m'
    ROJO = '\033[91m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIAN = '\033[96m'
    BLANCO = '\033[97m'
    GRIS = '\033[37m'

# --- CONSTANTES ---
ADB_TIMEOUT = 15
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

BANNER = f"""{MAGENTA}
██████╗ ██████╗  ██████╗ ██╗██████╗       ██╗  ██╗
██╔══██╗██╔══██╗██╔═══██╗██║██╔══██╗      ╚██╗██╔╝
██║  ██║██████╔╝██║   ██║██║██║  ██║       ╚███╔╝ 
██║  ██║██╔══██╗██║   ██║██║██║  ██║       ██╔██╗ 
██████╔╝██║  ██║╚██████╔╝██║██████╔╝███████╗██╔╝ ██╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
              {AZUL}Creador: Dogo Tallei (v1){RESET}
"""

def verificar_dependencias():
    """Comprueba si las librerías de Python necesarias están instaladas."""
    print(f"{AZUL}[•] Verificando dependencias...{RESET}")
    faltantes = []
    librerias_requeridas = {'requests': 'requests', 'dotenv': 'python-dotenv', 'halo': 'halo', 'colorama': 'colorama'}
    for modulo, paquete in librerias_requeridas.items():
        if not importlib.util.find_spec(modulo):
            faltantes.append({
                'tipo': 'libreria', 'nombre': paquete,
                'instruccion': f"Ejecuta en tu terminal: {CIAN}pip install {paquete}{RESET}"
            })
    if faltantes:
        print(f"\n{ROJO}[✘] Faltan dependencias para continuar.{RESET}")
        for item in faltantes:
            print(f"\n  - {AMARILLO}Falta {item['tipo']}:{RESET} {item['nombre']}")
            print(f"    {GRIS}Solución: {item['instruccion']}{RESET}")
        sys.exit(f"\n{ROJO}Instala las dependencias y vuelve a ejecutar el script.{RESET}")
    print(f"{VERDE}[✔] Todas las dependencias están instaladas.{RESET}")
    time.sleep(1)

def cargar_configuracion():
    ruta_config = obtener_ruta_recurso('config.json')
    try:
        with open(ruta_config, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{ROJO}[✘] Archivo 'config.json' no encontrado.{RESET}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{ROJO}[✘] Error de formato en 'config.json'.{RESET}")
        sys.exit(1)

def slow_print(text, delay=0.01):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

def verificar_adb(ruta_adb):
    try:
        resultado = subprocess.run([ruta_adb, 'devices'], capture_output=True, text=True, check=True, timeout=ADB_TIMEOUT)
        lineas = resultado.stdout.strip().splitlines()
        if len(lineas) > 1 and any('device' in l for l in lineas[1:]):
            print(f"\n{VERDE}[✔] Dispositivo ADB encontrado.{RESET}")
            return True
        else:
            print(f"\n{ROJO}[✘] No se encontraron dispositivos ADB autorizados.{RESET}")
            return False
    except (FileNotFoundError, subprocess.SubprocessError):
        print(f"\n{ROJO}[✘] Error al ejecutar ADB. Asegúrate de que está en la carpeta 'vendor/adb'.{RESET}")
        return False

def consultar_virustotal(paquete):
    if not VIRUSTOTAL_API_KEY: return "API Key no configurada"
    url = f"https://www.virustotal.com/api/v3/applications/{paquete}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    try:
        time.sleep(15.5)
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 404: return "No encontrado"
        response.raise_for_status()
        stats = response.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return stats.get("malicious", 0)
    except requests.exceptions.RequestException: return "Error de Conexión"

def guardar_reporte_json(alto, adw, info_disp, admins, accesibilidad):
    info_disp_serializable = {k: v.replace(RESET, "").replace(VERDE, "").replace(AMARILLO, "").replace(ROJO, "").strip() for k, v in info_disp.items()}
    reporte = {"info_dispositivo": info_disp_serializable, "fecha_analisis": datetime.now().isoformat(),
               "analisis_avanzado": {"admins_dispositivo": admins, "servicios_accesibilidad_activos": accesibilidad},
               "resumen": {"total_alto_riesgo": len(alto), "total_adware": len(adw)},
               "apps_alto_riesgo": alto, "apps_potencial_adware": adw}
    nombre_archivo = f"reporte_dogo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=4, ensure_ascii=False)
        print(f"\n{VERDE}[✔] Reporte detallado guardado en: {nombre_archivo}{RESET}")
    except (IOError, PermissionError) as e:
        print(f"\n{ROJO}[✘] No se pudo guardar el reporte: {e}{RESET}")

def obtener_info_dispositivo(ruta_adb):
    info = {}
    props = {'Modelo': 'ro.product.model', 'Fabricante': 'ro.product.manufacturer', 'Versión Android': 'ro.build.version.release', 'Versión SDK': 'ro.build.version.sdk'}
    for nombre, prop in props.items():
        try: info[nombre] = subprocess.check_output([ruta_adb, 'shell', 'getprop', prop], text=True, timeout=ADB_TIMEOUT, stderr=subprocess.DEVNULL).strip()
        except subprocess.SubprocessError: info[nombre] = "Desconocido"
    try:
        root_check = subprocess.run([ruta_adb, 'shell', 'su', '-c', 'id'], capture_output=True, text=True, timeout=ADB_TIMEOUT)
        info['Root'] = f"{VERDE}Sí{RESET}" if "uid=0(root)" in root_check.stdout else f"{AMARILLO}No{RESET}"
    except subprocess.SubprocessError: info['Root'] = f"{ROJO}Desconocido{RESET}"
    try:
        bootloader_locked = subprocess.check_output([ruta_adb, 'shell', 'getprop', 'ro.boot.flash.locked'], text=True, timeout=ADB_TIMEOUT, stderr=subprocess.DEVNULL).strip()
        if bootloader_locked == '1': info['Bootloader Bloqueado'] = f"{VERDE}Sí{RESET}"
        elif bootloader_locked == '0': info['Bootloader Bloqueado'] = f"{ROJO}No (¡Peligro!){RESET}"
        else: info['Bootloader Bloqueado'] = f"{AMARILLO}Inesperado ({bootloader_locked}){RESET}"
    except subprocess.SubprocessError: info['Bootloader Bloqueado'] = f"{AMARILLO}Desconocido{RESET}"
    return info

def imprimir_info_dispositivo(info):
    print(f"\n{AZUL}--- Información del Dispositivo ---{RESET}")
    print(f"{CIAN}  Modelo:               {AMARILLO}{info.get('Modelo')}{RESET}")
    print(f"{CIAN}  Fabricante:           {AMARILLO}{info.get('Fabricante')}{RESET}")
    print(f"{CIAN}  Versión de Android:   {AMARILLO}{info.get('Versión Android')} (SDK {info.get('Versión SDK')}){RESET}")
    print(f"{CIAN}  Acceso Root:          {info.get('Root')}{RESET}")
    print(f"{CIAN}  Bootloader Bloqueado: {info.get('Bootloader Bloqueado')}{RESET}")
    print(f"{AZUL}-----------------------------------{RESET}")

def obtener_paquetes_todos(ruta_adb):
    print(f"\n{AZUL}[•] Obteniendo lista de TODAS las aplicaciones...{RESET}")
    try:
        resultado = subprocess.run([ruta_adb, 'shell', 'pm', 'list', 'packages'], capture_output=True, text=True, check=True, timeout=ADB_TIMEOUT)
        paquetes = [linea.split(':')[1] for linea in resultado.stdout.strip().splitlines()]
        print(f"{VERDE}[✔] {len(paquetes)} paquetes encontrados.{RESET}")
        return paquetes
    except subprocess.SubprocessError: return []

def obtener_admins_dispositivo(ruta_adb):
    try:
        salida = subprocess.check_output([ruta_adb, 'shell', 'dumpsys', 'device_policy'], text=True, timeout=ADB_TIMEOUT)
        admins, parsing = [], False
        for linea in salida.splitlines():
            if "Active Admins:" in linea: parsing = True; continue
            if parsing and "ComponentInfo{" in linea: admins.append(linea.split('{')[1].split('/')[0].strip())
            elif parsing and ":" not in linea and "{" not in linea: parsing = False
        return admins
    except subprocess.SubprocessError: return []

def obtener_servicios_accesibilidad(ruta_adb):
    try:
        salida = subprocess.check_output([ruta_adb, 'shell', 'settings', 'get', 'secure', 'enabled_accessibility_services'], text=True, timeout=ADB_TIMEOUT).strip()
        if not salida or salida == 'null': return []
        return list(set([srv.split('/')[0] for srv in salida.split(':')]))
    except subprocess.SubprocessError: return []

def obtener_nombre_app(ruta_adb, paquete):
    try:
        path_output = subprocess.check_output([ruta_adb, 'shell', 'pm', 'path', paquete], text=True, timeout=ADB_TIMEOUT, stderr=subprocess.DEVNULL).strip()
        apk_path = path_output.split(':')[-1]
        aapt_output = subprocess.check_output([ruta_adb, 'shell', 'aapt', 'dump', 'badging', apk_path], text=True, timeout=ADB_TIMEOUT, stderr=subprocess.DEVNULL)
        for line in aapt_output.splitlines():
            if line.strip().startswith("application-label:"): return line.split("'")[1]
        return paquete
    except subprocess.SubprocessError: return paquete

def analizar_paquete_completo(ruta_adb, paquete, permisos_a_buscar):
    try:
        resultado_bytes = subprocess.check_output([ruta_adb, 'shell', 'dumpsys', 'package', paquete], timeout=ADB_TIMEOUT, stderr=subprocess.DEVNULL)
        resultado = resultado_bytes.decode('utf-8', errors='ignore')
        version, ruta_apk, permisos_encontrados = "N/A", "Desconocida", []
        for linea in resultado.splitlines():
            if "versionName=" in linea: version = linea.split("versionName=")[1].split()[0]
            elif "codePath=" in linea: ruta_apk = linea.split("codePath=")[1]
            elif "granted=true" in linea:
                for permiso in permisos_a_buscar:
                    if permiso in linea and permiso not in permisos_encontrados: permisos_encontrados.append(permiso)
        if permisos_encontrados:
            return {"paquete": paquete, "permisos": permisos_encontrados, "version": version, "ruta_apk": ruta_apk}
        return None
    except subprocess.SubprocessError: return None

def es_ruta_oficial(ruta_apk):
    return any(ruta_apk.startswith(ruta) for ruta in ["/system/", "/vendor/", "/product/", "/system_ext/", "/apex/"])

def desinstalar_apps(ruta_adb, apps_a_desinstalar):
    print(f"\n{ROJO}[!] Iniciando desinstalación selectiva...{RESET}")
    for app_info in apps_a_desinstalar:
        pkg, version = app_info['paquete'], app_info['version']
        print(f"{ROJO}[-] Desinstalando {app_info.get('nombre_app', pkg)} (v{version})...{RESET}")
        try:
            resultado = subprocess.run([ruta_adb, 'shell', 'pm', 'uninstall', '--user', '0', pkg], capture_output=True, text=True, timeout=ADB_TIMEOUT)
            if "Success" in resultado.stdout: print(f"{VERDE}[✔] {pkg} desinstalada.{RESET}")
            else: print(f"{ROJO}[✘] Falló la desinstalación de {pkg}:{RESET} {resultado.stderr.strip() or resultado.stdout.strip()}")
        except subprocess.SubprocessError: print(f"{ROJO}[✘] Timeout al desinstalar {pkg}.{RESET}")

def preguntar_y_desinstalar(ruta_adb, alto_riesgo_list):
    if not alto_riesgo_list: return
    print(f"\n{MAGENTA}--- Apps de Alto Riesgo Encontradas ---{RESET}")
    for i, app_info in enumerate(alto_riesgo_list, 1):
        vt_score = app_info.get('vt_score')
        vt_text = ""
        if isinstance(vt_score, int):
            vt_text = f" {ROJO}(VT: {vt_score}){RESET}" if vt_score > 0 else f" {VERDE}(VT: 0){RESET}"
        elif isinstance(vt_score, str):
             vt_text = f" {AMARILLO}(VT: {vt_score}){RESET}"
        nombre_visible = app_info.get('nombre_app', app_info['paquete'])
        print(f"{BLANCO}{i}. {nombre_visible} ({app_info['paquete']}) (v{app_info['version']}){vt_text}{RESET}")
    
    try:
        seleccion = input(f"\n{MAGENTA}❓ Escribe los NÚMEROS de las apps a desinstalar (separados por espacio) o Enter para omitir: {RESET}").strip()
        if not seleccion:
            print(f"{AZUL}[•] Operación cancelada.{RESET}")
            return
        
        indices_a_borrar, numeros_invalidos = [], []
        partes = seleccion.replace(',', ' ').split()
        for num_str in partes:
            try:
                num_int = int(num_str)
                if 1 <= num_int <= len(alto_riesgo_list):
                    indices_a_borrar.append(num_int - 1)
                else:
                    numeros_invalidos.append(num_str)
            except ValueError:
                numeros_invalidos.append(num_str)

        if numeros_invalidos:
            print(f"{ROJO}[✘] Entradas inválidas ignoradas: {', '.join(numeros_invalidos)}{RESET}")

        if not indices_a_borrar:
            print(f"{AZUL}[•] No se seleccionaron apps válidas.{RESET}")
            return
            
        apps_a_desinstalar = [alto_riesgo_list[i] for i in sorted(list(set(indices_a_borrar)))]
        
        if apps_a_desinstalar:
            desinstalar_apps(ruta_adb, apps_a_desinstalar)
        
    except KeyboardInterrupt:
        print(f"\n{ROJO}[✘] Operación cancelada por el usuario.{RESET}")

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)
    colorama.init(autoreset=True)
    
    verificar_dependencias()
    
    ruta_adb = obtener_ruta_recurso(os.path.join("vendor", "adb", "adb.exe"))

    config = cargar_configuracion()
    PERMISOS_SOSPECHOSOS = config.get('permisos_sospechosos', [])
    PERMISOS_ADWARE = config.get('permisos_adware', [])
    FALSOS_POSITIVOS = set(config.get('falsos_positivos', []))
    
    if not VIRUSTOTAL_API_KEY:
        print(f"{AMARILLO}[!] Advertencia: No se encontró la API Key de VirusTotal.{RESET}")

    slow_print(f"{BLANCO}[*] Iniciando análisis de seguridad...{RESET}", 0.02)
    
    if not verificar_adb(ruta_adb): sys.exit(1)
    
    info_disp = obtener_info_dispositivo(ruta_adb)
    imprimir_info_dispositivo(info_disp)
    
    print(f"\n{AZUL}[•] Realizando análisis avanzado del sistema...{RESET}")
    admins = obtener_admins_dispositivo(ruta_adb)
    accesibilidad = obtener_servicios_accesibilidad(ruta_adb)
    if admins: print(f"{AMARILLO}[!] Apps con permisos de Administrador:{RESET} {', '.join(admins)}")
    if accesibilidad: print(f"{ROJO}[!] Apps con Servicios de Accesibilidad ACTIVOS:{RESET} {', '.join(accesibilidad)}")
    
    paquetes = obtener_paquetes_todos(ruta_adb)
    if not paquetes: sys.exit(1)
    
    print(f"\n{AZUL}[•] Escaneando {len(paquetes)} apps por permisos...{RESET}")
    permisos_a_buscar = PERMISOS_SOSPECHOSOS + PERMISOS_ADWARE
    with ThreadPoolExecutor() as executor:
        resultados = list(executor.map(lambda p: analizar_paquete_completo(ruta_adb, p, permisos_a_buscar), paquetes))
    apps_sospechadas = [r for r in resultados if r]

    alto, adw = [], []
    for app in apps_sospechadas:
        if app['paquete'] in FALSOS_POSITIVOS or es_ruta_oficial(app['ruta_apk']): continue
        es_alto_riesgo = any(p in PERMISOS_SOSPECHOSOS for p in app['permisos']) or \
                         app['paquete'] in admins or app['paquete'] in accesibilidad
        if es_alto_riesgo: alto.append(app)
        else: adw.append(app)

    if alto or adw:
        print(f"\n{AZUL}[•] Obteniendo nombres de apps y reputación...{RESET}")
        all_apps_to_check = alto + adw
        spinner = Halo(text='Iniciando verificación...', spinner='dots')
        try:
            spinner.start()
            for i, app in enumerate(all_apps_to_check, 1):
                spinner.text = f"Verificando {i}/{len(all_apps_to_check)}: {app.get('paquete', 'desconocido')}"
                app['nombre_app'] = obtener_nombre_app(ruta_adb, app['paquete'])
                if app in alto and VIRUSTOTAL_API_KEY:
                    spinner.text = f"Consultando VirusTotal para {app.get('paquete')}..."
                    app['vt_score'] = consultar_virustotal(app['paquete'])
            spinner.succeed("Verificación completada.")
        except (KeyboardInterrupt, SystemExit):
            spinner.stop()

    print(f"\n{AZUL}Análisis completo.{RESET}")
    print(f"{ROJO}Apps de Alto Riesgo: {len(alto)}{RESET} | {AMARILLO}Potencial Adware: {len(adw)}{RESET}")
    preguntar_y_desinstalar(ruta_adb, alto)
    guardar_reporte_json(alto, adw, info_disp, admins, accesibilidad)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ROJO}[✘] Programa interrumpido por el usuario.{RESET}")
    except Exception as e:
        print(f"\n\n{ROJO}[✘] Ha ocurrido un error inesperado: {e}{RESET}")
    finally:
        # AÑADIDO: Pausa para evitar que la ventana se cierre
        print(f"\n{CIAN}El programa ha finalizado. Presiona Enter para salir.{RESET}")
        input()
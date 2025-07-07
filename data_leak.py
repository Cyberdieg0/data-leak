import os
from datetime import datetime 

palabras_clave = ["contraseña", "clave", "password", "usuario", "login", "admin"]
ruta = input("📂 Ingrese la carpeta de la ruta que desea analizar:\n→ ")

#si no es una ruta absoluta asumimos que es una carpeta dentro del home del usuario
if not os.path.isabs(ruta):
    ruta = os.path.join(os.path.expanduser("~"), ruta)
else:
    ruta = os.path.expanduser(ruta)

#convertimos la ruta a una ruta absoluta valida con .abspath
ruta = os.path.abspath(ruta)
print(f"\n📁 Ruta final analizada: {ruta}")

if os.path.exists(ruta):
    print("🔍 Analizando archivos...\n")
    resultados = [] #lisra para guardar los resultados encontrados

    #recorre todos los directorios y subdirectorios usando os.walk
    for carpeta_actual, subcarpetas, archivos in os.walk(ruta):
        for archivo in archivos:
            if archivo.endswith(".txt"):
                ruta_archivo = os.path.join(carpeta_actual, archivo)
                try:  #intentamos abrir y leer el .txt
                    with open(ruta_archivo, "r", encoding="utf-8") as f:
                        lineas = f.readlines()
                        for numero_linea, linea in enumerate(lineas, start=1):
                            for palabra in palabras_clave:
                                if palabra.lower() in linea.lower(): #.lower para encontrar una palabra clave sin distinguir mayuscula
                                    resultado = f"📄 Archivo: {ruta_archivo}\n   → Linea {numero_linea}: contiene '{palabra}'\n"
                                    print(resultado)
                                    resultados.append(resultado)
                except Exception as e: #si ocurre un error, el archivo esta dañado, o no tiene permisos muestra un mensaje de error y sigue con el siguiente archivo
                    print(f"❌ No se pudo leer: {ruta_archivo} ({e})")
    #si hay resultados los exportamos a un reporte txt
    if resultados:
        fecha_actual = datetime.now()
        fecha_hora = fecha_actual.strftime("%d-%m-%Y %H:%M:%S")
        print(f"📅 Fecha y hora actual: {fecha_hora}")
        with open("reporte_leak.txt", "a", encoding="utf-8") as reporte:
            reporte.write("\n==============\n")
            reporte.write (f"📅 Fecha y hora actual: {fecha_hora}\n")
            reporte.write(f"📁 Carpeta analizada: {ruta}\n")
            reporte.write("🔐 Resultado de analisis de posibles filtraciones de datos\n\n")
            for r in resultados:
                reporte.write(r)
        print("\n✅ Analisis realizado. Resultados guardados en 'repote_leak.txt'")
    else:
        print("✅ Análisis realizado. No se encontraron coincidencias.")
else:
    print("❌ La ruta ingresada no existe.")
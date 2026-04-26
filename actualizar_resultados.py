import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

FILE_PATH = 'baloto.xlsx'

def obtener_resultados_baloto():
    url = "https://www.resultadobaloto.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Encontrar todos los contenedores de números (bolas)
        # En la web actual tienen la clase 'numeros-md-mov' o similar
        contenedores = soup.find_all("div", class_=lambda x: x and 'numeros' in x.lower() and 'md-mov' in x.lower())
        
        # Si no encuentra con esa clase específica, intentar una más general
        if not contenedores:
            contenedores = soup.find_all("div", class_=lambda x: x and 'numeros' in x.lower())

        if len(contenedores) < 2:
            print("[!] No se encontraron suficientes contenedores de números.")
            return None

        # El primero suele ser Baloto, el segundo Revancha del último sorteo
        datos_extraidos = []
        for i, cont in enumerate(contenedores[:2]):
            tipo = "Baloto" if i == 0 else "Revancha"
            texto = cont.text.strip().replace(',', ' ')
            numeros = [n.strip() for n in texto.split() if n.strip().isdigit()]
            
            if len(numeros) >= 6:
                datos_extraidos.append({
                    "tipo": tipo,
                    "numeros": numeros[:6]
                })

        if not datos_extraidos:
            return None

        # 2. Extraer Acumulados
        # Buscamos en todo el texto de la página para mayor fiabilidad
        texto_completo = soup.get_text()
        acumulados = {"Baloto": "No disponible", "Revancha": "No disponible"}
        
        import re
        # Buscar el bloque que contiene "próximo sorteo" (con o sin tilde) y los valores
        # Permitimos espacio opcional después del signo $
        bloque_acumulado = re.search(r'pr.ximo sorteo.*?Baloto:?\s*(\$\s?[\d,.]+\s*millones).*?Revancha:?\s*(\$\s?[\d,.]+\s*millones)', texto_completo, re.IGNORECASE | re.DOTALL)
        if bloque_acumulado:
            acumulados["Baloto"] = bloque_acumulado.group(1)
            acumulados["Revancha"] = bloque_acumulado.group(2)
        else:
            # Búsqueda individual buscando valores altos
            for tipo in ["Baloto", "Revancha"]:
                matches = re.finditer(fr"{tipo}:?\s*(\$\s?[\d,.]+\s*(?:millones|mil millones)?)", texto_completo, re.IGNORECASE)
                for m in matches:
                    val_str = m.group(1)
                    if "4.000" not in val_str and "1.000" not in val_str and "2.000" not in val_str and "500" not in val_str:
                        acumulados[tipo] = val_str
                        break
                if acumulados[tipo] == "No disponible":
                    match = re.search(fr"{tipo}:?\s*(\$\s?[\d,.]+\s*(?:millones|mil millones)?)", texto_completo, re.IGNORECASE)
                    if match: acumulados[tipo] = match.group(1)

        # 3. Extraer Fecha del Sorteo
        fecha_val = datetime.now().strftime('%d/%m/%Y')
        # Buscar "Sorteo XXXX del día Sábado 25 de Abril de 2026" o similares
        match_fecha_completa = re.search(r'(\d{1,2}) de (\w+) de (\d{4})', texto_completo, re.IGNORECASE)
        if match_fecha_completa:
            meses = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06", 
                     "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}
            dia = match_fecha_completa.group(1).zfill(2)
            mes = meses.get(match_fecha_completa.group(2).lower(), "01")
            anio = match_fecha_completa.group(3)
            fecha_val = f"{dia}/{mes}/{anio}"
        else:
            # Buscar formato DD/MM/YYYY
            match_std = re.search(r'(\d{2}/\d{2}/\d{4})', texto_completo)
            if match_std:
                fecha_val = match_std.group(1)

        # 4. Formatear resultados finales
        resultados = {"Baloto": None, "Revancha": None}
        for item in datos_extraidos:
            tipo = item["tipo"]
            numeros = item["numeros"]
            resultados[tipo] = {
                "visual": {
                    "Sorteo": f"**{tipo}**",
                    "Números Ganadores": " - ".join(numeros[:5]),
                    "Súper Balota": numeros[5],
                    "Acumulado Próximo Sorteo": acumulados[tipo]
                },
                "excel": {
                    "Fecha": fecha_val,
                    "B1": int(numeros[0]), "B2": int(numeros[1]), "B3": int(numeros[2]), 
                    "B4": int(numeros[3]), "B5": int(numeros[4]), "SB": int(numeros[5])
                }
            }
        
        return resultados

    except Exception as e:
        print(f"Error al conectar con la fuente: {e}")
        import traceback
        traceback.print_exc()
        return None

def actualizar_excel(datos_dict):
    if not os.path.exists(FILE_PATH):
        print(f"Error: No se encontró el archivo {FILE_PATH}")
        return

    try:
        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            for nombre_hoja, datos in datos_dict.items():
                if datos and 'excel' in datos:
                    df_existente = pd.read_excel(FILE_PATH, sheet_name=nombre_hoja)
                    
                    # Crear nueva fila con fecha como datetime
                    nueva_fila = datos['excel'].copy()
                    nueva_fila['Fecha'] = pd.to_datetime(nueva_fila['Fecha'], dayfirst=True)
                    
                    # Verificar si ya existe el sorteo por fecha
                    fechas_existentes = pd.to_datetime(df_existente['Fecha'], errors='coerce')
                    if nueva_fila['Fecha'] in fechas_existentes.values:
                        print(f"[!] El sorteo del {nueva_fila['Fecha'].strftime('%d/%m/%Y')} ya existe en {nombre_hoja}. Saltando...")
                        continue
                    
                    df_nueva = pd.DataFrame([nueva_fila])
                    
                    # Concatenar y guardar
                    df_final = pd.concat([df_existente, df_nueva], ignore_index=True)
                    df_final.to_excel(writer, sheet_name=nombre_hoja, index=False)
                    print(f"[OK] Hoja '{nombre_hoja}' actualizada con éxito.")
    except Exception as e:
        print(f"Error al actualizar el Excel: {e}")

def presentar_tabla(resultados):
    if resultados:
        tabla_visual = []
        if resultados.get("Baloto"): tabla_visual.append(resultados["Baloto"]["visual"])
        if resultados.get("Revancha"): tabla_visual.append(resultados["Revancha"]["visual"])
        
        if tabla_visual:
            df_visual = pd.DataFrame(tabla_visual)
            print("\n### Resultados obtenidos:")
            print(df_visual.to_markdown(index=False))
            print(f"\n*Fecha de consulta: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*")
            return True
    return False

if __name__ == "__main__":
    res = obtener_resultados_baloto()
    
    # Si el scraping falla, el script te permitirá ingresar los datos manualmente o usará la guía de PROMPT_RESULTADOS.md
    if not res or (not res["Baloto"] and not res["Revancha"]):
        print("\n[!] No se pudieron extraer datos automáticamente.")
        print("Sigue las instrucciones en PROMPT_RESULTADOS.md para obtener los números y agrégalos manualmente al Excel.")
    else:
        if presentar_tabla(res):
            confirmar = input("\n¿Deseas guardar estos resultados en baloto.xlsx? (s/n): ")
            if confirmar.lower() == 's':
                actualizar_excel(res)
            else:
                print("Operación de guardado cancelada.")

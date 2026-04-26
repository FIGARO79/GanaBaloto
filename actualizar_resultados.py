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

        resultados = []
        
        def extraer_datos(tipo):
            seccion = soup.find(lambda tag: tag.name == "h2" and tipo in tag.text)
            if not seccion:
                seccion = soup.find(lambda tag: tag.name == "div" and tipo in tag.text)
            
            if seccion:
                contenedor = seccion.find_parent('div')
                bolas = contenedor.find_all(class_=lambda x: x and ('ball' in x.lower() or 'numero' in x.lower()))
                if not bolas:
                    bolas = contenedor.find_all('span')
                
                numeros = [b.text.strip() for b in bolas if b.text.strip().isdigit()]
                
                if len(numeros) >= 6:
                    # Datos para la tabla visual
                    n_principales = " - ".join(numeros[:5])
                    super_balota = numeros[5]
                    
                    # Datos para el Excel (numéricos)
                    datos_excel = [int(n) for n in numeros[:6]]
                    
                    # Buscar acumulado
                    acumulado_text = contenedor.find(lambda tag: "acumulado" in tag.text.lower())
                    acumulado = acumulado_text.text.strip() if acumulado_text else "No disponible"
                    
                    # Intentar extraer fecha del sorteo
                    fecha_text = soup.find(lambda tag: "Sorteo" in tag.text and ("202" in tag.text))
                    fecha_val = datetime.now().strftime('%d/%m/%Y') # Default
                    if fecha_text:
                        import re
                        match = re.search(r'\d{2}/\d{2}/\d{4}', fecha_text.text)
                        if match: fecha_val = match.group()

                    return {
                        "visual": {
                            "Sorteo": f"**{tipo}**",
                            "Números Ganadores": n_principales,
                            "Súper Balota": super_balota,
                            "Acumulado Próximo Sorteo": acumulado
                        },
                        "excel": {
                            "Fecha": fecha_val,
                            "B1": datos_excel[0], "B2": datos_excel[1], "B3": datos_excel[2], 
                            "B4": datos_excel[3], "B5": datos_excel[4], "SB": datos_excel[5]
                        }
                    }
            return None

        res_baloto = extraer_datos("Baloto")
        res_revancha = extraer_datos("Revancha")

        return {"Baloto": res_baloto, "Revancha": res_revancha}

    except Exception as e:
        print(f"Error al conectar con la fuente: {e}")
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

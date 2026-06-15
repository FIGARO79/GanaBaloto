import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import re
import json

FILE_PATH = 'baloto.json'

def extraer_premios(soup):
    premios = {
        "Baloto": {"5+1": 0, "5+0": 0},
        "Revancha": {"5+1": 0, "5+0": 0}
    }
    tables = soup.find_all('table')
    for i, tipo in enumerate(["Baloto", "Revancha"]):
        if len(tables) > i:
            rows = tables[i].find_all(['tr', 'row'])
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                texto_aciertos = cols[0].text.strip().lower()
                monto = cols[2].text.strip().replace('$', '').replace('.', '').replace(',', '')
                try:
                    monto_premio = int(monto)
                except ValueError:
                    monto_premio = 0
                
                if "5 + sb" in texto_aciertos or "5+sb" in texto_aciertos.replace(' ', ''):
                    premios[tipo]["5+1"] = monto_premio
                elif "5 aciertos" in texto_aciertos and "sb" not in texto_aciertos:
                    premios[tipo]["5+0"] = monto_premio
    return premios

def obtener_todos_los_resultados():
    url = "https://www.resultadobaloto.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        premios_actuales = extraer_premios(soup)
        
        resultados_lista = []
        headings = soup.find_all(class_='panel-heading')
        
        for heading in headings:
            if 'Baloto' not in heading.text or not heading.find('time'): continue
            
            # Extraer Fecha
            time_tag = heading.find('time')
            if time_tag and time_tag.get('datetime'):
                fecha_str = datetime.strptime(time_tag.get('datetime'), '%Y-%m-%d').strftime('%d/%m/%Y')
            else:
                match_fecha = re.search(r'(\d{1,2}) de (\w+) de (\d{4})', heading.text, re.IGNORECASE)
                if not match_fecha: continue
                meses = {"enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06", 
                         "julio": "07", "agosto": "08", "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"}
                dia = match_fecha.group(1).zfill(2)
                mes = meses.get(match_fecha.group(2).lower(), "01")
                anio = match_fecha.group(3)
                fecha_str = f"{dia}/{mes}/{anio}"

            # Extraer Números
            body = heading.find_next_sibling(class_='panel-body')
            if not body: continue
            
            bloques_nums = body.find_all(class_='numeros-md-mov')
            if len(bloques_nums) < 2: continue
            
            def extract_from_bloque(bloque):
                nums = [s.text.strip() for s in bloque.find_all(class_='label-baloto')]
                sb = bloque.find(class_='label-comple')
                if sb: nums.append(sb.text.strip())
                return nums

            baloto_nums = extract_from_bloque(bloques_nums[0])
            revancha_nums = extract_from_bloque(bloques_nums[1])
            
            if len(baloto_nums) < 6 or len(revancha_nums) < 6: continue
            
            es_ultimo = (len(resultados_lista) == 0)
            res = {
                "Fecha": fecha_str,
                "Baloto": {
                    "numeros": baloto_nums,
                    "p51": premios_actuales["Baloto"]["5+1"] if es_ultimo else 0,
                    "p50": premios_actuales["Baloto"]["5+0"] if es_ultimo else 0
                },
                "Revancha": {
                    "numeros": revancha_nums,
                    "p51": premios_actuales["Revancha"]["5+1"] if es_ultimo else 0,
                    "p50": premios_actuales["Revancha"]["5+0"] if es_ultimo else 0
                }
            }
            resultados_lista.append(res)
            
        return resultados_lista

    except Exception as e:
        print(f"Error al conectar con la fuente: {e}")
        return None

def actualizar_json(lista_resultados):
    if not os.path.exists(FILE_PATH):
        print(f"Error: No se encontró el archivo {FILE_PATH}")
        return

    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            dict_hojas = json.load(f)
        
        cambios = False
        for tipo in ["Baloto", "Revancha"]:
            df = pd.DataFrame(dict_hojas[tipo])
            # En el JSON la fecha se guarda en formato YYYY-MM-DD
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            
            fechas_existentes = df['Fecha'].dt.date.dropna().tolist()
            
            nuevas_filas = []
            for item in reversed(lista_resultados):
                fecha_dt = pd.to_datetime(item["Fecha"], dayfirst=True)
                
                if fecha_dt.date() not in fechas_existentes:
                    nums = item[tipo]["numeros"]
                    nueva_fila = {
                        "Fecha": fecha_dt.strftime('%Y-%m-%d'),
                        "B1": int(nums[0]), "B2": int(nums[1]), "B3": int(nums[2]),
                        "B4": int(nums[3]), "B5": int(nums[4]), "SB": int(nums[5]),
                        "Premios 5+1": int(item[tipo]["p51"]),
                        "Premios 5+0": int(item[tipo]["p50"])
                    }
                    nuevas_filas.append(nueva_fila)
                    print(f"[+] Añadiendo {tipo} del {item['Fecha']}")
            
            if nuevas_filas:
                df_nuevas = pd.DataFrame(nuevas_filas)
                df_nuevas['Fecha'] = pd.to_datetime(df_nuevas['Fecha'])
                df_final = pd.concat([df, df_nuevas], ignore_index=True)
                df_final = df_final.sort_values(by='Fecha').reset_index(drop=True)
                
                df_final['Fecha'] = df_final['Fecha'].dt.strftime('%Y-%m-%d')
                for col in ['B1', 'B2', 'B3', 'B4', 'B5', 'SB', 'Premios 5+1', 'Premios 5+0']:
                    df_final[col] = df_final[col].astype(int)
                    
                dict_hojas[tipo] = df_final.to_dict(orient='records')
                cambios = True
        
        if not cambios:
            print("[!] No se encontraron sorteos nuevos.")
        else:
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(dict_hojas, f, ensure_ascii=False, indent=4)
            print("[OK] JSON actualizado.")

    except Exception as e:
        print(f"Error al actualizar el archivo JSON: {e}")

def presentar_resumen(lista_resultados):
    if not lista_resultados:
        print("No se obtuvieron resultados.")
        return False
    
    print(f"\n### Sorteos encontrados en la web:")
    resumen = []
    for r in lista_resultados:
        resumen.append({
            "Fecha": r["Fecha"],
            "Baloto": " - ".join(r["Baloto"]["numeros"][:5]) + " [" + r["Baloto"]["numeros"][5] + "]",
            "Revancha": " - ".join(r["Revancha"]["numeros"][:5]) + " [" + r["Revancha"]["numeros"][5] + "]",
            "Premios Baloto (5+1 / 5+0)": f"${r['Baloto']['p51']:,} / ${r['Baloto']['p50']:,}".replace(',', '.')
        })
    
    df_resumen = pd.DataFrame(resumen)
    print(df_resumen.to_markdown(index=False))
    return True

if __name__ == "__main__":
    import sys
    es_auto = os.getenv("AUTO_UPDATE") == "true" or "--auto" in sys.argv
    print("Buscando resultados...")
    res = obtener_todos_los_resultados()
    if res:
        if presentar_resumen(res):
            if es_auto:
                print("\n[AUTO] Guardando automáticamente los nuevos resultados en baloto.json...")
                actualizar_json(res)
            else:
                confirmar = input("\n¿Deseas guardar los nuevos resultados en baloto.json? (s/n): ")
                if confirmar.lower() == 's':
                    actualizar_json(res)
                else:
                    print("Operación cancelada.")


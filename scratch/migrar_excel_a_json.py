import pandas as pd
import json
import os

FILE_EXCEL = 'baloto.xlsx'
FILE_JSON = 'baloto.json'

def migrar():
    if not os.path.exists(FILE_EXCEL):
        print(f"Error: No se encontró el archivo {FILE_EXCEL}")
        return
        
    print(f"Leyendo {FILE_EXCEL}...")
    xls = pd.ExcelFile(FILE_EXCEL)
    
    data_final = {}
    
    for sheet in ['Baloto', 'Revancha']:
        if sheet in xls.sheet_names:
            print(f"Procesando hoja '{sheet}'...")
            df = pd.read_excel(FILE_EXCEL, sheet_name=sheet)
            
            # Limpiar filas vacías
            df = df.dropna(subset=['B1', 'B2', 'B3', 'B4', 'B5', 'SB'])
            
            # Convertir Fecha a string YYYY-MM-DD
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            # Si hay fechas nulas, rellenar o reportar
            if df['Fecha'].isnull().any():
                print("Advertencia: Se detectaron fechas inválidas que serán omitidas.")
                df = df.dropna(subset=['Fecha'])
            
            df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')
            
            # Convertir columnas numéricas a int
            cols_int = ['B1', 'B2', 'B3', 'B4', 'B5', 'SB']
            if 'Premios 5+1' in df.columns:
                df['Premios 5+1'] = pd.to_numeric(df['Premios 5+1'], errors='coerce').fillna(0)
                cols_int.append('Premios 5+1')
            if 'Premios 5+0' in df.columns:
                df['Premios 5+0'] = pd.to_numeric(df['Premios 5+0'], errors='coerce').fillna(0)
                cols_int.append('Premios 5+0')
                
            for col in cols_int:
                df[col] = df[col].astype(int)
                
            # Convertir a lista de diccionarios
            registros = df.to_dict(orient='records')
            data_final[sheet] = registros
            print(f"Migrados {len(registros)} registros para {sheet}.")
            
    print(f"Escribiendo en {FILE_JSON}...")
    with open(FILE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data_final, f, ensure_ascii=False, indent=4)
        
    print("¡Migración completada exitosamente!")

if __name__ == "__main__":
    migrar()

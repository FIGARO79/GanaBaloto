# Fuentes Oficiales, Horarios y Arquitectura de Sincronización

## 📅 Calendario de Sorteos (Colombia)
Los sorteos oficiales de **Baloto** y **Revancha** se llevan a cabo dos veces por semana:
- **Miércoles en la noche**: aproximadamente a las 23:00 COT (Hora de Colombia, UTC-5).
- **Sábados en la noche**: aproximadamente a las 23:00 COT (Hora de Colombia, UTC-5).

### Reglas de los Números
- **Balotas Principales**: 5 números enteros seleccionados entre **1 y 43** (sin repetición en un mismo sorteo).
- **Super Balota (SB)**: 1 número entero seleccionado entre **1 y 16**.

---

## 🌐 Fuentes de Datos
1. **Resultado Baloto (Scraping Primario)**:
   - URL: `https://www.resultadobaloto.com/`
   - El script `actualizar_resultados.py` analiza el HTML de este portal mediante BeautifulSoup.
2. **Sitio Oficial Baloto**:
   - URL: `https://baloto.com/`
   - Fuente de contraste y auditoría en caso de discrepancias en los números o premios.

---

## 🤖 Flujo Automatizado de GitHub Actions
El repositorio cuenta con un flujo en `.github/workflows/actualizar_sorteos.yml`:
- **Cron**: `0 17 * * 0,2,4` (Domingos, Martes y Jueves a las 12:00 PM COT / 17:00 UTC).
- **Paso 1**: Ejecuta `actualizar_resultados.py` con la variable `AUTO_UPDATE="true"`.
- **Paso 2**: Si `baloto.json` tiene cambios, realiza commit y push automático.
- **Paso 3**: Sube `baloto.json` a la API de PythonAnywhere (`ganabaloto.pythonanywhere.com`).
- **Paso 4**: Llama al endpoint de recarga de la WebApp en PythonAnywhere para actualizar la memoria de Flask.

---

## 🚨 Protocolo de Rescate y Búsqueda Manual
Si el scraper falla (por ejemplo por cambio en el maquetado HTML o caída del portal):
1. Usar el prompt definido en `PROMPT_RESULTADOS.md`:
   > *"Realiza una búsqueda web de los resultados de Baloto y Revancha del [FECHA] y presenta los resultados en una tabla que incluya: Sorteo, Números Ganadores, Súper Balota y Acumulado Próximo Sorteo."*
2. Verificar número de sorteo y fecha correspondiente.
3. Auditar siempre con `validar_datos.py` antes de realizar commit a `baloto.json`.

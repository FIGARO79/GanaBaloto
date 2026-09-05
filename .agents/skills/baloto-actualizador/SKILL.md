---
name: baloto-actualizador
description: >-
  Use this skill when updating, auditing, verifying, or repairing the historical lottery dataset (baloto.json) for Baloto and Revancha, running the web scraper, validating database integrity, or ingesting new draw results.
---

# Sincronización y Validación de Datos (Baloto & Revancha)

Esta skill proporciona las herramientas y procedimientos para mantener actualizada y libre de anomalías la base de datos histórica `baloto.json`, tanto de forma automatizada mediante web scraping como manual por contingencia.

Para consultar el cronograma de sorteos, fuentes oficiales y arquitectura de despliegue en GitHub Actions, revisa la referencia:
[Fuentes Oficiales, Horarios y Arquitectura](./references/fuentes_y_horarios.md).

---

## Procedimientos

### 1. Actualización Automática de Sorteos (Web Scraper)
El script `actualizar_resultados.py` consulta el portal de resultados, detecta sorteos recientes y los agrega a `baloto.json` evitando duplicados.

**Ejecución interactiva (pide confirmación antes de guardar):**
```bash
./.venv/bin/python actualizar_resultados.py
```

**Ejecución desatendida / automatizada (guarda directamente si hay novedades):**
```bash
./.venv/bin/python actualizar_resultados.py --auto
```

---

### 2. Auditoría de Integridad de la Base de Datos
Antes y después de cualquier actualización o edición, se debe auditar `baloto.json` para verificar que no existan inconsistencias de formato, números duplicados dentro de una jugada, valores fuera de rango o fechas desordenadas.

**Comando de validación:**
```bash
./.venv/bin/python .agents/skills/baloto-actualizador/scripts/validar_datos.py
```

**Validaciones realizadas:**
* Hojas requeridas: `Baloto` y `Revancha`.
* Rango de balotas: $B_1 \dots B_5 \in [1, 43]$ y $SB \in [1, 16]$.
* Balotas únicas por jugada (sin repetición interna).
* Formato de fecha estricto `YYYY-MM-DD` y orden cronológico.
* Detección de fechas duplicadas o saltos en la secuencia.
* Detección de sincronía entre el total de sorteos de Baloto y Revancha.

**Modo JSON:**
```bash
./.venv/bin/python .agents/skills/baloto-actualizador/scripts/validar_datos.py --json
```

---

### 3. Protocolo de Contingencia si Falla el Scraper
Si la fuente web principal cambia su estructura o se encuentra inaccesible:
1. Efectuar búsqueda de los números oficiales utilizando el formato de [PROMPT_RESULTADOS.md](../../../PROMPT_RESULTADOS.md):
   * *Ejemplo:* "Resultados de Baloto y Revancha del [FECHA]"
2. Verificar que los 5 números pertenezcan a 1-43 y la Super Balota a 1-16.
3. Incorporar los registros en `baloto.json` bajo la estructura:
   ```json
   {
       "Fecha": "YYYY-MM-DD",
       "B1": 1,
       "B2": 18,
       "B3": 25,
       "B4": 31,
       "B5": 43,
       "SB": 8,
       "Premios 5+1": 0,
       "Premios 5+0": 0
   }
   ```
4. Ejecutar `validar_datos.py` para certificar la integridad del archivo.

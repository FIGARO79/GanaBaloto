# Arquitectura y Endpoints de la API REST (Flask + React)

GanaBaloto dispone de una arquitectura desacoplada compuesta por un backend Flask (en `app.py`) y una Single Page Application (SPA) en React + Vite (en `frontend/`).

---

## 🔌 Especificación de Endpoints REST

### 1. `GET /api/sorteo/<tipo>`
Obtiene el análisis estadístico completo, datos del último sorteo, frecuencias, números fríos/calientes y matrices de transición para el sorteo especificado (`Baloto` o `Revancha`).

- **Parámetros URL**: `tipo` (`Baloto` o `Revancha`).
- **Respuesta 200 OK**:
  ```json
  {
    "sorteo": "Baloto",
    "last_combination": [1, 18, 25, 31, 43],
    "last_sb": 8,
    "total_combinations": 1009,
    "score_meta": 0.1499,
    "score_mediana": 0.1475,
    "score_p75": 0.1550,
    "last_score": 0.1523,
    "last_markov": 0.000021,
    "hot_numbers": [...],
    "cold_numbers": [...],
    "chi2": [...],
    "parity": [...],
    "low_high": [...],
    "decade": [...],
    "pos_top_data": [...],
    "winners_adn": [...]
  }
  ```

---

### 2. `POST /api/generar`
Genera combinaciones candidatas basadas en ponderaciones estadísticas y el Índice Compuesto Global.

- **Cuerpo de la Petición (JSON)**:
  ```json
  {
    "sorteo": "Baloto",
    "cantidad": 5
  }
  ```
- **Respuesta 200 OK**:
  ```json
  {
    "combinaciones": [
      {
        "combinacion": [8, 12, 21, 28, 43],
        "sb": 7,
        "score": 0.1612,
        "composite": 64.7,
        "score_gauss": 1.0,
        "score_entropy": 0.92,
        "score_bayes": 0.53,
        "score_hazard": 0.58,
        "prob_m": 0.000015,
        "prob_pos": 0.0
      }
    ]
  }
  ```

---

### 3. `POST /api/analizar`
Audita un boleto personalizado de 5 números y Super Balota proporcionado por el usuario.

- **Cuerpo de la Petición (JSON)**:
  ```json
  {
    "sorteo": "Baloto",
    "numeros": [4, 8, 15, 23, 42],
    "sb": 7
  }
  ```
- **Respuesta 200 OK**:
  ```json
  {
    "combinacion": [4, 8, 15, 23, 42],
    "sb": 7,
    "composite": 67.89,
    "score": 0.1571,
    "score_gauss": 0.79,
    "score_entropy": 0.88,
    "score_bayes": 0.52,
    "score_hazard": 0.58,
    "prob_m": 0.000020,
    "prob_pos": 0.0,
    "veredicto": [
      "👍 CALIFICACIÓN GENERAL: 🟡 BUENA / PROMEDIO...",
      "• 🟢 Suma de balotas (92): EXCELENTE...",
      "..."
    ]
  }
  ```

---

### 4. `POST /api/rueda`
Genera un sistema de ruedas combinatorias reducidas (Wheeling System).

- **Cuerpo de la Petición (JSON)**:
  ```json
  {
    "sorteo": "Baloto",
    "numeros": [4, 8, 15, 23, 31, 38, 42],
    "garantia": 3,
    "sbs": [7, 11]
  }
  ```
- **Respuesta 200 OK**:
  ```json
  {
    "ruedas": [[4, 8, 15, 23, 31], ...],
    "tiquetes_finales": [{"combinacion": [4, 8, 15, 23, 31], "sb": 7}, ...],
    "total_tiquetes": 10,
    "tiquetes_base": 5,
    "superbalotas": [7, 11],
    "garantia": 3
  }
  ```

---

### 5. `POST /api/recargar`
Fuerza la recarga e indexación en memoria de los datos históricos desde `baloto.json`.
- **Respuesta 200 OK**: `{"status": "ok", "message": "Datos recargados exitosamente"}`

---

## 🖥️ Flujo de Compilación y Ejecución Web
1. **Frontend**: Escrito en React con Vite y Tailwind CSS / Lucide icons.
   - Directorio: `frontend/`
   - Build: `npm run build` compila los assets hacia `frontend/dist/`.
2. **Backend**: Flask sirve los archivos estáticos de `frontend/dist` en la ruta raíz `/` y expone las rutas REST bajo el prefijo `/api/`.

---
name: baloto-servicio-web
description: >-
  Use this skill when running, testing, debugging, or deploying the GanaBaloto full-stack application (Flask backend REST API and React/Vite frontend), executing automated API integration tests, verifying endpoints, or compiling frontend assets.
---

# Gestión del Servicio Web Full-Stack (Flask + React)

Esta skill permite administrar, probar y verificar la aplicación web completa de GanaBaloto, que combina un backend en Flask (`app.py`) y un frontend en React + Vite (`frontend/`).

Para conocer el detalle de los contratos de la API REST y esquemas de petición/respuesta, consulta la referencia:
[Arquitectura y Endpoints de la API REST](./references/arquitectura_api.md).

---

## Procedimientos y Flujos de Trabajo

### 1. Ejecución de la Suite de Pruebas Automatizadas de la API
Verifica que todos los endpoints (`/api/sorteo/*`, `/api/generar`, `/api/analizar`, `/api/rueda`, `/api/recargar`) respondan con código HTTP 200 y esquemas JSON íntegros.

**Comando:**
```bash
./.venv/bin/python .agents/skills/baloto-servicio-web/scripts/test_api.py
```

*Valida tiempos de respuesta por endpoint y confirma el funcionamiento de los 6 modelos en el backend.*

---

### 2. Compilación del Frontend (React + Vite)
Cuando se realicen modificaciones en los componentes visuales en `frontend/src/`, es necesario compilar el paquete estático que sirve Flask:

```bash
cd frontend && npm run build && cd ..
```
*Los archivos generados se ubican en `frontend/dist/`.*

---

### 3. Iniciar el Servidor Web Completo
Para arrancar el backend en modo local:

**Usando el script lanzador:**
```bash
./ejecutar_web.sh
```

**O manualmente:**
```bash
./.venv/bin/python app.py
```
*El servicio queda accesible en `http://localhost:5000`.*

---

### 4. Recarga de Caché en Memoria
Si `baloto.json` se actualiza mientras el servidor Flask está en ejecución, se puede forzar el refresco de memoria sin reiniciar el servidor:

```bash
curl -X POST http://localhost:5000/api/recargar
```

---

### 5. Verificación de Aceleración por Hardware (JAX / CUDA)
GanaBaloto detecta automáticamente si hay disponible una GPU NVIDIA con soporte CUDA para acelerar el cálculo matricial en JAX:

```bash
./.venv/bin/python -c "
import jax
print('Dispositivos JAX detectados:', jax.devices())
"
```
*Si no hay GPU presente, JAX conmuta automáticamente a CPU sin interrumpir el servicio.*

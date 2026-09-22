# Reglas de Proyecto: GanaBaloto

## ⚡ Palabra Activadora Rápida (Trigger Keyword)
* **Palabra Principal:** `PRONOSTICO` (o en minúsculas `pronostico`)
* **Alias reconocidos:** `JUGADAS`, `GANABALOTO`

Cuando el usuario ingrese la palabra activadora o solicite jugadas/pronósticos para el sorteo:
1. **Activar de inmediato la skill:** `baloto-analisis-predictivo` (`.agents/skills/baloto-analisis-predictivo/SKILL.md`).
2. **Ejecutar el script automatizado:**
   ```bash
   ./.venv/bin/python .agents/skills/baloto-analisis-predictivo/scripts/ejecutar_pronostico_completo.py
   ```
3. **Presentar la respuesta con la estructura estandarizada en 4 secciones:**
   * **Cabecera de Entorno:** Motor estocástico JAX con GPU detectada y total de sorteos en `baloto.json`.
   * **🎱 1. Pronósticos Recomendados: Baloto:** Tabla Markdown de 10 columnas con Top 5 jugadas ordenadas por Índice Compuesto descendente, sumas, métricas completas e insignias (🏆 Top #1, 🌟 Perfil Óptimo $\ge 70$, 🧬 ADN Ganador $\ge$ Meta JAX).
   * **🎱 2. Pronósticos Recomendados: Revancha:** Tabla Markdown idéntica con Top 5 jugadas para Revancha y leyenda explicativa de insignias.
   * **🔬 3. Auditoría Detallada de las Jugadas Estrella:** Desglose cualitativo a fondo del Top 1 de Baloto y Top 1 de Revancha (Suma/Gauss en zona dorada 90-130, Entropía/Dispersión, Score JAX vs Meta histórica, SB destacada y nivel de madurez por Hazard Rate).
   * **🛡️ 4. Estrategia Avanzada: Rueda Combinatoria Reducida (Wheeling System):** Bloque de 7 números clave (cruce de frecuentes y atrasadas) con 2 Super Balotas más probables, con garantía matemática de 3 aciertos en 10 tiquetes optimizados.
4. **Idioma:** Todas las respuestas y análisis deben entregarse en español.

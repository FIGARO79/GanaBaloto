import streamlit as st
import pandas as pd
import numpy as np
import os
import jax
import ganabaloto as gb

# --- Configuración Inicial del Sistema ---
# Deshabilitar preasignación de JAX (por seguridad en la web)
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"] = "false"

# Configuración de página de Streamlit
st.set_page_config(
    page_title="GanaBaloto Web - Analítica de Lotería",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS Personalizados (Aesthetics - Tarjetas y Layout) ---
st.markdown("""
<style>
    /* Reducir el padding superior de la aplicación y del sidebar para subir los títulos */
    .block-container {
        padding-top: 1.5rem !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
    }
    
    /* Estilizar todos los contenedores con borde de Streamlit para que parezcan tarjetas premium */
    div[data-testid="stVerticalBlockBorderDiv"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        padding: 18px !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-testid="stVerticalBlockBorderDiv"]:hover {
        transform: translateY(-2px) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.1) !important;
    }
    div[data-testid="stVerticalBlockBorderDiv"] p, div[data-testid="stVerticalBlockBorderDiv"] span, div[data-testid="stVerticalBlockBorderDiv"] div {
        color: #1e272e !important;
    }
    
    /* Asegurar que el botón de colapsar sidebar sea visible y oscuro en el tema claro */
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
        color: #1e272e !important;
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg {
        fill: #1e272e !important;
        color: #1e272e !important;
    }
    
    /* Ajustar el contenedor del botón de sidebar colapsado para permitir que se expanda */
    div:has(> button[data-testid=stSidebarCollapseButton]),
    [data-testid=collapsedControl],
    .st-emotion-cache-collapsedNav,
    div[class*=collapsedNav],
    div[data-testid=collapsedControl] {
        width: auto !important;
        height: auto !important;
        overflow: visible !important;
        background: transparent !important;
    }
    
    /* Mostrar la palabra "Controles" al lado de la flecha cuando el sidebar está oculto */
    button[data-testid=stSidebarCollapseButton]:not(section[data-testid=stSidebar] button) {
        width: auto !important;
        height: 40px !important;
        padding-right: 14px !important;
        padding-left: 10px !important;
        border-radius: 20px !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        transition: all 0.2s ease-in-out !important;
        overflow: visible !important;
    }
    button[data-testid=stSidebarCollapseButton]:not(section[data-testid=stSidebar] button):hover {
        background-color: #f8fafc !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }
    button[data-testid=stSidebarCollapseButton]:not(section[data-testid=stSidebar] button)::after {
        content: "Controles" !important;
        display: inline-block !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #1e272e !important;
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Funciones de Dibujado de Balotas (Aesthetics) ---
def render_balotas_html(numeros, sb):
    """Renderiza las balotas principales en 3D rojo y blanco, y la Super Balota en amarillo/negro con círculos centrales."""
    html_str = "<div style='display: flex; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;'>"
    # Balotas principales (Cuerpo Rojo, Círculo Blanco, Número Rojo)
    for num in numeros:
        html_str += f'<div style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #ff4d4d 0%, #ff1a1a 40%, #cc0000 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.25), inset -2px -2px 6px rgba(0,0,0,0.3); border: 1px solid #990000;"><div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #ffffff; color: #cc0000 !important; font-weight: 900; font-size: 14px; font-family: \'Inter\', sans-serif; box-shadow: inset 1px 1px 3px rgba(0,0,0,0.2);">{num}</div></div>'
    
    # Separador
    html_str += "<div style='font-size: 24px; color: rgba(0,0,0,0.3); font-weight: bold; margin: 0 5px;'>+</div>"
    
    # Super Balota (Cuerpo Amarillo, Círculo Blanco, Número Negro)
    html_str += f'<div style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #ffd32a 0%, #ffc048 60%, #ff9f1a 100%); box-shadow: 0 4px 8px rgba(0,0,0,0.25), inset -2px -2px 6px rgba(0,0,0,0.3); border: 1px solid #d35400;"><div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #ffffff; color: #1e272e !important; font-weight: 900; font-size: 14px; font-family: \'Inter\', sans-serif; box-shadow: inset 1px 1px 3px rgba(0,0,0,0.2);">{sb}</div></div>'
    
    html_str += "</div>"
    st.markdown(html_str, unsafe_allow_html=True)


def obtener_predicciones_markov_posicional(r):
    """Calcula la tabla de predicciones de Markov Posicional para el próximo sorteo."""
    if 'positional_matrices' not in r or 'last_combination' not in r:
        return pd.DataFrame()
        
    pos_top_data = []
    # Balotas principales
    for idx, col in enumerate(gb.COLUMNS_TO_ANALYZE):
        matrix = r['positional_matrices'][col]
        last_val = r['last_combination'][idx]
        if last_val in matrix.index:
            probs = matrix.loc[last_val].sort_values(ascending=False).head(3)
            for dest, prob in probs.items():
                if prob > 0:
                    pos_top_data.append({
                        'Posición': col,
                        'Último Número': int(last_val),
                        'Número Probable': int(dest),
                        'Probabilidad': float(prob)
                    })
    # Super Balota
    sb_matrix = r['positional_matrices'].get(gb.SUPER_BALOTA_COLUMN)
    if sb_matrix is not None and r['last_sb'] in sb_matrix.index:
        sb_probs = sb_matrix.loc[r['last_sb']].sort_values(ascending=False).head(3)
        for dest, prob in sb_probs.items():
            if prob > 0:
                pos_top_data.append({
                    'Posición': 'SB',
                    'Último Número': int(r['last_sb']),
                    'Número Probable': int(dest),
                    'Probabilidad': float(prob)
                })
                
    if not pos_top_data:
        return pd.DataFrame()
        
    return pd.DataFrame(pos_top_data)


# --- Carga de Datos y Procesamiento con Caché ---
FILE_PATH = 'baloto.json'

@st.cache_data
def cargar_y_analizar_datos(file_mtime):
    """Lee el archivo JSON de Baloto y ejecuta el análisis matemático."""
    if not os.path.exists(FILE_PATH):
        return None
    try:
        import json
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
        resultados = {}
        for s in ['Baloto', 'Revancha']:
            if s in data_json:
                df = pd.DataFrame(data_json[s])
                resultados[s] = gb.analizar_sorteo(s, df)
        return resultados
    except Exception as e:
        st.error(f"Error al analizar el archivo de datos: {e}")
        return None

# Obtener fecha de última modificación del archivo para invalidar la caché automáticamente si cambia
mtime = os.path.getmtime(FILE_PATH) if os.path.exists(FILE_PATH) else 0

# --- Ejecución de Carga Inicial ---
with st.spinner("Analizando historial y matrices de Markov con JAX..."):
    resultados_globales = cargar_y_analizar_datos(mtime)

# Detectar dispositivo de JAX para reporte en barra lateral
try:
    dispositivo_jax = jax.devices()[0].device_kind.upper()
except Exception:
    dispositivo_jax = "CPU"

# --- Panel Lateral (Sidebar) ---
st.sidebar.markdown("<h2 style='display: flex; align-items: center; justify-content: center; margin-bottom: 0;'><div style='display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #ff4d4d 0%, #ff1a1a 40%, #cc0000 100%); margin-right: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.2), inset -1px -1px 3px rgba(0,0,0,0.3); border: 1px solid #990000;'><div style='display: flex; align-items: center; justify-content: center; width: 16px; height: 16px; border-radius: 50%; background: #ffffff; color: #cc0000 !important; font-weight: 900; font-size: 10px; font-family: \"Inter\", sans-serif; box-shadow: inset 1px 1px 2px rgba(0,0,0,0.2);'>8</div></div>Controles</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Selector de Sorteo
tipo_sorteo = st.sidebar.radio(
    "Selecciona el sorteo:",
    options=["Baloto", "Revancha"],
    index=0
)

# Configurar combinaciones a generar
num_combinaciones = st.sidebar.slider(
    "Cantidad de combinaciones a generar:",
    min_value=5,
    max_value=25,
    value=10,
    step=1
)

st.sidebar.markdown("---")
# Caja informativa sobre hardware
st.sidebar.markdown(f"""
<div style="background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
    <span style="font-size: 11px; color: #64748b !important; display: block; font-weight: bold; margin-bottom: 2px;">MOTOR DE CÁLCULO</span>
    <span style="font-weight: 800; color: #16a34a !important; font-size: 14px;">⚡ JAX ({dispositivo_jax})</span>
</div>
""", unsafe_allow_html=True)

# Botón interactivo para recarga manual de datos
st.sidebar.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
if st.sidebar.button("🔄 Recargar Base de Datos", use_container_width=True):
    st.cache_data.clear()
    st.rerun()


# --- Contenido Principal ---
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 10px; margin-top: 10px;">
    <div style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%; background: radial-gradient(circle at 30% 30%, #ff4d4d 0%, #ff1a1a 40%, #cc0000 100%); box-shadow: 0 3px 6px rgba(0,0,0,0.2), inset -2px -2px 4px rgba(0,0,0,0.3); border: 1px solid #990000; margin-right: 12px; margin-top: 5px;"><div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #ffffff; color: #cc0000 !important; font-weight: 900; font-size: 14px; font-family: 'Inter', sans-serif; box-shadow: inset 1px 1px 3px rgba(0,0,0,0.2);">8</div></div>
    <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800;">GanaBaloto Web</h1>
</div>
<p style="color: #475569 !important; font-size: 1.1rem; margin-top: 0; margin-bottom: 30px;">
    Análisis estocástico y probabilístico de lotería mediante Cadenas de Markov.
</p>
""", unsafe_allow_html=True)

if not resultados_globales or tipo_sorteo not in resultados_globales:
    st.error("No se pudo cargar la base de datos de sorteos. Asegúrate de que `baloto.json` esté en la raíz del proyecto.")
else:
    r = resultados_globales[tipo_sorteo]
    
    # Calcular Score de referencia (Promedio, Mediana y Percentil 75 de ganadores históricos 5+1)
    df_ganadores_ref = gb.analizar_ganadores_historicos(r)
    if not df_ganadores_ref.empty:
        scores_ganadores = df_ganadores_ref['Score JAX'].astype(float).values
        score_meta = float(scores_ganadores.mean())
        score_mediana = float(np.median(scores_ganadores))
        score_p75 = float(np.percentile(scores_ganadores, 75))
    else:
        score_meta = 0.1450
        score_mediana = 0.1450
        score_p75 = 0.1550
    
    # Crear Pestañas principales (Premium layout)
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔮 Sugerencias Inteligentes", 
        "📝 Analizador Manual", 
        "📊 Métricas e Historial",
        "📘 Metodología y Guía"
    ])

    # -------------------------------------------------------------------------
    # PESTAÑA 1: SUGERENCIAS INTELIGENTES
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader(f"Predicciones para el próximo sorteo de {tipo_sorteo}")
        st.write("Estas combinaciones son generadas utilizando Cadenas de Markov (Global y Posicional) y filtradas mediante paridad, distribución de altos/bajos e intervalos de sumas más frecuentes en el historial.")

        with st.expander("ℹ️ ¿Cómo interpretar las sugerencias y puntajes?"):
            st.markdown(f"""
            * **Score JAX (Frecuencia):** Mide la popularidad histórica combinada de los números sugeridos. Un score alto indica que las balotas han salido frecuentemente. Las combinaciones marcadas con **🌟 ADN Ganador** tienen un score igual o superior al promedio histórico de los sorteos ganadores (`{score_meta:.4f}` en este sorteo).
            * **Markov Global:** Evalúa la probabilidad de que esta combinación completa ocurra en un solo sorteo según transiciones del histórico. Mayor probabilidad = combinación más natural estadísticamente.
            * **Markov Posicional:** Evalúa la transición con respecto al **último sorteo jugado** para cada posición. Mayor probabilidad = transición muy fluida y común desde los últimos números reales.
            """)

        # Score de referencia ya calculado globalmente

        col_ref_1, col_ref_2 = st.columns(2)
        with col_ref_1:
            st.info(f"🎯 **Umbrales Score JAX:** Mediana: `{score_mediana:.4f}` | P75: `{score_p75:.4f}` (Promedio: `{score_meta:.4f}`)")
        with col_ref_2:
            st.success(f"📅 **Último sorteo analizado:** `{' - '.join(map(str, r['last_combination']))} + SB({r['last_sb']})`")

        if st.button("🔮 Generar Combinaciones Sugeridas", type="primary"):
            with st.spinner("Simulando millones de transiciones matemáticas..."):
                # Obtener pesos dinámicos
                weights = gb.get_number_weights(r, gb.N_MAIN_BALLS, gb.N_SUPER_BALOTA)
                # Generar combinaciones probabilísticas
                combinaciones = gb.generate_probable_combinations(num_combinaciones, r, weights)

            if not combinaciones:
                st.warning("No se pudieron generar combinaciones válidas bajo los filtros actuales. Intenta nuevamente.")
            else:
                st.markdown("### Combinaciones Recomendadas:")
                for i, (comb, sb, score) in enumerate(combinaciones):
                    prob_m = gb.calculate_sequence_probability(comb, r['df_transition_matrix'])
                    
                    has_pos_markov = 'positional_matrices' in r
                    prob_pos = gb.calculate_positional_markov_probability(
                        comb, sb, r['positional_matrices'], r['last_combination'], r['last_sb']
                    ) if has_pos_markov else 0.0

                    es_estrella = score >= score_p75
                    es_bueno = score >= score_mediana and score < score_p75
                    
                    # Estructura de tarjeta para la combinación usando contenedores con borde
                    with st.container(border=True):
                        col_card_1, col_card_2, col_card_3 = st.columns([3, 2, 2])
                        with col_card_1:
                            prefix_text = ""
                            if es_estrella:
                                prefix_text = " 🌟 (ADN Premium)"
                            elif es_bueno:
                                prefix_text = " 👍 (Frecuencia Media)"
                            st.markdown(f"**Sugerencia #{i+1}**" + prefix_text)
                            render_balotas_html(comb, sb)
                        with col_card_2:
                            st.write(f"📊 **Score JAX:** `{score:.4f}`")
                            st.write(f"⛓️ **Markov Global:** `{prob_m:.8f}`")
                        with col_card_3:
                            st.write(f"🧩 **Markov Posicional:** `{prob_pos:.8f}`")
                            if es_estrella:
                                st.markdown("<span style='color: #16a34a !important; font-weight: bold;'>⭐ ADN Ganador Premium</span>", unsafe_allow_html=True)
                            elif es_bueno:
                                st.markdown("<span style='color: #3b82f6 !important; font-weight: bold;'>✔ Frecuente</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("<span style='color: #64748b !important; font-weight: bold;'>Estándar</span>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # PESTAÑA 2: ANALIZADOR MANUAL
    # -------------------------------------------------------------------------
    with tab2:
        st.subheader("Evalúa tu jugada favorita")
        st.write("Ingresa los números que tienes en mente para analizar si se alinean con los patrones matemáticos del historial de la lotería.")

        with st.expander("ℹ️ Guía rápida de análisis"):
            st.markdown(f"""
            Ingresa tu combinación favorita. El analizador calculará tres métricas clave:
            1. **Score JAX:** Compáralo con los umbrales históricos (Mediana: `{score_mediana:.4f}`, P75: `{score_p75:.4f}`). Si supera el P75, es de frecuencia premium.
            2. **Markov Global:** Una probabilidad mayor a `0` indica que las transiciones de números son factibles.
            3. **Markov Posicional:** Si es mayor a `0`, significa que la transición desde el último sorteo real es común y está respaldada por el histórico.
            """)

        # Entradas para la combinación
        col_in_1, col_in_2, col_in_3, col_in_4, col_in_5, col_in_sb = st.columns(6)
        with col_in_1: num1 = st.number_input("Balota 1", min_value=1, max_value=gb.N_MAIN_BALLS, value=1, step=1)
        with col_in_2: num2 = st.number_input("Balota 2", min_value=1, max_value=gb.N_MAIN_BALLS, value=2, step=1)
        with col_in_3: num3 = st.number_input("Balota 3", min_value=1, max_value=gb.N_MAIN_BALLS, value=3, step=1)
        with col_in_4: num4 = st.number_input("Balota 4", min_value=1, max_value=gb.N_MAIN_BALLS, value=4, step=1)
        with col_in_5: num5 = st.number_input("Balota 5", min_value=1, max_value=gb.N_MAIN_BALLS, value=5, step=1)
        with col_in_sb: input_sb = st.number_input("Super Balota", min_value=1, max_value=gb.N_SUPER_BALOTA, value=1, step=1)

        lista_ingresada = [num1, num2, num3, num4, num5]
        # Validar duplicados en las entradas
        duplicados = len(lista_ingresada) != len(set(lista_ingresada))

        if duplicados:
            st.error("❌ Error: No puedes ingresar números repetidos en las balotas principales.")
        else:
            if st.button("📊 Analizar Mi Jugada", type="secondary"):
                jugada_ordenada = sorted(lista_ingresada)
                
                # JAX Score
                score = float(gb.calculate_frequency_score_jax(
                    jax.numpy.array(jugada_ordenada), jax.numpy.array(input_sb),
                    r['b_cols_jax'], r['sb_col_jax'], r['total_draws_jax_val']
                ))
                
                # Markov global
                prob_m = gb.calculate_sequence_probability(jugada_ordenada, r['df_transition_matrix'])
                
                # Markov posicional
                prob_pos = 0.0
                if 'positional_matrices' in r:
                    prob_pos = gb.calculate_positional_markov_probability(
                        jugada_ordenada, input_sb, r['positional_matrices'], r['last_combination'], r['last_sb']
                    )

                st.markdown("---")
                st.markdown("### Diagnóstico de tu jugada:")
                render_balotas_html(jugada_ordenada, input_sb)
                
                col_m_1, col_m_2, col_m_3 = st.columns(3)
                
                with col_m_1:
                    st.metric(
                        label="Score JAX (Frecuencia)",
                        value=f"{score:.4f}",
                        delta=f"{(score - score_mediana):.4f} vs Mediana",
                        help="El Score JAX mide la frecuencia ponderada de los números elegidos en base a la matriz de sorteos históricos."
                    )
                    if score >= score_p75:
                        status_text = "Excelente (ADN Ganador Premium). Tus números tienen una frecuencia acumulada excepcionalmente alta."
                    elif score >= score_mediana:
                        status_text = "Frecuente. Tus números están en el rango promedio del histórico de combinaciones ganadoras."
                    else:
                        status_text = "Bajo el promedio. Juegas con combinaciones de balotas menos comunes en el histórico."
                    
                    st.markdown(f"""
                    * **Interpretación:** {status_text}
                    """)
                with col_m_2:
                    st.metric(
                        label="Probabilidad de Markov Global",
                        value=f"{prob_m:.8f}",
                        help="Mide la probabilidad de que esta secuencia de 5 números aparezca junta en un sorteo, basándose en la matriz de transición general."
                    )
                    st.markdown("""
                    * **Interpretación:** Evalúa si es normal que estos números salgan juntos en un mismo sorteo en base a transiciones previas.
                    """)
                with col_m_3:
                    st.metric(
                        label="Markov Posicional (Sorteo Anterior)",
                        value=f"{prob_pos:.8f}",
                        help="Calcula la probabilidad de que ocurra esta transición exacta desde el último sorteo de lotería real, posición por posición."
                    )
                    st.markdown(f"""
                    * **Interpretación:** {"Transición factible con respecto al último sorteo." if prob_pos > 0 else "Transición no registrada con respecto al sorteo anterior."}
                    """)

    # -------------------------------------------------------------------------
    # PESTAÑA 3: MÉTRICAS E HISTORIAL
    # -------------------------------------------------------------------------
    with tab3:
        st.subheader("Tendencias Históricas y Estadísticas")
        st.write("Análisis detallado de frecuencias acumuladas, números calientes y fríos obtenidos directamente de la base de datos.")

        with st.expander("ℹ️ ¿Qué significan estas estadísticas y tendencias?"):
            st.markdown("""
            * **ADN de Ganadores Históricos (5+1):** Listado completo de sorteos donde se entregó el premio mayor. Muestra las métricas que tenían las combinaciones ganadoras en ese momento real.
            * **Predicciones de Markov Posicional:** Indica cuáles son los números más probables de salir en el próximo sorteo para cada balota (B1 a B5 y la Super Balota SB) de acuerdo con los números exactos del sorteo anterior.
            * **Números Calientes / Fríos:** Los calientes son los que tienen mayor racha de aparición reciente; los fríos son los que llevan más tiempo sin salir.
            * **Prueba de Aleatoriedad Chi-cuadrado:** Determina si la lotería se comporta de forma puramente aleatoria (p-value > 0.05) o si el histórico presenta sesgos o patrones de frecuencia.
            """)

        st.markdown(f"### 🏆 ADN de Ganadores Históricos (5+1) - {tipo_sorteo}")
        df_ganadores = gb.analizar_ganadores_historicos(r)
        if not df_ganadores.empty:
            st.dataframe(df_ganadores.astype(str), hide_index=True, width='stretch')
        else:
            st.info(f"No se registraron sorteos con ganadores del acumulado (5+1) en el historial de {tipo_sorteo}.")

        st.markdown("---")

        st.markdown(f"### 🔮 Predicciones de Markov Posicional (Próximo Sorteo) - {tipo_sorteo}")
        st.write("Predicciones de transiciones de números más probables por cada posición, calculadas a partir del último sorteo jugado.")
        df_pos = obtener_predicciones_markov_posicional(r)
        if not df_pos.empty:
            df_pos_show = df_pos.copy()
            df_pos_show['Probabilidad'] = df_pos_show['Probabilidad'].map(lambda x: f"{x:.4f}")
            st.dataframe(df_pos_show.astype(str), hide_index=True, width='stretch')
        else:
            st.info("No hay suficientes datos de transición posicional para realizar predicciones.")

        st.markdown("---")

        col_hist_1, col_hist_2 = st.columns(2)

        with col_hist_1:
            st.markdown("### 🔥 Números Calientes")
            st.write(f"Los números que más han salido en las últimas {gb.RECENT_DRAWS_THRESHOLD} balotas.")
            df_hot = r['df_hot_numbers'].astype(str).reset_index().rename(columns={'index': 'Balota'})
            st.dataframe(df_hot, hide_index=True, width='stretch')

            st.markdown("### 🎲 Prueba de Aleatoriedad Chi-cuadrado")
            st.write("Determina si la distribución de apariciones de las balotas es puramente aleatoria (p > 0.05) o presenta sesgos históricos.")
            st.dataframe(r['df_chi2'], width='stretch')

        with col_hist_2:
            st.markdown("### ❄️ Números Fríos")
            st.write("Los números con mayor tiempo sin aparecer en los sorteos.")
            df_cold = r['df_cold_numbers'].astype(str).reset_index().rename(columns={'index': 'Balota'})
            st.dataframe(df_cold, hide_index=True, width='stretch')

            st.markdown("### ⚖️ Distribución de Paridad y Altos/Bajos")
            col_p_1, col_p_2 = st.columns(2)
            with col_p_1:
                st.markdown("**Paridad (Pares, Impares)**")
                st.dataframe(r['df_parity_frequencies'].head(5), width='stretch')
            with col_p_2:
                st.markdown("**Bajos vs Altos**")
                st.dataframe(r['df_low_high_frequencies'].head(5), width='stretch')

    # -------------------------------------------------------------------------
    # PESTAÑA 4: METODOLOGÍA Y GUÍA
    # -------------------------------------------------------------------------
    with tab4:
        st.subheader("📚 Guía Teórica y Metodológica de GanaBaloto")
        st.write("Esta aplicación utiliza modelos estocásticos, cadenas de Markov y análisis de frecuencias acelerado por GPU para analizar y optimizar jugadas de lotería.")
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            with st.container(border=True):
                st.markdown("""
                ### ⚡ Computación Acelerada con JAX
                Para calcular el **Score JAX**, el sistema mapea la frecuencia con la que cada número ha aparecido en el histórico. 
                * **¿Por qué JAX?** JAX nos permite paralelizar las búsquedas de frecuencias sobre millones de registros y combinaciones posibles en microsegundos, ejecutando operaciones matemáticas de álgebra lineal directamente en la GPU (si está disponible) o mediante CPU optimizada vectorialmente.
                * **El Score:** Es el promedio de las frecuencias relativas de aparición de las 5 balotas principales y la super balota elegida.
                """)
                
            with st.container(border=True):
                st.markdown("""
                ### ⚖️ Filtros Estadísticos del ADN Ganador
                Para reducir el espacio de búsqueda de millones de combinaciones posibles a solo aquellas viables, la aplicación aplica tres filtros del "ADN histórico":
                1. **Frecuencia de Suma:** Las sumas de las combinaciones sugeridas deben caer dentro del intervalo del 80% más frecuente en los sorteos históricos.
                2. **Distribución Par/Impar:** Se evitan combinaciones de puros pares o impares, sugiriendo distribuciones más probables (ej. 3 pares y 2 impares).
                3. **Bajos vs Altos:** Se distribuyen las balotas de forma balanceada entre los números bajos (1-21) y altos (22-43).
                """)
                
        with col_t2:
            with st.container(border=True):
                st.markdown("""
                ### ⛓️ Cadenas de Markov
                Una **Cadena de Markov** es un modelo estocástico donde la probabilidad de que ocurra un evento depende únicamente del estado inmediatamente anterior.
                
                #### 🌍 1. Markov Global
                * Analiza la secuencia de balotas consecutivas dentro de un mismo sorteo.
                * Permite construir una **Matriz de Transición** general que mide qué tan probable es que el número $X$ ocurra al lado del número $Y$.
                
                #### 📍 2. Markov Posicional
                * Analiza cómo evoluciona cada balota individualmente de un sorteo al siguiente.
                * Si en el sorteo anterior la balota en la Posición 1 fue el número $A$, la matriz de transición posicional calcula la probabilidad de que en el sorteo actual la balota de la Posición 1 sea el número $B$.
                """)

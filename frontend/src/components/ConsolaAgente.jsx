import { useState } from 'react';

export default function ConsolaAgente() {
  const [triggerInput, setTriggerInput] = useState('PRONOSTICO');
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('visual'); // 'visual' o 'markdown'
  const [copiado, setCopiado] = useState(false);

  const ejecutarTrigger = async (palabra) => {
    const cmd = (palabra || triggerInput).trim();
    if (!cmd) return;

    setLoading(true);
    setError(null);
    setCopiado(false);

    try {
      const response = await fetch('/api/agente/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trigger: cmd })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Error al ejecutar el agente local');
      }

      setResultado(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copiarMarkdown = () => {
    if (!resultado?.markdown) return;
    navigator.clipboard.writeText(resultado.markdown);
    setCopiado(true);
    setTimeout(() => setCopiado(false), 2500);
  };

  const datos = resultado?.datos;
  const sorteoInfo = datos?.sorteo_info;
  const balotoJugadas = datos?.baloto?.jugadas || [];
  const revanchaJugadas = datos?.revancha?.jugadas || [];
  const auditB = datos?.auditoria_top1?.baloto;
  const auditR = datos?.auditoria_top1?.revancha;
  const rueda = datos?.rueda_reducida;

  return (
    <div>
      {/* Tarjeta de Disparador Rápido (Trigger) */}
      <div className="card" style={{ borderTop: '3px solid var(--accent-blue)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <h3 className="card-title" style={{ margin: 0 }}>Consola de Ejecución de Agentes Locales</h3>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 18px 0' }}>
          Ingresa la <strong>palabra activadora (Trigger Keyword)</strong> para invocar la skill predictiva del agente, compilar en JAX GPU y calcular el pronóstico oficial estandarizado en 4 secciones.
        </p>

        {/* Barra de Entrada y Botón de Disparo */}
        <form onSubmit={(e) => { e.preventDefault(); ejecutarTrigger(); }} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '14px' }}>
          <input
            type="text"
            value={triggerInput}
            onChange={(e) => setTriggerInput(e.target.value.toUpperCase())}
            placeholder="Escribe 'PRONOSTICO', 'JUGADAS' o 'GANABALOTO'..."
            disabled={loading}
            style={{
              flex: '1 1 300px',
              padding: '12px 16px',
              fontSize: '1rem',
              fontWeight: '700',
              letterSpacing: '1px',
              borderRadius: '8px',
              border: '2px solid var(--accent-blue)',
              background: 'rgba(59, 130, 246, 0.05)',
              color: 'var(--text-primary)'
            }}
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ padding: '12px 24px', fontSize: '1rem', fontWeight: '800' }}
          >
            {loading ? 'Ejecutando Agente...' : 'Disparar Agente Local'}
          </button>
        </form>

        {/* Botones de Atajos Rápidos */}
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'bold' }}>Triggers oficiales:</span>
          {['PRONOSTICO', 'JUGADAS', 'GANABALOTO'].map((trig) => (
            <button
              key={trig}
              onClick={() => { setTriggerInput(trig); ejecutarTrigger(trig); }}
              disabled={loading}
              style={{
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--border-color)',
                borderRadius: '6px',
                padding: '4px 12px',
                fontSize: '0.8rem',
                color: 'var(--text-primary)',
                fontWeight: '700',
                cursor: 'pointer',
                transition: 'all 0.2s'
              }}
            >
              {trig}
            </button>
          ))}
        </div>
      </div>

      {/* Animación y Feedback de Carga */}
      {loading && (
        <div className="loading-container" style={{ marginTop: '20px' }}>
          <div className="spinner"></div>
          <p style={{ fontWeight: '700', color: 'var(--accent-blue)', fontSize: '1.05rem', margin: '10px 0 4px 0' }}>
            Invocando skill: baloto-analisis-predictivo
          </p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            Calculando matrices estocásticas en JAX (NVIDIA GeForce GPU), supervivencia de Weibull, energía de Ising y Rueda Wheeling Greedy...
          </p>
        </div>
      )}

      {/* Manejo de Error */}
      {error && (
        <div className="alert alert-error" style={{ marginTop: '20px' }}>
          <span>Error de ejecución: {error}</span>
        </div>
      )}

      {/* Resultados de la Ejecución del Agente */}
      {resultado && !loading && (
        <div style={{ marginTop: '24px' }}>
          {/* Barra de Control de Vistas */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className={`tab-btn ${viewMode === 'visual' ? 'active' : ''}`}
                onClick={() => setViewMode('visual')}
                style={{ padding: '6px 16px', fontSize: '0.9rem' }}
              >
                Vista Interactiva Oficial
              </button>
              <button
                className={`tab-btn ${viewMode === 'markdown' ? 'active' : ''}`}
                onClick={() => setViewMode('markdown')}
                style={{ padding: '6px 16px', fontSize: '0.9rem' }}
              >
                Salida Markdown de Consola
              </button>
            </div>

            <button
              onClick={copiarMarkdown}
              className="btn btn-secondary"
              style={{ fontSize: '0.85rem', padding: '6px 14px' }}
            >
              {copiado ? 'Copiado al portapapeles' : 'Copiar Reporte Completo'}
            </button>
          </div>

          {/* VISTA 1: INTERACTIVA ESTRUCTURADA (4 SECCIONES REGLAMENTARIAS) */}
          {viewMode === 'visual' && datos && (
            <div>
              {/* Cabecera de Entorno */}
              <div className="card" style={{ background: 'rgba(59, 130, 246, 0.05)', borderColor: 'rgba(59, 130, 246, 0.2)', marginBottom: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>
                      Sorteo Oficial Objetivo
                    </span>
                    <h2 style={{ fontSize: '1.4rem', margin: '4px 0', color: 'var(--text-primary)' }}>
                      #{sorteoInfo?.num_sorteo} — {sorteoInfo?.fecha_legible}
                    </h2>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                      Anclajes: Día {sorteoInfo?.dia < 10 ? `0${sorteoInfo?.dia}` : sorteoInfo?.dia} | Mes {sorteoInfo?.mes < 10 ? `0${sorteoInfo?.mes}` : sorteoInfo?.mes} | Suma Sorteo {sorteoInfo?.suma_sorteo} | Suma Día+Mes: {sorteoInfo?.suma_dia_mes}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '16px' }}>
                    <div className="engine-box" style={{ margin: 0 }}>
                      <span className="engine-title">Motor Acelerado</span>
                      <span className="engine-value">JAX (NVIDIA GPU)</span>
                    </div>
                    <div className="engine-box" style={{ margin: 0, background: 'rgba(34, 197, 94, 0.08)' }}>
                      <span className="engine-title">Trigger Utilizado</span>
                      <span className="engine-value" style={{ color: 'var(--accent-green)' }}>{resultado.trigger_ejecutado}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* SECCION 1: BALOTO */}
              <div className="card" style={{ marginBottom: '24px' }}>
                <h3 className="card-title">
                  1. Pronósticos Recomendados: Baloto
                </h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '14px' }}>
                  Meta histórica de ganadores (Score JAX): <strong>&ge; {datos.baloto?.score_meta?.toFixed(4)}</strong> | Criterio Perfil Óptimo: <strong>&ge; 70.0</strong>
                </p>

                <div className="table-responsive">
                  <table className="styled-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Combinación</th>
                        <th>Suma</th>
                        <th>Índice</th>
                        <th>JAX</th>
                        <th>Gauss</th>
                        <th>Entropía</th>
                        <th>Hazard</th>
                        <th>Insignias</th>
                      </tr>
                    </thead>
                    <tbody>
                      {balotoJugadas.map((j, idx) => (
                        <tr key={idx} style={{ background: idx === 0 ? 'rgba(234, 179, 8, 0.04)' : 'transparent' }}>
                          <td><strong>{idx + 1}</strong></td>
                          <td>
                            <strong style={{ fontFamily: 'monospace', fontSize: '1rem', color: 'var(--text-primary)' }}>
                              {j.comb.map(x => x < 10 ? `0${x}` : x).join('-')}
                            </strong>
                            {' '}+{' '}
                            <span style={{ background: 'var(--accent-yellow)', color: '#0f172a', fontWeight: '800', padding: '2px 6px', borderRadius: '4px', fontSize: '0.85rem' }}>
                              [{j.sb < 10 ? `0${j.sb}` : j.sb}]
                            </span>
                          </td>
                          <td><strong>{j.suma}</strong></td>
                          <td style={{ color: j.indice >= 70 ? 'var(--accent-green)' : 'var(--accent-blue)', fontWeight: '800', fontSize: '1.05rem' }}>
                            {j.indice.toFixed(1)}
                          </td>
                          <td><code>{j.jax.toFixed(4)}</code></td>
                          <td>{j.gauss.toFixed(2)}</td>
                          <td>{j.entropia.toFixed(2)}</td>
                          <td>{j.hazard.toFixed(2)}</td>
                          <td>
                            <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                              {idx === 0 && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(234, 179, 8, 0.2)', color: '#b45309', padding: '2px 6px', borderRadius: '4px' }}>Top #1</span>}
                              {j.es_optimo && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(34, 197, 94, 0.2)', color: '#15803d', padding: '2px 6px', borderRadius: '4px' }}>Óptimo</span>}
                              {j.tiene_adn && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(59, 130, 246, 0.2)', color: '#1d4ed8', padding: '2px 6px', borderRadius: '4px' }}>ADN</span>}
                              {j.coinc_fecha?.length > 0 && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Fecha</span>}
                              {j.coinc_lag8?.length > 0 && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Lag-8</span>}
                              {j.es_espejo && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Espejo</span>}
                              {j.tiene_salto && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Delta</span>}
                              {j.tiene_ising && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Ising</span>}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* SECCION 2: REVANCHA */}
              <div className="card" style={{ marginBottom: '24px' }}>
                <h3 className="card-title">
                  2. Pronósticos Recomendados: Revancha
                </h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '14px' }}>
                  Meta histórica de ganadores (Score JAX): <strong>&ge; {datos.revancha?.score_meta?.toFixed(4)}</strong> | Criterio Perfil Óptimo: <strong>&ge; 70.0</strong>
                </p>

                <div className="table-responsive">
                  <table className="styled-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Combinación</th>
                        <th>Suma</th>
                        <th>Índice</th>
                        <th>JAX</th>
                        <th>Gauss</th>
                        <th>Entropía</th>
                        <th>Hazard</th>
                        <th>Insignias</th>
                      </tr>
                    </thead>
                    <tbody>
                      {revanchaJugadas.map((j, idx) => (
                        <tr key={idx} style={{ background: idx === 0 ? 'rgba(234, 179, 8, 0.04)' : 'transparent' }}>
                          <td><strong>{idx + 1}</strong></td>
                          <td>
                            <strong style={{ fontFamily: 'monospace', fontSize: '1rem', color: 'var(--text-primary)' }}>
                              {j.comb.map(x => x < 10 ? `0${x}` : x).join('-')}
                            </strong>
                            {' '}+{' '}
                            <span style={{ background: 'var(--accent-yellow)', color: '#0f172a', fontWeight: '800', padding: '2px 6px', borderRadius: '4px', fontSize: '0.85rem' }}>
                              [{j.sb < 10 ? `0${j.sb}` : j.sb}]
                            </span>
                          </td>
                          <td><strong>{j.suma}</strong></td>
                          <td style={{ color: j.indice >= 70 ? 'var(--accent-green)' : 'var(--accent-blue)', fontWeight: '800', fontSize: '1.05rem' }}>
                            {j.indice.toFixed(1)}
                          </td>
                          <td><code>{j.jax.toFixed(4)}</code></td>
                          <td>{j.gauss.toFixed(2)}</td>
                          <td>{j.entropia.toFixed(2)}</td>
                          <td>{j.hazard.toFixed(2)}</td>
                          <td>
                            <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                              {idx === 0 && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(234, 179, 8, 0.2)', color: '#b45309', padding: '2px 6px', borderRadius: '4px' }}>Top #1</span>}
                              {j.es_optimo && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(34, 197, 94, 0.2)', color: '#15803d', padding: '2px 6px', borderRadius: '4px' }}>Óptimo</span>}
                              {j.tiene_adn && <span style={{ fontSize: '0.7rem', fontWeight: 'bold', background: 'rgba(59, 130, 246, 0.2)', color: '#1d4ed8', padding: '2px 6px', borderRadius: '4px' }}>ADN</span>}
                              {j.coinc_fecha?.length > 0 && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Fecha</span>}
                              {j.coinc_lag8?.length > 0 && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Lag-8</span>}
                              {j.es_espejo && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Espejo</span>}
                              {j.tiene_salto && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Delta</span>}
                              {j.tiene_ising && <span style={{ fontSize: '0.7rem', background: 'rgba(0,0,0,0.06)', color: 'var(--text-primary)', padding: '2px 6px', borderRadius: '4px' }}>Ising</span>}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* SECCION 3: AUDITORIA DETALLADA */}
              <div className="grid-2" style={{ gap: '16px', marginBottom: '24px' }}>
                {auditB && (
                  <div className="card">
                    <h4 className="card-title" style={{ color: 'var(--accent-yellow)' }}>
                      Auditoría Top #1 Baloto
                    </h4>
                    <ul style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px', margin: 0 }}>
                      <li><strong>{auditB.desc_suma}</strong></li>
                      <li><strong>{auditB.desc_entr}</strong></li>
                      <li><strong>{auditB.desc_jax}</strong></li>
                      <li><strong>{auditB.desc_sb}</strong></li>
                      <li><strong>{auditB.desc_anclaje}</strong></li>
                      <li><strong>{auditB.desc_haz}</strong></li>
                      <li><strong>{auditB.desc_ising}</strong></li>
                    </ul>
                  </div>
                )}

                {auditR && (
                  <div className="card">
                    <h4 className="card-title" style={{ color: 'var(--accent-yellow)' }}>
                      Auditoría Top #1 Revancha
                    </h4>
                    <ul style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px', margin: 0 }}>
                      <li><strong>{auditR.desc_suma}</strong></li>
                      <li><strong>{auditR.desc_entr}</strong></li>
                      <li><strong>{auditR.desc_jax}</strong></li>
                      <li><strong>{auditR.desc_sb}</strong></li>
                      <li><strong>{auditR.desc_anclaje}</strong></li>
                      <li><strong>{auditR.desc_haz}</strong></li>
                      <li><strong>{auditR.desc_ising}</strong></li>
                    </ul>
                  </div>
                )}
              </div>

              {/* SECCION 4: RUEDA REDUCIDA */}
              {rueda && (
                <div className="card">
                  <h3 className="card-title">
                    4. Rueda Combinatoria Reducida (Wheeling System)
                  </h3>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '14px' }}>
                    Selección de <strong>{rueda.numeros_pool?.length} números clave</strong> ({rueda.numeros_pool?.map(x => x < 10 ? `0${x}` : x).join(', ')}) cruzados con Super Balotas líderes con <strong>garantía matemática de {rueda.garantia} aciertos</strong> en solo <strong>{rueda.total_tiquetes} tiquetes</strong>:
                  </p>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '10px' }}>
                    {rueda.tiquetes?.map((t, idx) => (
                      <div key={idx} style={{
                        background: 'var(--bg-card-subtle)',
                        border: '1px solid var(--border-color)',
                        borderRadius: '8px',
                        padding: '10px 14px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center'
                      }}>
                        <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: 'var(--text-muted)' }}>
                          Tiquete #{idx + 1 < 10 ? `0${idx + 1}` : idx + 1}:
                        </span>
                        <div>
                          <strong style={{ fontFamily: 'monospace', fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                            {t.comb.map(x => x < 10 ? `0${x}` : x).join(' - ')}
                          </strong>
                          {' '}+{' '}
                          <span style={{ background: 'var(--accent-yellow)', color: '#0f172a', fontWeight: '800', padding: '1px 5px', borderRadius: '4px', fontSize: '0.8rem' }}>
                            [{t.sb < 10 ? `0${t.sb}` : t.sb}]
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* VISTA 2: MARKDOWN PLANO OFICIAL */}
          {viewMode === 'markdown' && (
            <div className="card">
              <pre style={{
                background: '#090d16',
                color: '#e2e8f0',
                padding: '20px',
                borderRadius: '8px',
                overflowX: 'auto',
                fontSize: '0.88rem',
                lineHeight: '1.6',
                fontFamily: 'monospace',
                whiteSpace: 'pre-wrap'
              }}>
                {resultado.markdown}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

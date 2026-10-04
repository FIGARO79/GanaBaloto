import { useState } from 'react';

const formatProb = (val) => {
  if (val === undefined || val === null) return '0.000000';
  const num = Number(val);
  if (num === 0) return '0.000000';
  if (num < 1e-5) {
    return num.toExponential(3);
  }
  return num.toFixed(6);
};

export default function Sugerencias({ sorteo, scoreMediana, scoreP75, scoreMeta = 0.1495 }) {
  const [cantidad, setCantidad] = useState(10);
  const [combinaciones, setCombinaciones] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generarSugerencias = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/generar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sorteo: sorteo,
          cantidad: cantidad
        })
      });
      if (!response.ok) {
        throw new Error('Error al generar combinaciones');
      }
      const data = await response.json();
      setCombinaciones(data.combinaciones || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h3 className="card-title">Generador Estocástico Multimodelo: {sorteo}</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 16px 0' }}>
          Simula millones de combinaciones con aceleración JAX y las califica mediante <strong>7 modelos estocásticos</strong> (Weibull, Ising, Gauss, Entropía, Dirichlet-Bayes, Markov y Regímenes HMM).
        </p>

        <div className="alert alert-info" style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '0.9rem', lineHeight: '1.6' }}>
            <strong>Guía de Interpretación Multidimensional:</strong>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '8px', marginTop: '8px' }}>
              <div>• <strong>Índice Compuesto:</strong> Promedio continuo (0 a 100).</div>
              <div>• <strong>Weibull (H):</strong> Ventana de madurez óptima (8–14 sorteos).</div>
              <div>• <strong>Ising (J):</strong> Co-ocurrencia por acoplamiento pareado.</div>
              <div>• <strong>Gauss / Entropía:</strong> Suma normalizada y dispersión espacial.</div>
            </div>
          </div>
        </div>

        <div className="slider-container" style={{ margin: '20px 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: '600' }}>Cantidad de combinaciones a optimizar:</span>
            <span className="slider-val" style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-blue)' }}>{cantidad}</span>
          </div>
          <input
            type="range"
            min="5"
            max="25"
            value={cantidad}
            onChange={(e) => setCantidad(parseInt(e.target.value))}
            className="range-slider"
          />
        </div>

        <button onClick={generarSugerencias} className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
          {loading ? 'Simulando en JAX con GPU...' : 'Generar Combinaciones Optimizadas'}
        </button>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Ejecutando filtrado estocástico en GPU, cálculo de matrices Ising y supervivencia Weibull...</p>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <span>Error: {error}</span>
        </div>
      )}

      {combinaciones.length > 0 && !loading && (
        <div style={{ marginTop: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 className="card-title" style={{ margin: 0 }}>Combinaciones Recomendadas (Top {combinaciones.length}):</h3>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Ordenadas por Índice Compuesto descendente</span>
          </div>

          {combinaciones.map((item, index) => {
            const composite = item.composite || 50;
            const insignias = item.insignias || [];
            const suma = item.suma || item.combinacion.reduce((a, b) => a + b, 0);

            return (
              <div key={index} className="card" style={{ marginBottom: '16px', borderLeft: index === 0 ? '4px solid var(--accent-yellow)' : composite >= 70 ? '4px solid var(--accent-green)' : '1px solid var(--border-color)' }}>
                <div className="sugerencia-card-container">
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '800', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                        JUGADA #{index + 1}
                      </span>
                      {insignias.map((ins, i) => (
                        <span key={i} style={{
                          fontSize: '0.75rem',
                          fontWeight: '700',
                          padding: '3px 8px',
                          borderRadius: '12px',
                          background: ins.includes('Top') ? 'rgba(234, 179, 8, 0.15)' : ins.includes('ADN') ? 'rgba(34, 197, 94, 0.15)' : 'rgba(59, 130, 246, 0.12)',
                          color: ins.includes('Top') ? '#eab308' : ins.includes('ADN') ? '#22c55e' : '#60a5fa',
                          border: '1px solid rgba(255, 255, 255, 0.1)'
                        }}>
                          {ins}
                        </span>
                      ))}
                    </div>

                    <div className="balotas-container" style={{ margin: '10px 0 16px 0' }}>
                      {item.combinacion.map((num, i) => (
                        <div key={i} className="balota balota-principal">
                          <div className="balota-inner">{num < 10 ? `0${num}` : num}</div>
                        </div>
                      ))}
                      <div className="balota-separator">+</div>
                      <div className="balota balota-super">
                        <div className="balota-inner">{item.sb < 10 ? `0${item.sb}` : item.sb}</div>
                      </div>
                    </div>
                    
                    {/* Barra de progreso de Índice Compuesto */}
                    <div style={{ background: 'var(--bg-card-subtle)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                        <span>Índice Compuesto Global (Suma: {suma})</span>
                        <span style={{ color: composite >= 70 ? 'var(--accent-green)' : 'var(--accent-blue)', fontSize: '1rem' }}>
                          {composite.toFixed(1)} / 100
                        </span>
                      </div>
                      <div style={{ height: '7px', width: '100%', background: 'rgba(0,0,0,0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                        <div style={{
                          height: '100%',
                          width: `${Math.min(100, composite)}%`,
                          background: composite >= 70 ? 'var(--accent-green)' : composite >= 60 ? 'var(--accent-blue)' : 'var(--accent-yellow)',
                          transition: 'width 0.4s ease'
                        }}></div>
                      </div>
                    </div>
                  </div>

                  {/* Panel con los 7 scores analíticos */}
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', minWidth: '320px', background: 'var(--bg-card-subtle)', padding: '14px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                    <div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Score JAX</div>
                      <div style={{ fontSize: '0.95rem', fontWeight: '700', color: item.score >= scoreMeta ? 'var(--accent-green)' : 'var(--text-primary)' }}>
                        {item.score.toFixed(4)}
                      </div>
                    </div>

                    <div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Afinidad Ising</div>
                      <div style={{ fontSize: '0.95rem', fontWeight: '700', color: (item.score_ising || 0.5) >= 0.52 ? 'var(--accent-yellow)' : 'var(--text-primary)' }}>
                        {(item.score_ising || 0.5).toFixed(2)}
                      </div>
                    </div>

                    <div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Gauss & Entropía</div>
                      <div style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                        G: {(item.score_gauss || 0).toFixed(2)} | E: {(item.score_entropy || 0).toFixed(2)}
                      </div>
                    </div>

                    <div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Weibull Hazard</div>
                      <div style={{ fontSize: '0.9rem', fontWeight: '600', color: (item.score_hazard || 0) >= 0.65 ? 'var(--accent-green)' : 'var(--text-primary)' }}>
                        {(item.score_hazard || 0).toFixed(2)}
                      </div>
                    </div>

                    <div style={{ gridColumn: 'span 2', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '6px' }}>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: '700' }}>Bayes & Markov</div>
                      <div style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-secondary)' }}>
                        Bayes: {(item.score_bayes || 0).toFixed(2)} | Trans: {formatProb(item.prob_m)}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

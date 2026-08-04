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

export default function Sugerencias({ sorteo, scoreMediana, scoreP75 }) {
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

  const getScoreBadge = (score) => {
    if (score >= scoreP75) {
      return { text: '⭐ ADN Ganador Premium', class: 'text-success', style: { color: 'var(--accent-green)', fontWeight: 'bold' } };
    } else if (score >= scoreMediana) {
      return { text: '✔ Frecuente', class: 'text-blue', style: { color: 'var(--accent-blue)', fontWeight: 'bold' } };
    } else {
      return { text: 'Estándar', class: 'text-muted', style: { color: 'var(--text-muted)' } };
    }
  };

  return (
    <div>
      <div className="card">
        <h3 className="card-title">Predicciones para el próximo sorteo de {sorteo}</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 20px 0' }}>
          Estas combinaciones son generadas utilizando Cadenas de Markov (Global y Posicional) y filtradas mediante paridad, distribución de altos/bajos e intervalos de sumas más frecuentes en el historial.
        </p>

        <div className="alert alert-info">
          <div>
            <strong>💡 ¿Cómo interpretar las sugerencias y métricas multimodelo?</strong>
            <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px' }}>
              <li><strong>Índice Compuesto (0 - 100):</strong> Evalúa de forma unificada 6 dimensiones (JAX, Markov, Gauss, Bayes, Hazard y Entropía).</li>
              <li><strong>Suma Gaussiana & Entropía:</strong> Garantizan que la combinación no sea un patrón artificial y tenga la variabilidad estructural ideal.</li>
              <li><strong>Inferencia Bayesiana & Hazard Rate:</strong> Incorporan la probabilidad a posteriori y la "presión estadística" de números atrasados.</li>
            </ul>
          </div>
        </div>

        <div className="slider-container" style={{ margin: '24px 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: '600' }}>Cantidad de combinaciones a generar:</span>
            <span className="slider-val">{cantidad}</span>
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
          {loading ? 'Simulando transiciones...' : '🔮 Generar Combinaciones Sugeridas'}
        </button>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Simulando millones de transiciones estocásticas y modelos Bayesianos con JAX...</p>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <span>❌ Error: {error}</span>
        </div>
      )}

      {combinaciones.length > 0 && !loading && (
        <div>
          <h3 className="card-title" style={{ marginBottom: '16px' }}>Combinaciones Recomendadas:</h3>
          {combinaciones.map((item, index) => {
            const badge = getScoreBadge(item.score);
            const composite = item.composite || 50;
            return (
              <div key={index} className="card">
                <div className="sugerencia-card-container">
                  <div>
                    <span style={{ fontWeight: '700', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      SUGERENCIA #{index + 1} {item.score >= scoreP75 && '🌟 (ADN Premium)'} {item.score >= scoreMediana && item.score < scoreP75 && '👍 (Frecuencia Media)'}
                    </span>
                    <div className="balotas-container" style={{ margin: '10px 0 16px 0' }}>
                      {item.combinacion.map((num, i) => (
                        <div key={i} className="balota balota-principal">
                          <div className="balota-inner">{num}</div>
                        </div>
                      ))}
                      <div className="balota-separator">+</div>
                      <div className="balota balota-super">
                        <div className="balota-inner">{item.sb}</div>
                      </div>
                    </div>
                    
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                        <span>Índice Compuesto Global</span>
                        <span style={{ color: 'var(--accent-blue)' }}>{composite.toFixed(1)} / 100</span>
                      </div>
                      <div style={{ height: '6px', width: '100%', background: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ height: '100%', width: `${composite}%`, background: composite >= 60 ? 'var(--accent-green)' : 'var(--accent-blue)', transition: 'width 0.3s' }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="grid-2" style={{ gap: '12px', minWidth: '300px' }}>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Score JAX</div>
                      <div style={{ fontSize: '1rem', fontWeight: '700', color: 'var(--text-primary)' }}>{item.score.toFixed(6)}</div>
                      <div style={{ fontSize: '0.7rem', ...badge.style }}>{badge.text}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Gauss & Entropía</div>
                      <div style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--text-primary)' }}>G: {(item.score_gauss || 0).toFixed(2)} | E: {(item.score_entropy || 0).toFixed(2)}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Bayes & Hazard</div>
                      <div style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--text-primary)' }}>B: {(item.score_bayes || 0).toFixed(2)} | H: {(item.score_hazard || 0).toFixed(2)}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Markov (Global / Pos)</div>
                      <div style={{ fontSize: '0.85rem', fontWeight: '600', color: 'var(--text-primary)' }}>{formatProb(item.prob_m)} / {formatProb(item.prob_pos)}</div>
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

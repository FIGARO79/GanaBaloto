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
            <strong>💡 ¿Cómo interpretar las sugerencias y puntajes?</strong>
            <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px' }}>
              <li><strong>Score JAX (Frecuencia):</strong> Mide la popularidad histórica combinada de los números. Un score alto indica que las balotas han salido frecuentemente. Las combinaciones premium superan el percentil 75 histórico (<code>{scoreP75.toFixed(4)}</code>).</li>
              <li><strong>Markov Global:</strong> Mide la probabilidad de que esta secuencia completa ocurra según las transiciones del historial.</li>
              <li><strong>Markov Posicional:</strong> Mide la transición con respecto al <strong>último sorteo real jugado</strong>.</li>
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
          <p>Simulando millones de transiciones matemáticas con JAX...</p>
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
            return (
              <div key={index} className="card">
                <div className="sugerencia-card-container">
                  <div>
                    <span style={{ fontWeight: '700', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      SUGERENCIA #{index + 1} {item.score >= scoreP75 && '🌟 (ADN Premium)'} {item.score >= scoreMediana && item.score < scoreP75 && '👍 (Frecuencia Media)'}
                    </span>
                    <div className="balotas-container">
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
                  </div>

                  <div className="grid-2" style={{ gap: '16px', minWidth: '280px' }}>
                    <div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Score JAX</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-primary)' }}>{item.score.toFixed(6)}</div>
                      <div style={{ fontSize: '0.75rem', ...badge.style }}>{badge.text}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Markov Global</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-primary)' }}>{formatProb(item.prob_m)}</div>
                    </div>
                    <div style={{ gridColumn: 'span 2' }}>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Markov Posicional</div>
                      <div style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--text-primary)' }}>{formatProb(item.prob_pos)}</div>
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

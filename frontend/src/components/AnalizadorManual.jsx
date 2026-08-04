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

export default function AnalizadorManual({ sorteo, scoreMediana, scoreP75, posTopData }) {
  const [numeros, setNumeros] = useState(['', '', '', '', '']);
  const [sb, setSb] = useState('');
  const [analisis, setAnalisis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleNumChange = (index, value) => {
    const newNums = [...numeros];
    newNums[index] = value === '' ? '' : parseInt(value);
    setNumeros(newNums);
    setAnalisis(null);
  };

  const handleSbChange = (value) => {
    setSb(value === '' ? '' : parseInt(value));
    setAnalisis(null);
  };

  // Validaciones
  const hasEmptyFields = numeros.some(n => n === '') || sb === '';
  const numInts = numeros.map(n => parseInt(n)).filter(n => !isNaN(n));
  const hasDuplicates = numInts.length !== new Set(numInts).size;
  const outOfRangeMain = numInts.some(n => n < 1 || n > 43);
  const outOfRangeSb = sb !== '' && (parseInt(sb) < 1 || parseInt(sb) > 16);

  const analizarJugada = async (e) => {
    e.preventDefault();
    if (hasEmptyFields || hasDuplicates || outOfRangeMain || outOfRangeSb) return;

    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/analizar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sorteo: sorteo,
          numeros: numInts,
          sb: parseInt(sb)
        })
      });

      if (!response.ok) {
        throw new Error('Error al procesar el análisis de la jugada');
      }

      const data = await response.json();
      setAnalisis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreInterpretation = (score) => {
    if (score >= scoreP75) {
      return {
        text: 'Excelente (ADN Ganador Premium). Tus números tienen una frecuencia acumulada excepcionalmente alta en el histórico de ganadores.',
        color: 'var(--accent-green)'
      };
    } else if (score >= scoreMediana) {
      return {
        text: 'Frecuente. Tus números están en el rango promedio de las combinaciones que suelen salir premiadas.',
        color: 'var(--accent-blue)'
      };
    } else {
      return {
        text: 'Bajo el promedio. Juegas con combinaciones de balotas menos comunes o frías en el historial.',
        color: 'var(--text-muted)'
      };
    }
  };

  return (
    <div>
      {/* Formulario e informe de análisis manual */}
      <div className="card">
        <h3 className="card-title">Evalúa tu jugada favorita</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 20px 0' }}>
          Ingresa los números que tienes en mente para analizar si se alinean con los patrones matemáticos del historial de la lotería.
        </p>

        <form onSubmit={analizarJugada} className="analizador-form">
          <div className="inputs-row">
            {numeros.map((num, i) => (
              <div key={i} className="input-field">
                <label>B{i+1}</label>
                <input
                  type="number"
                  min="1"
                  max="43"
                  placeholder="-"
                  value={num}
                  onChange={(e) => handleNumChange(i, e.target.value)}
                  className="num-input"
                  required
                />
              </div>
            ))}
            <div className="input-field">
              <label style={{ color: 'var(--accent-yellow)' }}>Super Balota</label>
              <input
                type="number"
                min="1"
                max="16"
                placeholder="-"
                value={sb}
                onChange={(e) => handleSbChange(e.target.value)}
                className="num-input num-input-sb"
                required
              />
            </div>
          </div>

          {hasDuplicates && (
            <div className="alert alert-error" style={{ margin: '0' }}>
              <span>❌ Error: No puedes ingresar números repetidos en las balotas principales.</span>
            </div>
          )}

          {outOfRangeMain && (
            <div className="alert alert-error" style={{ margin: '0' }}>
              <span>❌ Error: Las balotas principales deben estar entre 1 y 43.</span>
            </div>
          )}

          {outOfRangeSb && (
            <div className="alert alert-error" style={{ margin: '0' }}>
              <span>❌ Error: La Super Balota debe estar entre 1 y 16.</span>
            </div>
          )}

          <button
            type="submit"
            className="btn btn-secondary"
            disabled={loading || hasEmptyFields || hasDuplicates || outOfRangeMain || outOfRangeSb}
            style={{ width: '100%', background: 'rgba(255,255,255,0.03)', borderColor: 'var(--border-color)' }}
          >
            {loading ? 'Analizando...' : '📊 Analizar Mi Jugada'}
          </button>
        </form>

        {error && (
          <div className="alert alert-error" style={{ marginTop: '20px' }}>
            <span>❌ Error: {error}</span>
          </div>
        )}
      </div>

      {analisis && !loading && (
        <div className="card" style={{ marginTop: '24px' }}>
          <h3 className="card-title">Diagnóstico de tu jugada:</h3>
          
          <div className="balotas-container">
            {analisis.combinacion.map((num, i) => (
              <div key={i} className="balota balota-principal">
                <div className="balota-inner">{num}</div>
              </div>
            ))}
            <div className="balota-separator">+</div>
            <div className="balota balota-super">
              <div className="balota-inner">{analisis.sb}</div>
            </div>
          </div>

          <div className="grid-3" style={{ marginTop: '24px', gap: '16px' }}>
            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.02)', gridColumn: 'span 3' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Índice Compuesto Global</div>
                  <div style={{ fontSize: '2rem', fontWeight: '800', margin: '4px 0', color: (analisis.composite || 50) >= 60 ? 'var(--accent-green)' : 'var(--accent-blue)' }}>{(analisis.composite || 50).toFixed(1)} / 100</div>
                </div>
                <div style={{ maxWidth: '400px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Evaluación ponderada en 6 dimensiones: Frecuencia JAX, Transiciones de Markov, Distribución Gaussiana, Entropía de Shannon, Posterior Bayesiano y Presión Hazard de Atraso.
                </div>
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.01)' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Score JAX (Frecuencia)</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', margin: '8px 0', color: 'var(--text-primary)' }}>{analisis.score.toFixed(6)}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--accent-blue)', display: 'flex', gap: '4px', alignItems: 'center' }}>
                <span>{analisis.score >= scoreMediana ? '▲' : '▼'}</span>
                <span>{(analisis.score - scoreMediana).toFixed(6)} vs Mediana</span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: '1.4' }}>
                <strong>Análisis:</strong> {getScoreInterpretation(analisis.score).text}
              </p>
            </div>

            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.01)' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Gauss & Entropía</div>
              <div style={{ fontSize: '1.2rem', fontWeight: '700', margin: '8px 0', color: 'var(--text-primary)' }}>
                Gauss: {(analisis.score_gauss || 0).toFixed(2)} | Entropía: {(analisis.score_entropy || 0).toFixed(2)}
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: '1.4' }}>
                Mide si la suma cae en la campana central (~110) y si los números mantienen suficiente aleatoriedad estructural.
              </p>
            </div>

            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.01)' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Bayes & Hazard Rate</div>
              <div style={{ fontSize: '1.2rem', fontWeight: '700', margin: '8px 0', color: 'var(--text-primary)' }}>
                Bayes: {(analisis.score_bayes || 0).toFixed(2)} | Hazard: {(analisis.score_hazard || 0).toFixed(2)}
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: '1.4' }}>
                Incorpora probabilidades posteriori Dirichlet y la madurez de atraso de las balotas según procesos de Poisson.
              </p>
            </div>

            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.01)' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Probabilidad Markov Global</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', margin: '8px 0', color: 'var(--text-primary)' }}>{formatProb(analisis.prob_m)}</div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: '1.4' }}>
                Evalúa si es natural que esta secuencia de 5 números aparezca junta en un sorteo.
              </p>
            </div>

            <div className="card" style={{ margin: 0, background: 'rgba(255, 255, 255, 0.01)', gridColumn: 'span 2' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Markov Posicional</div>
              <div style={{ fontSize: '1.4rem', fontWeight: '800', margin: '8px 0', color: 'var(--text-primary)' }}>{formatProb(analisis.prob_pos)}</div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '8px', lineHeight: '1.4' }}>
                {analisis.prob_pos > 1e-20 
                  ? 'Transición viable con respecto a la última combinación de la lotería real.' 
                  : 'Transición no registrada con respecto al sorteo anterior.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Predicciones Posicionales debajo de todo */}
      <div className="card" style={{ marginTop: '24px' }}>
        <h3 className="card-title">🔮 Predicciones de Markov Posicional (Próximo Sorteo)</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '12px' }}>
          Predicción de las transiciones de números más probables para cada balota (B1 a B5 y la Super Balota SB) de acuerdo con los números del último sorteo.
        </p>
        <div className="table-responsive">
          <table className="styled-table">
            <thead>
              <tr>
                <th>Posición</th>
                <th>Último Número</th>
                <th>Siguiente Probable</th>
                <th>Probabilidad de Transición</th>
              </tr>
            </thead>
            <tbody>
              {posTopData && posTopData.length > 0 ? (
                posTopData.map((row, i) => (
                  <tr key={i}>
                    <td><strong style={{ color: 'var(--text-primary)' }}>{row.Posicion}</strong></td>
                    <td>{row.Ultimo}</td>
                    <td style={{ color: 'var(--accent-blue)', fontWeight: 'bold' }}>{row.Siguiente}</td>
                    <td><code>{row.Probabilidad.toFixed(6)}</code></td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" style={{ textAlign: 'center', padding: '20px' }}>
                    No hay suficientes datos de transiciones para calcular predicciones.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

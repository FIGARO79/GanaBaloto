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

export default function AnalizadorManual({ sorteo, scoreMediana, scoreP75, scoreMeta = 0.1495 }) {
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

  return (
    <div>
      <div className="card">
        <h3 className="card-title">Auditoría Estocástica en 7 Dimensiones: {sorteo}</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 20px 0' }}>
          Ingresa 5 balotas principales y la Super Balota para auditar su calidad estructural mediante física estadística (Weibull, Ising, Gauss, Entropía y JAX).
        </p>

        <form onSubmit={analizarJugada} className="analizador-form">
          <div className="inputs-row" style={{ display: 'flex', gap: '10px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '20px' }}>
            {numeros.map((num, i) => (
              <div key={i} className="input-field" style={{ textAlign: 'center' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'bold' }}>B{i+1}</label>
                <input
                  type="number"
                  min="1"
                  max="43"
                  placeholder="-"
                  value={num}
                  onChange={(e) => handleNumChange(i, e.target.value)}
                  className="num-input"
                  style={{ width: '56px', height: '56px', fontSize: '1.2rem', textAlign: 'center', borderRadius: '12px', border: '1px solid var(--border-color)', background: 'rgba(255,255,255,0.03)', color: 'var(--text-primary)', fontWeight: 'bold' }}
                  required
                />
              </div>
            ))}
            <div className="input-field" style={{ textAlign: 'center' }}>
              <label style={{ fontSize: '0.8rem', color: 'var(--accent-yellow)', fontWeight: 'bold' }}>Super Balota</label>
              <input
                type="number"
                min="1"
                max="16"
                placeholder="-"
                value={sb}
                onChange={(e) => handleSbChange(e.target.value)}
                className="num-input num-input-sb"
                style={{ width: '56px', height: '56px', fontSize: '1.2rem', textAlign: 'center', borderRadius: '12px', border: '2px solid var(--accent-yellow)', background: 'rgba(234, 179, 8, 0.08)', color: 'var(--accent-yellow)', fontWeight: 'bold' }}
                required
              />
            </div>
          </div>

          {hasDuplicates && (
            <div className="alert alert-error" style={{ marginBottom: '16px' }}>
              <span>Error: No puedes ingresar números repetidos en las balotas principales.</span>
            </div>
          )}

          {outOfRangeMain && (
            <div className="alert alert-error" style={{ marginBottom: '16px' }}>
              <span>Error: Las balotas principales deben estar entre 1 y 43.</span>
            </div>
          )}

          {outOfRangeSb && (
            <div className="alert alert-error" style={{ marginBottom: '16px' }}>
              <span>Error: La Super Balota debe estar entre 1 y 16.</span>
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || hasEmptyFields || hasDuplicates || outOfRangeMain || outOfRangeSb}
            style={{ width: '100%', padding: '14px', fontSize: '1rem', fontWeight: 'bold' }}
          >
            {loading ? 'Calculando tensores en JAX...' : 'Auditar Combinación con Motor Cuantitativo'}
          </button>
        </form>

        {error && (
          <div className="alert alert-error" style={{ marginTop: '20px' }}>
            <span>Error: {error}</span>
          </div>
        )}
      </div>

      {analisis && !loading && (
        <div className="card" style={{ marginTop: '24px' }}>
          <h3 className="card-title">Resultado de la Auditoría Cuantitativa:</h3>
          
          <div className="balotas-container" style={{ margin: '16px 0' }}>
            {analisis.combinacion.map((num, i) => (
              <div key={i} className="balota balota-principal">
                <div className="balota-inner">{num < 10 ? `0${num}` : num}</div>
              </div>
            ))}
            <div className="balota-separator">+</div>
            <div className="balota balota-super">
              <div className="balota-inner">{analisis.sb < 10 ? `0${analisis.sb}` : analisis.sb}</div>
            </div>
          </div>

          {/* Veredicto Cualitativo Oficial */}
          {analisis.veredicto && (
            <div className="alert alert-info" style={{
              margin: '20px 0',
              background: (analisis.composite || 50) >= 70 ? 'rgba(34, 197, 94, 0.08)' : (analisis.composite || 50) >= 55 ? 'rgba(59, 130, 246, 0.08)' : 'rgba(239, 68, 68, 0.08)',
              borderColor: (analisis.composite || 50) >= 70 ? 'var(--accent-green)' : (analisis.composite || 50) >= 55 ? 'var(--accent-blue)' : 'var(--accent-red)'
            }}>
              <div style={{ fontWeight: '800', fontSize: '1.05rem', marginBottom: '10px' }}>
                {analisis.veredicto[0]}
              </div>
              <ul style={{ margin: '8px 0', paddingLeft: '20px', fontSize: '0.9rem', lineHeight: '1.7' }}>
                {analisis.veredicto.slice(2, -1).map((line, idx) => (
                  <li key={idx}>{line.replace(/^  • /, '')}</li>
                ))}
              </ul>
              <div style={{ marginTop: '12px', fontWeight: 'bold', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
                {analisis.veredicto[analisis.veredicto.length - 1]}
              </div>
            </div>
          )}

          {/* Resumen Central del Índice Compuesto */}
          <div style={{ background: 'var(--bg-card-subtle)', padding: '20px', borderRadius: '12px', border: '1px solid var(--border-color)', marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '15px' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Índice Compuesto Global</div>
                <div style={{ fontSize: '2.5rem', fontWeight: '800', margin: '4px 0', color: (analisis.composite || 50) >= 70 ? 'var(--accent-green)' : (analisis.composite || 50) >= 55 ? 'var(--accent-blue)' : 'var(--accent-yellow)' }}>
                  {(analisis.composite || 50).toFixed(1)} / 100
                </div>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Suma Total: <strong>{analisis.suma}</strong></span>
              </div>
              <div style={{ maxWidth: '420px', fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                Integra <strong>7 modelos estocásticos</strong> calibrados: Supervivencia de Weibull (Hazard), Acoplamiento de Ising, Campana Gaussiana, Entropía de Shannon, Frecuencia JAX, Inferencia Bayesiana y Cadenas de Markov.
              </div>
            </div>
          </div>

          {/* Grid de 6 Tarjetas Detalladas */}
          <div className="grid-3" style={{ gap: '14px' }}>
            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Score JAX vs Meta</div>
              <div style={{ fontSize: '1.3rem', fontWeight: '800', margin: '6px 0', color: analisis.score >= scoreMeta ? 'var(--accent-green)' : 'var(--text-primary)' }}>
                {analisis.score.toFixed(4)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Meta Histórica: {scoreMeta.toFixed(4)} {analisis.score >= scoreMeta ? '[ADN Ganador]' : '[Por debajo de meta]'}
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Weibull Hazard (Madurez)</div>
              <div style={{ fontSize: '1.3rem', fontWeight: '800', margin: '6px 0', color: (analisis.score_hazard || 0) >= 0.65 ? 'var(--accent-green)' : 'var(--text-primary)' }}>
                {(analisis.score_hazard || 0).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Curva de supervivencia ($k=1.1667$). Ventana dorada: 8 a 14 sorteos.
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Afinidad Ising ($J_{ij}$)</div>
              <div style={{ fontSize: '1.3rem', fontWeight: '800', margin: '6px 0', color: (analisis.score_ising || 0.5) >= 0.52 ? 'var(--accent-yellow)' : 'var(--text-primary)' }}>
                {(analisis.score_ising || 0.5).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Acoplamiento mutuo y atracción cooperativa entre pares de balotas.
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Gaussiana (Suma: {analisis.suma})</div>
              <div style={{ fontSize: '1.3rem', fontWeight: '800', margin: '6px 0', color: 'var(--text-primary)' }}>
                {(analisis.score_gauss || 0).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Proximidad a la zona dorada central ($\mu \approx 110, \sigma \approx 30$).
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Entropía de Shannon</div>
              <div style={{ fontSize: '1.3rem', fontWeight: '800', margin: '6px 0', color: 'var(--text-primary)' }}>
                {(analisis.score_entropy || 0).toFixed(2)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Dispersión espacial no uniforme para evitar aglomeraciones forzadas.
              </div>
            </div>

            <div className="card" style={{ margin: 0, background: 'var(--bg-card-subtle)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 'bold' }}>Bayes & Markov</div>
              <div style={{ fontSize: '1.1rem', fontWeight: '700', margin: '6px 0', color: 'var(--text-primary)' }}>
                B: {(analisis.score_bayes || 0).toFixed(2)} | M: {formatProb(analisis.prob_m)}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Suavizado Dirichlet y transición condicionada al último sorteo.
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

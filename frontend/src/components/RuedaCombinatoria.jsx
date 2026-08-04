import { useState } from 'react';

export default function RuedaCombinatoria() {
  const [selectedNums, setSelectedNums] = useState([]);
  const [selectedSbs, setSelectedSbs] = useState([7]);
  const [sorteoRueda, setSorteoRueda] = useState('Baloto');
  const [garantia, setGarantia] = useState(3);
  const [ruedas, setRuedas] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const toggleNum = (num) => {
    if (selectedNums.includes(num)) {
      setSelectedNums(selectedNums.filter((n) => n !== num));
    } else {
      if (selectedNums.length >= 12) {
        alert('Puedes seleccionar máximo 12 números principales para mantener la eficiencia del sistema.');
        return;
      }
      setSelectedNums([...selectedNums, num].sort((a, b) => a - b));
    }
    setRuedas(null);
  };

  const toggleSb = (sbNum) => {
    if (selectedSbs.includes(sbNum)) {
      if (selectedSbs.length === 1) return; // Mantener al menos 1 Super Balota
      setSelectedSbs(selectedSbs.filter((s) => s !== sbNum));
    } else {
      setSelectedSbs([...selectedSbs, sbNum].sort((a, b) => a - b));
    }
    setRuedas(null);
  };

  const generarRueda = async () => {
    if (selectedNums.length < 5) {
      setError('Debes seleccionar al menos 5 números principales.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/rueda', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          numeros: selectedNums,
          sbs: selectedSbs,
          sorteo: sorteoRueda,
          garantia: garantia
        })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Error al generar la rueda combinatoria');
      }
      const data = await response.json();
      setRuedas(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title">⚙️ Sistema de Ruedas Combinatorias (Wheeling System & BIBD)</h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 20px 0' }}>
        Selecciona tus números favoritos (entre 5 y 12 números entre 1 y 43) y <strong>una o varias Super Balotas (1 a 16)</strong>. El sistema expandirá las combinaciones optimizadas para garantizar matemáticamente 3 o 4 aciertos tanto para <strong>Baloto</strong> como para <strong>Revancha</strong>.
      </p>

      <div style={{ marginBottom: '20px' }}>
        <span style={{ fontWeight: '600' }}>1. Aplica para el sorteo:</span>
        <div style={{ display: 'flex', gap: '16px', marginTop: '8px' }}>
          {['Baloto', 'Revancha', 'Ambos (Baloto + Revancha)'].map((s) => {
            const val = s.startsWith('Ambos') ? 'Ambos' : s;
            return (
              <label key={val} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <input
                  type="radio"
                  name="sorteoRueda"
                  value={val}
                  checked={sorteoRueda === val}
                  onChange={() => setSorteoRueda(val)}
                />
                {s}
              </label>
            );
          })}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <span style={{ fontWeight: '600' }}>2. Selecciona números principales (1-43) ({selectedNums.length}/12):</span>
          {selectedNums.length > 0 && (
            <button 
              onClick={() => { setSelectedNums([]); setRuedas(null); }}
              className="btn btn-secondary"
              style={{ padding: '2px 10px', fontSize: '0.8rem' }}
            >
              Limpiar selección
            </button>
          )}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(42px, 1fr))', gap: '8px', margin: '12px 0' }}>
          {Array.from({ length: 43 }, (_, i) => i + 1).map((n) => {
            const isSelected = selectedNums.includes(n);
            return (
              <button
                key={n}
                onClick={() => toggleNum(n)}
                style={{
                  height: '42px',
                  borderRadius: '50%',
                  border: isSelected ? '2px solid var(--accent-blue)' : '1px solid var(--border-color)',
                  background: isSelected ? 'var(--accent-blue)' : 'rgba(255,255,255,0.03)',
                  color: isSelected ? '#fff' : 'var(--text-primary)',
                  fontWeight: '700',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {n}
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <span style={{ fontWeight: '600' }}>3. Selecciona una o varias Super Balotas ({selectedSbs.length} seleccionadas):</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(42px, 1fr))', gap: '8px', margin: '10px 0' }}>
          {Array.from({ length: 16 }, (_, i) => i + 1).map((n) => {
            const isSelected = selectedSbs.includes(n);
            return (
              <button
                key={n}
                onClick={() => toggleSb(n)}
                style={{
                  height: '42px',
                  borderRadius: '50%',
                  border: isSelected ? '2px solid var(--accent-yellow)' : '1px solid var(--border-color)',
                  background: isSelected ? 'var(--accent-yellow)' : 'rgba(255,255,255,0.03)',
                  color: isSelected ? '#1e293b' : 'var(--text-primary)',
                  fontWeight: '800',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {n}
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ marginBottom: '24px' }}>
        <span style={{ fontWeight: '600' }}>4. Nivel de Garantía de Aciertos:</span>
        <div style={{ display: 'flex', gap: '16px', marginTop: '10px' }}>
          <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <input 
              type="radio" 
              name="garantia" 
              value={3} 
              checked={garantia === 3}
              onChange={() => setGarantia(3)} 
            />
            Garantía Mínima: 3 Aciertos (Optimizado en costo)
          </label>
          <label style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <input 
              type="radio" 
              name="garantia" 
              value={4} 
              checked={garantia === 4}
              onChange={() => setGarantia(4)} 
            />
            Garantía Alta: 4 Aciertos (Mayor cobertura)
          </label>
        </div>
      </div>

      <button
        onClick={generarRueda}
        className="btn btn-primary"
        disabled={loading || selectedNums.length < 5}
        style={{ width: '100%' }}
      >
        {loading ? 'Calculando cobertura de rueda...' : '🔀 Generar Tiquetes Optimizados de Rueda'}
      </button>

      {error && (
        <div className="alert alert-error" style={{ marginTop: '20px' }}>
          <span>❌ {error}</span>
        </div>
      )}

      {ruedas && !loading && (
        <div style={{ marginTop: '28px' }}>
          <div className="alert alert-info">
            🎉 <strong>¡Rueda Combinatoria Generada para {ruedas.sorteo}!</strong>
            <p style={{ margin: '6px 0 0 0' }}>
              Para tus {ruedas.numeros_seleccionados.length} números elegidos [<code>{ruedas.numeros_seleccionados.join(', ')}</code>] y {ruedas.superbalotas.length} Super Balota(s) [<code>{ruedas.superbalotas.join(', ')}</code>], se generaron <strong>{ruedas.tiquetes_base} ruedas base</strong> expandidas a <strong>{ruedas.total_tiquetes} tiquetes de juego totales</strong> con garantía de {ruedas.garantia} aciertos.
            </p>
          </div>

          <h4 style={{ margin: '20px 0 12px 0' }}>Tiquetes de Juego Sugeridos ({ruedas.total_tiquetes} tiquetes):</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
            {(ruedas.tiquetes_finales || []).map((tiq, idx) => (
              <div key={idx} className="card" style={{ margin: 0, padding: '16px', background: 'rgba(255,255,255,0.02)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'bold' }}>TIQUETE #{idx + 1}</span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--accent-blue)', fontWeight: 'bold' }}>[{ruedas.sorteo}]</span>
                </div>
                <div className="balotas-container" style={{ margin: '0' }}>
                  {tiq.combinacion.map((num, i) => (
                    <div key={i} className="balota balota-principal" style={{ width: '36px', height: '36px' }}>
                      <div className="balota-inner" style={{ width: '20px', height: '20px', fontSize: '12px' }}>{num}</div>
                    </div>
                  ))}
                  <div className="balota-separator" style={{ fontSize: '16px' }}>+</div>
                  <div className="balota balota-super" style={{ width: '36px', height: '36px' }}>
                    <div className="balota-inner" style={{ width: '20px', height: '20px', fontSize: '12px' }}>{tiq.sb}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

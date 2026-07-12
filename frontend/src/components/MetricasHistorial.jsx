const formatProb = (val) => {
  if (val === undefined || val === null) return '0.000000';
  const num = Number(val);
  if (num === 0) return '0.000000';
  if (num < 1e-5) {
    return num.toExponential(3);
  }
  return num.toFixed(6);
};

export default function MetricasHistorial({ sorteo, data }) {
  if (!data) return <p>Cargando métricas...</p>;

  return (
    <div>
      <div className="card">
        <h3 className="card-title">Tendencias Históricas y Estadísticas de {sorteo}</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0 0 20px 0' }}>
          Análisis detallado de frecuencias acumuladas, números calientes y fríos obtenidos directamente de la base de datos de sorteos históricos.
        </p>
      </div>

      {/* Tabla ADN Ganadores */}
      <div className="card">
        <h3 className="card-title">🏆 ADN de Ganadores Históricos (5+1)</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '12px' }}>
          Listado de los sorteos históricos de {sorteo} donde se entregó el premio mayor (5 aciertos + Súper Balota).
        </p>
        <div className="table-responsive">
          <table className="styled-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Combinación</th>
                <th>SB</th>
                <th>Valor Premio</th>
                <th>Score JAX</th>
                <th>Prob. Markov</th>
              </tr>
            </thead>
            <tbody>
              {data.winners_adn && data.winners_adn.length > 0 ? (
                data.winners_adn.map((row, i) => (
                  <tr key={i}>
                    <td>{row.Fecha}</td>
                    <td><strong style={{ color: 'var(--text-primary)' }}>{row.Combinación}</strong></td>
                    <td>{row.SB}</td>
                    <td style={{ color: 'var(--accent-green)', fontWeight: '600' }}>${row['Valor Premio']}</td>
                    <td><code>{row['Score JAX'].toFixed(6)}</code></td>
                    <td><code>{formatProb(row['Prob. Markov'])}</code></td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>
                    No se encontraron ganadores históricos en el registro.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>


      {/* Grid de Hot/Cold y Chi2 */}
      <div className="grid-2">
        {/* Calientes */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title">🔥 Números Calientes</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px' }}>
            Los números con mayor frecuencia de aparición en los últimos 50 sorteos.
          </p>
          <div className="table-responsive">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Posición</th>
                  <th>Top 1</th>
                  <th>Top 2</th>
                  <th>Top 3</th>
                  <th>Top 4</th>
                  <th>Top 5</th>
                </tr>
              </thead>
              <tbody>
                {data.hot_numbers && data.hot_numbers.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{row.Balota}</strong></td>
                    <td style={{ color: 'var(--accent-red)', fontWeight: 'bold' }}>{row['Caliente 1']}</td>
                    <td>{row['Caliente 2']}</td>
                    <td>{row['Caliente 3']}</td>
                    <td>{row['Caliente 4']}</td>
                    <td>{row['Caliente 5']}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Fríos */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title">❄️ Números Fríos</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px' }}>
            Los números que llevan más tiempo sin salir (mayor racha de ausencia).
          </p>
          <div className="table-responsive">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Posición</th>
                  <th>Top 1</th>
                  <th>Top 2</th>
                  <th>Top 3</th>
                  <th>Top 4</th>
                  <th>Top 5</th>
                </tr>
              </thead>
              <tbody>
                {data.cold_numbers && data.cold_numbers.map((row, i) => (
                  <tr key={i}>
                    <td><strong>{row.Balota}</strong></td>
                    <td style={{ color: 'var(--accent-blue)', fontWeight: 'bold' }}>{row['Frío 1']}</td>
                    <td>{row['Frío 2']}</td>
                    <td>{row['Frío 3']}</td>
                    <td>{row['Frío 4']}</td>
                    <td>{row['Frío 5']}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Segunda Fila de Grid: Chi2, Paridad, Altos/Bajos */}
      <div className="grid-3" style={{ marginTop: '24px' }}>
        {/* Chi2 */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title">🎲 Prueba Chi-cuadrado</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px' }}>
            Determina si el comportamiento de la lotería es aleatorio (p-value &gt; 0.05).
          </p>
          <div className="table-responsive">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Métrica</th>
                  <th>Chi2</th>
                  <th>p-value</th>
                  <th>Diagnóstico</th>
                </tr>
              </thead>
              <tbody>
                {data.chi2 && data.chi2.map((row, i) => (
                  <tr key={i}>
                    <td>{row.Métrica}</td>
                    <td>{row['Chi2 Stat']}</td>
                    <td>{row['p-value']}</td>
                    <td style={{ 
                      color: row.Interpretación === 'Aleatorio' ? 'var(--accent-green)' : 'var(--accent-red)',
                      fontWeight: 'bold' 
                    }}>
                      {row.Interpretación}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Paridad */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title">⚖️ Frecuencia de Paridad</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px' }}>
            Proporción de números pares e impares en una combinación.
          </p>
          <div className="table-responsive">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Distribución</th>
                  <th>Frecuencia</th>
                </tr>
              </thead>
              <tbody>
                {data.parity && data.parity.slice(0, 5).map((row, i) => (
                  <tr key={i}>
                    <td>{row.Pares_Impares}</td>
                    <td style={{ color: 'var(--text-primary)', fontWeight: 'bold' }}>{row.Frecuencia}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Altos / Bajos */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title">📉 Altos vs Bajos</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', marginBottom: '12px' }}>
            Frecuencia de balotas bajas (1-21) vs altas (22-43).
          </p>
          <div className="table-responsive">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Distribución</th>
                  <th>Frecuencia</th>
                </tr>
              </thead>
              <tbody>
                {data.low_high && data.low_high.slice(0, 5).map((row, i) => (
                  <tr key={i}>
                    <td>{row.Bajos_Altos}</td>
                    <td style={{ color: 'var(--text-primary)', fontWeight: 'bold' }}>{row.Frecuencia}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

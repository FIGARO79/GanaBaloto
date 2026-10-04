export default function Metodologia() {
  return (
    <div>
      <div className="card">
        <h3 className="card-title">Arquitectura Cuantitativa y Física Estadística de GanaBaloto</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0' }}>
          El motor estocástico integra <strong>7 dimensiones matemáticas y modelos de física estadística</strong> compilados con aceleración por hardware en JAX.
        </p>
      </div>

      {/* Grid de Modelos 1 a 4 */}
      <div className="grid-2" style={{ gap: '16px', marginTop: '16px' }}>
        <div className="card">
          <h4 className="card-title" style={{ color: 'var(--accent-blue)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            1. Aceleración Vectorial con JAX (GPU)
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            JAX permite evaluar millones de combinaciones candidatas en milisegundos mediante compilación <code>@jax.jit</code> sobre GPU NVIDIA o CPU vectorizada con XLA.
          </p>
          <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px' }}>
            <li><strong>Score JAX:</strong> Evalúa la presencia histórica acumulada de las balotas en sorteos premiados.</li>
            <li><strong>Meta Histórica (ADN):</strong> Compara el score frente al promedio real de boletos que han obtenido el premio mayor (5+1).</li>
          </ul>
        </div>

        <div className="card">
          <h4 className="card-title" style={{ color: 'var(--accent-green)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            2. Supervivencia de Weibull (Hazard Rate)
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            Sustituye la hipótesis clásica sin memoria (Poisson) por una curva de riesgo de Weibull calibrada empíricamente (<code style={{ color: '#22c55e' }}>k = 1.1667</code>, <code style={{ color: '#22c55e' }}>λ = 9.0176</code>).
          </p>
          <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px' }}>
            <li><strong>Ventana Dorada de Madurez:</strong> La probabilidad de retorno estocástico alcanza su cresta entre los <strong>8 y 14 sorteos de atraso</strong>.</li>
            <li>Penaliza tanto balotas hiper-recientes (enfriamiento) como balotas hiper-atrasadas (estados de absorción).</li>
          </ul>
        </div>

        <div className="card">
          <h4 className="card-title" style={{ color: 'var(--accent-yellow)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            3. Modelo de Ising para Co-ocurrencias (J_ij)
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            Inspirado en la mecánica estadística y los vidrios de espín (Spin Glasses), mide la energía de acoplamiento mutuo pareado:
          </p>
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '8px 12px', borderRadius: '6px', fontSize: '0.85rem', fontFamily: 'monospace', margin: '8px 0' }}>
            J_ij = ln((C_ij + 1) / (E[C_ij] + 1))
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
            Detecta pares de balotas con atracción cooperativa cuya frecuencia real supera significativamente el azar estadístico (hasta 1.94x la expectativa teórica).
          </p>
        </div>

        <div className="card">
          <h4 className="card-title" style={{ color: '#a855f7', display: 'flex', alignItems: 'center', gap: '8px' }}>
            4. Régimen Dinámico con HMM
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            Un Modelo Oculto de Markov (HMM) de 3 estados monitorea la inercia de la suma y densidad posicional de los últimos 10 sorteos:
          </p>
          <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px' }}>
            <li><strong>Congestión Baja:</strong> Sumas &lt; 95 (régimen habitual en los sorteos con botes millonarios).</li>
            <li><strong>Equilibrio Central:</strong> Sumas entre 95 y 125 con dispersión armónica.</li>
            <li><strong>Expansión Alta:</strong> Sumas &gt; 125 con predominio en decenas 3 y 4.</li>
          </ul>
        </div>
      </div>

      {/* Grid de Modelos 5 a 8 */}
      <div className="grid-2" style={{ gap: '16px', marginTop: '16px' }}>
        <div className="card">
          <h4 className="card-title" style={{ color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px' }}>
            5. Campana Gaussiana & Entropía de Shannon
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            <strong>Gauss (Suma de Balotas):</strong> Evalúa la proximidad al centro de masa histórico (μ ≈ 110, σ ≈ 30), premiando la zona dorada de 90 a 130.<br /><br />
            <strong>Entropía de Shannon:</strong> Mide la dispersión espacial de los intervalos para descartar secuencias artificiales, concentraciones en una sola decena o escaleras correlativas forzadas.
          </p>
        </div>

        <div className="card">
          <h4 className="card-title" style={{ color: '#f97316', display: 'flex', alignItems: 'center', gap: '8px' }}>
            6. Ruedas Combinatorias (Wheeling Systems)
          </h4>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
            Algoritmo de cobertura basado en <strong>Greedy Set-Cover</strong>:
          </p>
          <ul style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '18px' }}>
            <li>Permite seleccionar N números clave (ej. 7 a 15) y genera el número mínimo de tiquetes que garantiza matemáticamente <strong>t aciertos asegurados</strong>.</li>
            <li>Optimiza de manera determinista el presupuesto de juego al cubrir el 100% de los subconjuntos objetivo.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

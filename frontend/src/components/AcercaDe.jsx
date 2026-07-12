export default function AcercaDe() {
  return (
    <div className="card">
      <h3 className="card-title">🧭 Acerca de GanaBaloto Web</h3>
      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '16px' }}>
        GanaBaloto Web nace como una guía práctica para explorar resultados históricos de Baloto y Revancha con un enfoque más analítico y transparentemente estadístico.
      </p>

      <div className="content-intro-grid" style={{ marginBottom: '16px' }}>
        <div className="info-card">
          <h3>¿Qué ofrece?</h3>
          <p>Ofrece análisis de resultados históricos, métricas de frecuencia, comparativas y sugerencias basadas en patrones observables.</p>
        </div>
        <div className="info-card">
          <h3>¿Para quién?</h3>
          <p>Está dirigida a personas interesadas en entender mejor la dinámica de los sorteos y a quienes quieren ver datos con contexto.</p>
        </div>
        <div className="info-card">
          <h3>¿Qué debemos tener en cuenta?</h3>
          <p>Los resultados de lotería siguen siendo aleatorios. Esta web no garantiza premios, pero sí ofrece una mirada más informada.</p>
        </div>
      </div>

      <div className="card" style={{ background: 'rgba(37, 99, 235, 0.04)', borderColor: 'rgba(37, 99, 235, 0.16)' }}>
        <h4 className="card-title" style={{ marginBottom: '8px' }}>¿Qué son las cadenas de Markov?</h4>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '10px' }}>
          Las cadenas de Markov son modelos probabilísticos que describen cómo cambia un sistema de estado en estado. En este proyecto se utilizan para estudiar la relación entre resultados consecutivos y estimar patrones de transición entre números.
        </p>
        <h4 className="card-title" style={{ marginBottom: '8px' }}>Nuestros principios</h4>
        <ul className="info-list">
          <li>Explicar el análisis con claridad y sin promesas engañosas.</li>
          <li>Mostrar los datos de forma útil y comprensible para cualquier usuario.</li>
          <li>Separar el análisis estadístico del simple azar y las expectativas irreales.</li>
          <li>Mejorar la experiencia del usuario con contenido original y bien estructurado.</li>
        </ul>
      </div>
    </div>
  );
}

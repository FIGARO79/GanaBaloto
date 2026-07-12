export default function Metodologia() {
  return (
    <div>
      <div className="card">
        <h3 className="card-title">📚 Guía Teórica y Metodológica de GanaBaloto</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0' }}>
          Esta aplicación utiliza modelos estocásticos, cadenas de Markov y análisis de frecuencias acelerado mediante JAX para analizar y optimizar jugadas de lotería.
        </p>
      </div>

      <div className="card" style={{ background: 'rgba(16, 185, 129, 0.04)', borderColor: 'rgba(16, 185, 129, 0.18)' }}>
        <h4 className="card-title" style={{ marginBottom: '10px' }}>🧠 Qué puedes aprender aquí</h4>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>
          Esta web no pretende ofrecer certezas sobre la lotería, sino mostrar un marco más claro para interpretar los datos históricos, comparar combinaciones y entender cómo se construye el análisis estadístico.
        </p>
      </div>

      <div className="card" style={{ background: 'rgba(37, 99, 235, 0.04)', borderColor: 'rgba(37, 99, 235, 0.16)' }}>
        <h4 className="card-title" style={{ marginBottom: '10px' }}>🔗 ¿Qué son las cadenas de Markov?</h4>
        <p style={{ color: 'var(--text-secondary)', lineHeight: 1.7, margin: 0 }}>
          Una cadena de Markov es un modelo matemático que permite estudiar cómo cambia un sistema paso a paso, donde el siguiente estado depende solo del estado actual, no de todo el pasado. En este contexto, se usa para analizar la probabilidad de que ciertos números aparezcan en relación con los resultados anteriores.
        </p>
      </div>

      <div className="grid-2">
      </div>

      <div className="grid-2">
        <div>
          <div className="card" style={{ height: '100%' }}>
            <h4 className="card-title" style={{ color: 'var(--accent-blue)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>⚡</span> Computación Acelerada con JAX
            </h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              Para calcular el <strong>Score JAX</strong>, el sistema mapea la frecuencia con la que cada número ha aparecido en el histórico total de sorteos.
            </p>
            <ul style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '20px' }}>
              <li>
                <strong>¿Por qué JAX?</strong> JAX nos permite paralelizar las búsquedas de frecuencias sobre millones de registros y combinaciones posibles en microsegundos, ejecutando operaciones matemáticas de álgebra lineal directamente en la GPU (si está disponible) o mediante CPU optimizada vectorialmente a través de XLA.
              </li>
              <li>
                <strong>El Score:</strong> Es el promedio de las frecuencias relativas de aparición de las 5 balotas principales y la súper balota elegida.
              </li>
            </ul>
          </div>
        </div>

        <div>
          <div className="card" style={{ height: '100%' }}>
            <h4 className="card-title" style={{ color: 'var(--accent-green)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>⚖]</span> Filtros Estadísticos del ADN Ganador
            </h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              Para reducir el espacio de búsqueda de millones de combinaciones posibles a solo aquellas viables, la aplicación aplica tres filtros del "ADN histórico":
            </p>
            <ol style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6', paddingLeft: '20px' }}>
              <li>
                <strong>Frecuencia de Suma:</strong> Las sumas de las combinaciones sugeridas deben caer dentro del intervalo del 80% más frecuente en los sorteos históricos.
              </li>
              <li>
                <strong>Distribución Par/Impar:</strong> Se evitan combinaciones de puros pares o impares, sugiriendo distribuciones más probables (ej. 3 pares y 2 impares).
              </li>
              <li>
                <strong>Bajos vs Altos:</strong> Se distribuyen las balotas de forma balanceada entre los números bajos (1-21) y altos (22-43).
              </li>
            </ol>
          </div>
        </div>

        <div style={{ gridColumn: 'span 2' }}>
          <div className="card">
            <h4 className="card-title" style={{ color: 'var(--accent-yellow)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>⛓️</span> Cadenas de Markov
            </h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
              Una <strong>Cadena de Markov</strong> es un modelo estocástico donde la probabilidad de que ocurra un evento depende únicamente del estado inmediatamente anterior.
            </p>
            
            <div className="grid-2" style={{ marginTop: '16px', gap: '16px' }}>
              <div style={{ background: 'rgba(255, 255, 255, 0.01)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <h5 style={{ margin: '0 0 8px 0', fontSize: '0.95rem', color: 'var(--text-primary)' }}>🌍 1. Markov Global</h5>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.5' }}>
                  Analiza la secuencia de balotas consecutivas dentro de un mismo sorteo. Permite construir una <strong>Matriz de Transición</strong> general que mide qué tan probable es que el número X ocurra al lado del número Y.
                </p>
              </div>

              <div style={{ background: 'rgba(255, 255, 255, 0.01)', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <h5 style={{ margin: '0 0 8px 0', fontSize: '0.95rem', color: 'var(--text-primary)' }}>📍 2. Markov Posicional</h5>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 0, lineHeight: '1.5' }}>
                  Analiza cómo evoluciona cada balota individualmente de un sorteo al siguiente. Si en el sorteo anterior la balota en la Posición 1 fue el número A, la matriz calcula la probabilidad de que en el sorteo actual sea el número B.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

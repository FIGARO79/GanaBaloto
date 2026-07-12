import { useState } from 'react';

const ARTICLES = [
  {
    id: 'matematica-baloto',
    title: 'La Ciencia Detrás de Baloto: Probabilidades, Combinatoria y Frecuencias',
    date: '10 de Julio, 2026',
    author: 'Equipo Científico GanaBaloto',
    readTime: '5 min de lectura',
    category: 'Matemáticas y Probabilidad',
    excerpt: '¿Cómo funciona realmente el azar en sorteos de tipo 5+1? Analizamos matemáticamente las combinaciones posibles y por qué la distribución de frecuencias es clave.',
    content: (
      <>
        <p>
          El sorteo oficial de Baloto en Colombia opera bajo una fórmula clásica de combinatoria sin repetición, denominada técnicamente como un sorteo <strong>5/43 + 1/16</strong>. Esto significa que para obtener el premio mayor (conocido comercialmente como el acumulado), un jugador debe acertar exactamente 5 números principales elegidos del 1 al 43, además de una balota especial llamada "Súper Balota", seleccionada del 1 al 16.
        </p>

        <h4>El cálculo de las combinaciones posibles</h4>
        <p>
          Para calcular cuántas combinaciones distintas existen, recurrimos al coeficiente binomial. Primero, calculamos cuántos grupos de 5 números se pueden formar a partir de un conjunto de 43:
        </p>
        <div className="formula-box" style={{ background: 'var(--bg-primary)', padding: '15px', borderRadius: '8px', margin: '15px 0', fontFamily: 'monospace', textAlign: 'center' }}>
          C(43, 5) = 43! / [5! * (43 - 5)!] = 962,598 combinaciones
        </div>
        <p>
          Una vez obtenido este valor, debemos multiplicarlo por las posibilidades de la Súper Balota, las cuales son 16. El resultado es el espacio muestral total de jugadas posibles:
        </p>
        <div className="formula-box" style={{ background: 'var(--bg-primary)', padding: '15px', borderRadius: '8px', margin: '15px 0', fontFamily: 'monospace', textAlign: 'center', fontWeight: 'bold', color: 'var(--accent-blue)' }}>
          Total = 962,598 * 16 = 15,401,568 combinaciones únicas
        </div>
        <p>
          Esto significa que la probabilidad teórica pura de acertar el premio mayor con una sola apuesta es exactamente de <strong>1 entre 15,401,568</strong> (es decir, aproximadamente 0.00000649%).
        </p>

        <h4>Frecuencias e Historial: ¿Ayudan a elegir mejor?</h4>
        <p>
          En la teoría matemática pura de probabilidad clásica, cada sorteo es un evento independiente. La probabilidad de que salga cualquier número en el próximo sorteo es exactamente igual. No obstante, al estudiar series de tiempo históricas amplias, los analistas de datos observan la denominada <strong>Ley de los Grandes Números</strong>. A medida que el número de sorteos aumenta, las frecuencias de aparición de todas las balotas tienden a estabilizarse en torno a un promedio uniforme teórico.
        </p>
        <p>
          Sin embargo, en períodos finitos (como los últimos años de sorteos), se producen desviaciones estadísticas interesantes debido a fluctuaciones del azar. Es aquí donde surgen los conceptos de "números calientes" (aquellos con frecuencia temporalmente por encima de la media) y "números fríos" o "maduros" (números con brechas de inactividad altas). Identificar estas anomalías nos permite conformar apuestas que respeten las tendencias reales de distribución (como las proporciones de pares/impares y sumas agregadas), emulando las características físicas que suelen presentar las combinaciones ganadoras históricas.
        </p>
      </>
    )
  },
  {
    id: 'markov-loterias',
    title: 'Cadenas de Markov en Loterías: Mitos y Realidades Estadísticas',
    date: '8 de Julio, 2026',
    author: 'Dr. Estadística Aplicada',
    readTime: '6 min de lectura',
    category: 'Algoritmos y Modelos',
    excerpt: '¿Pueden las matrices de transición predecir números ganadores? Separamos la especulación de la matemática formal al estudiar dependencias temporales en sorteos.',
    content: (
      <>
        <p>
          Las <strong>Cadenas de Markov</strong>, llamadas así en honor al matemático ruso Andréi Márkov, son procesos estocásticos en los que la probabilidad de transición a un estado futuro depende únicamente del estado inmediatamente anterior (propiedad de Markov de primer orden). En términos cotidianos: "el futuro depende de dónde estás ahora, no de cómo llegaste ahí".
        </p>

        <h4>¿Por qué aplicar Markov a un sorteo de Baloto?</h4>
        <p>
          Un detractor del análisis técnico podría argumentar que, dado que el sorteo es mecánico (balotas en una urna de aire), los resultados son completamente independientes y no tienen memoria. Esto es cierto desde la física teórica ideal. Sin embargo, en el análisis de datos de series históricas, modelar los sorteos como una Cadena de Markov nos permite responder preguntas analíticas valiosas:
        </p>
        <ul>
          <li>¿Existe alguna correlación temporal o física menor en las máquinas de sorteo que favorezca que un número aparezca inmediatamente después de otro?</li>
          <li>¿Cómo cambian las probabilidades de transición de las balotas según su posición ordenada de aparición (Markov Posicional)?</li>
          <li>¿Qué números tienden a aparecer juntos en secuencias consecutivas (Markov Global)?</li>
        </ul>

        <h4>La realidad de la matriz de transición</h4>
        <p>
          Mediante el cálculo de matrices de transición en el histórico de Baloto y Revancha, podemos estimar empíricamente la probabilidad condicional:
        </p>
        <div className="formula-box" style={{ background: 'var(--bg-primary)', padding: '15px', borderRadius: '8px', margin: '15px 0', fontFamily: 'monospace', textAlign: 'center' }}>
          P(X_t = j | X_(t-1) = i)
        </div>
        <p>
          Esto mide la probabilidad de que la balota <em>j</em> aparezca en el sorteo actual si en el sorteo anterior salió la balota <em>i</em>.
        </p>
        <p>
          Es fundamental aclarar que **estos modelos no son predictivos en el sentido de adivinar el futuro con certeza**. El azar sigue gobernando el sistema. Sin embargo, las cadenas de Markov actúan como un potente filtro descriptivo. Si una jugada seleccionada al azar tiene un coeficiente de transición histórico extremadamente bajo dentro de la matriz de Markov, significa que esa combinación en particular va en contra de la dinámica de cambio observada en la práctica histórica. Ajustar nuestras jugadas hacia caminos de transición más transitados es una técnica racional para evitar combinaciones sumamente improbables.
        </p>
      </>
    )
  },
  {
    id: 'juego-responsable',
    title: 'Juego Responsable: Estrategias de Autocontrol y Matemáticas de Lotería',
    date: '5 de Julio, 2026',
    author: 'Lic. Bienestar Colectivo',
    readTime: '4 min de lectura',
    category: 'Juego Responsable',
    excerpt: 'Consejos prácticos para ver la lotería como entretenimiento, limitar tu presupuesto y comprender que la estadística es una herramienta formativa, no mágica.',
    content: (
      <>
        <p>
          La participación en sorteos y juegos de azar como Baloto y Revancha debe ser concebida única y exclusivamente como una actividad de entretenimiento y recreación personal. Debido a que las probabilidades de ganar el premio acumulado principal son extremadamente reducidas (1 entre 15.4 millones), es esencial mantener una perspectiva madura, racional y responsable.
        </p>

        <h4>Pilares fundamentales del Juego Responsable</h4>
        <ol>
          <li>
            <strong>Presupuesto Cerrado:</strong> Asigna una cantidad fija de dinero mensual o semanal para jugar, la cual consideres parte de tu presupuesto de entretenimiento (como ir al cine o cenar fuera). Bajo ninguna circunstancia uses dinero destinado a gastos básicos, alimentación, educación o ahorro familiar.
          </li>
          <li>
            <strong>Sin Búsqueda de Pérdidas:</strong> Si juegas una combinación y no resulta ganadora, nunca intentes realizar más apuestas de inmediato con la esperanza de "recuperar" el dinero invertido. Acepta el coste como parte del entretenimiento.
          </li>
          <li>
            <strong>Comprensión del Azar:</strong> Ningún software, algoritmo predictivo, cadena de Markov o inteligencia artificial puede garantizar un boleto ganador. Las herramientas estadísticas sirven para estructurar datos históricos y aprender sobre probabilidad, pero el resultado final siempre dependerá de una mezcla inalterable de azar puro.
          </li>
          <li>
            <strong>Control del Tiempo:</strong> No permitas que el análisis de números o el juego interfieran con tu vida social, familiar o laboral. Define momentos específicos para revisar tus estadísticas y combinaciones sin obsesionarte.
          </li>
        </ol>

        <h4>Dónde buscar apoyo en Colombia</h4>
        <p>
          En Colombia, el organismo estatal que regula los juegos de suerte y azar es <strong>Coljuegos</strong>. Ellos promueven la campaña "Juega Bien", orientada a la concientización sobre la ludopatía y el juego compulsivo. Si sientes que tú o un familiar está perdiendo el control de sus apuestas, puedes buscar ayuda gratuita a través de canales de apoyo psicológico especializados en adicciones conductuales o contactar directamente a los programas de prevención locales de Coljuegos.
        </p>
      </>
    )
  }
];

export default function Blog() {
  const [selectedArticle, setSelectedArticle] = useState(null);

  return (
    <div className="blog-section">
      <div className="card">
        <h3 className="card-title">📚 Artículos Educativos y Análisis del Azar</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0' }}>
          Explora guías detalladas escritas por expertos en probabilidad, algoritmos aplicados e instrucciones de juego responsable. Nuestro objetivo es educar y aportar valor real a la comunidad.
        </p>
      </div>

      {selectedArticle ? (
        <div className="card article-detail" style={{ animation: 'fadeIn 0.3s ease' }}>
          <button 
            className="btn btn-secondary" 
            onClick={() => setSelectedArticle(null)} 
            style={{ marginBottom: '20px' }}
          >
            ← Volver a la lista de artículos
          </button>
          
          <span className="section-badge" style={{ display: 'inline-block', marginBottom: '8px' }}>
            {selectedArticle.category}
          </span>
          <h2 className="card-title" style={{ fontSize: '1.8rem', lineHeight: '1.3', marginBottom: '10px' }}>
            {selectedArticle.title}
          </h2>
          
          <div style={{ display: 'flex', gap: '15px', color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '20px', flexWrap: 'wrap' }}>
            <span><strong>Autor:</strong> {selectedArticle.author}</span>
            <span>•</span>
            <span><strong>Fecha:</strong> {selectedArticle.date}</span>
            <span>•</span>
            <span><strong>Lectura:</strong> {selectedArticle.readTime}</span>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '0 0 20px 0' }} />

          <div className="article-body-content" style={{ color: 'var(--text-secondary)', lineHeight: '1.8', fontSize: '1rem' }}>
            {selectedArticle.content}
          </div>
          
          <div style={{ marginTop: '30px', padding: '15px', background: 'rgba(37, 99, 235, 0.03)', borderRadius: '8px', borderLeft: '4px solid var(--accent-blue)' }}>
            <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              <strong>Nota del editor:</strong> Las matemáticas de la combinatoria y las Cadenas de Markov son modelos teóricos que ayudan a entender la frecuencia de sorteos anteriores, pero no cambian las leyes del azar inherentes a la lotería. Juega de forma consciente.
            </p>
          </div>
        </div>
      ) : (
        <div className="articles-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
          {ARTICLES.map((article) => (
            <div key={article.id} className="card article-card" style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between', transition: 'transform 0.2s', cursor: 'pointer' }} onClick={() => setSelectedArticle(article)}>
              <div>
                <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--accent-blue)', fontWeight: 'bold' }}>
                  {article.category}
                </span>
                <h4 style={{ margin: '8px 0', fontSize: '1.2rem', color: 'var(--text-primary)', fontWeight: '700' }}>
                  {article.title}
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', textOverflow: 'ellipsis', marginBottom: '15px' }}>
                  {article.excerpt}
                </p>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                <span>{article.date}</span>
                <span style={{ color: 'var(--accent-blue)', fontWeight: '600' }}>Leer más →</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

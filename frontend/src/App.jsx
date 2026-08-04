import { useState, useEffect } from 'react';
import Sugerencias from './components/Sugerencias.jsx';
import AnalizadorManual from './components/AnalizadorManual.jsx';
import RuedaCombinatoria from './components/RuedaCombinatoria.jsx';
import MetricasHistorial from './components/MetricasHistorial.jsx';
import Metodologia from './components/Metodologia.jsx';
import AcercaDe from './components/AcercaDe.jsx';
import Blog from './components/Blog.jsx';
import Politicas from './components/Politicas.jsx';
import AdBanner from './components/AdBanner.jsx';
import './App.css';

const formatProb = (val) => {
  if (val === undefined || val === null) return '0.000000';
  const num = Number(val);
  if (num === 0) return '0.000000';
  if (num < 1e-5) {
    return num.toExponential(3);
  }
  return num.toFixed(6);
};

function App() {
  const [sorteo, setSorteo] = useState('Baloto');
  const [activeTab, setActiveTab] = useState('sugerencias');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reloadingDb, setReloadingDb] = useState(false);
  const [politicasSubTab, setPoliticasSubTab] = useState('privacidad');

  const fetchSorteoData = async (tipo) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/sorteo/${tipo}`);
      if (!response.ok) {
        throw new Error(`Error al obtener los datos de ${tipo}`);
      }
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchSorteoData(sorteo);
    }, 0);
    return () => clearTimeout(timer);
  }, [sorteo]);

  const recargarBaseDatos = async () => {
    setReloadingDb(true);
    try {
      const response = await fetch('/api/recargar', {
        method: 'POST'
      });
      if (!response.ok) {
        throw new Error('Error al recargar la base de datos');
      }
      alert('¡Base de datos recargada con éxito!');
      fetchSorteoData(sorteo);
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setReloadingDb(false);
    }
  };

  return (
    <div className="dashboard-container">
      {/* Barra Lateral (Sidebar) */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-logo">8</div>
          <span className="sidebar-brand-name">GanaBaloto Web</span>
        </div>
        
        <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '0' }} />

        <div className="sidebar-section">
          <span className="sidebar-label">Selecciona el Sorteo</span>
          <div className="radio-group">
            <div 
              className={`radio-option ${sorteo === 'Baloto' ? 'active' : ''}`}
              onClick={() => setSorteo('Baloto')}
            >
              <div className="radio-dot"></div>
              <span className="radio-label">Baloto</span>
            </div>
            <div 
              className={`radio-option ${sorteo === 'Revancha' ? 'active' : ''}`}
              onClick={() => setSorteo('Revancha')}
            >
              <div className="radio-dot"></div>
              <span className="radio-label">Revancha</span>
            </div>
          </div>
        </div>

        <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '0' }} />

        <div className="sidebar-section">
          <div className="engine-box">
            <span className="engine-title">Motor de Cálculo</span>
            <span className="engine-value">⚡ JAX (CPU/GPU)</span>
          </div>
        </div>

        <div className="sidebar-section" style={{ marginTop: 'auto' }}>
          <button 
            className="btn btn-secondary" 
            onClick={recargarBaseDatos}
            disabled={reloadingDb}
            style={{ width: '100%', fontSize: '0.85rem' }}
          >
            {reloadingDb ? 'Recargando...' : '🔄 Recargar Base de Datos'}
          </button>

          {/* Bloque de Anuncio Vertical en Barra Lateral */}
          <AdBanner slot="1234567890" format="vertical" />
        </div>
      </aside>

      {/* Contenido Principal */}
      <main className="main-content">
        <header className="main-header">
          <div className="main-title-container">
            <div className="main-logo">8</div>
            <div>
              <h1 className="main-title">GanaBaloto Web</h1>
              <p className="main-subtitle">Análisis estocástico y probabilístico de lotería mediante Cadenas de Markov.</p>
            </div>
          </div>
        </header>

        <section className="card content-intro">
          <h2 className="card-title">Una herramienta para interpretar patrones de Baloto con criterio</h2>
          <p className="content-intro-text">
            GanaBaloto Web combina resultados históricos, métricas probabilísticas y una metodología clara para ayudarte a entender mejor cómo se comportan los sorteos y a tomar decisiones con más contexto.
          </p>
          <div className="content-intro-grid">
            <div className="info-card">
              <h3>¿Qué incluye?</h3>
              <p>Sugerencias inteligentes, métricas de historial y un analizador manual para comparar combinaciones con más detalle.</p>
            </div>
            <div className="info-card">
              <h3>¿Cómo leer los resultados?</h3>
              <p>El panel muestra puntuaciones, probabilidades y comparativas históricas para que el análisis sea más comprensible.</p>
            </div>
            <div className="info-card">
              <h3>¿Por qué esta web existe?</h3>
              <p>Porque la lotería no es solo azar: comprender patrones y distribuciones ayuda a analizar mejor cada sorteo.</p>
            </div>
          </div>
        </section>

        <section className="card">
          <h3 className="card-title">❓ Preguntas frecuentes</h3>
          <div className="faq-list">
            <details>
              <summary>¿Qué significa el score JAX?</summary>
              <p>Es una métrica que compara la frecuencia histórica de una combinación con el comportamiento general del sorteo.</p>
            </details>
            <details>
              <summary>¿Sirve para predecir resultados?</summary>
              <p>No garantiza aciertos, pero sí ofrece un marco más informado para comparar combinaciones de forma estadística.</p>
            </details>
            <details>
              <summary>¿Por qué hay una metodología tan detallada?</summary>
              <p>Porque el objetivo es que la web sea útil y transparente, no solo visual. La metodología ayuda a entender el origen de cada señal.</p>
            </details>
          </div>
        </section>

        <section className="content-support-grid">
          <div className="card">
            <h3 className="card-title">📘 Cómo usar esta web</h3>
            <p className="content-intro-text" style={{ marginBottom: '12px' }}>
              La idea de esta plataforma es mostrar un análisis más amplio del comportamiento histórico de Baloto y Revancha, ayudando a interpretar las series de resultados con mayor contexto.
            </p>
            <ul className="info-list">
              <li>Comienza por elegir el sorteo en la barra lateral.</li>
              <li>Revisa las sugerencias inteligentes para ver combinaciones con mejor perfil histórico.</li>
              <li>Consulta la pestaña de métricas si quieres entender cómo se distribuyen las frecuencias.</li>
              <li>Usa la metodología para conocer el fundamento detrás del análisis.</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="card-title">🧭 Acerca de la propuesta</h3>
            <p className="content-intro-text" style={{ marginBottom: '12px' }}>
              Esta web busca presentar el análisis de forma práctica, clara y educativa, con explicaciones que ayudan a comprender el contexto de cada recomendación.</p>
            <ul className="info-list">
              <li>Explica los conceptos básicos de forma sencilla.</li>
              <li>Relaciona los datos con el comportamiento histórico real.</li>
              <li>Ofrece una lectura menos superficial y más informada.</li>
            </ul>
          </div>
        </section>

        {/* Navegación de Pestañas */}
        <nav className="tabs-navigation">
          <button 
            className={`tab-btn ${activeTab === 'sugerencias' ? 'active' : ''}`}
            onClick={() => setActiveTab('sugerencias')}
          >
            🔮 Sugerencias Inteligentes
          </button>
          <button 
            className={`tab-btn ${activeTab === 'analizador' ? 'active' : ''}`}
            onClick={() => setActiveTab('analizador')}
          >
            📝 Analizador Manual
          </button>
          <button 
            className={`tab-btn ${activeTab === 'rueda' ? 'active' : ''}`}
            onClick={() => setActiveTab('rueda')}
          >
            🔀 Ruedas de Juego
          </button>
          <button 
            className={`tab-btn ${activeTab === 'metricas' ? 'active' : ''}`}
            onClick={() => setActiveTab('metricas')}
          >
            📊 Métricas e Historial
          </button>
          <button 
            className={`tab-btn ${activeTab === 'blog' ? 'active' : ''}`}
            onClick={() => setActiveTab('blog')}
          >
            📚 Artículos Educativos
          </button>
          <button 
            className={`tab-btn ${activeTab === 'metodologia' ? 'active' : ''}`}
            onClick={() => setActiveTab('metodologia')}
          >
            📘 Metodología y Guía
          </button>
          <button 
            className={`tab-btn ${activeTab === 'acerca' ? 'active' : ''}`}
            onClick={() => setActiveTab('acerca')}
          >
            ℹ️ Acerca de
          </button>
          <button 
            className={`tab-btn ${activeTab === 'politicas' ? 'active' : ''}`}
            onClick={() => setActiveTab('politicas')}
          >
            ⚖️ Legal y Contacto
          </button>
        </nav>

        {/* Carga del Contenido según la Pestaña Activa */}
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Analizando historial y matrices de Markov con JAX...</p>
          </div>
        ) : error ? (
          <div className="alert alert-error">
            <span>❌ Error al cargar los datos: {error}</span>
          </div>
        ) : data ? (
          <div>
            {/* Cabecera de Resumen Rápido */}
            <div className="card" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '20px', background: 'rgba(59, 130, 246, 0.04)' }}>
              <div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Último sorteo analizado</span>
                <div className="balotas-container" style={{ margin: '8px 0 0 0' }}>
                  {data.last_combination.map((num, i) => (
                    <div key={i} className="balota balota-principal" style={{ width: '36px', height: '36px' }}>
                      <div className="balota-inner" style={{ width: '20px', height: '20px', fontSize: '12px' }}>{num}</div>
                    </div>
                  ))}
                  <div className="balota-separator" style={{ fontSize: '20px' }}>+</div>
                  <div className="balota balota-super" style={{ width: '36px', height: '36px' }}>
                    <div className="balota-inner" style={{ width: '20px', height: '20px', fontSize: '12px' }}>{data.last_sb}</div>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Score JAX Último</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-primary)' }}>{data.last_score !== undefined ? data.last_score.toFixed(6) : '0.000000'}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Prob. Markov Último</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-primary)' }}>{data.last_markov !== undefined ? formatProb(data.last_markov) : '0.000000'}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Mediana Histórica</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-primary)' }}>{data.score_mediana.toFixed(6)}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Combinaciones Posibles</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-blue)' }}>{data.total_combinations.toLocaleString()}</div>
                </div>
              </div>
            </div>

            {/* Anuncio Horizontal de Contenido */}
            <AdBanner slot="0987654321" format="horizontal" />

            {/* Contenido de la pestaña */}
            {activeTab === 'sugerencias' && (
              <Sugerencias 
                sorteo={sorteo} 
                scoreMediana={data.score_mediana} 
                scoreP75={data.score_p75} 
              />
            )}
            
            {activeTab === 'analizador' && (
              <AnalizadorManual 
                sorteo={sorteo} 
                scoreMediana={data.score_mediana} 
                scoreP75={data.score_p75}
                posTopData={data.pos_top_data}
              />
            )}

            {activeTab === 'rueda' && (
              <RuedaCombinatoria />
            )}
            
            {activeTab === 'metricas' && (
              <MetricasHistorial 
                sorteo={sorteo} 
                data={data}
              />
            )}
            
            {activeTab === 'blog' && (
              <Blog />
            )}
            
            {activeTab === 'metodologia' && (
              <Metodologia />
            )}

            {activeTab === 'acerca' && (
              <AcercaDe />
            )}

            {activeTab === 'politicas' && (
              <Politicas 
                activeSubTab={politicasSubTab}
                setActiveSubTab={setPoliticasSubTab}
              />
            )}
          </div>
        ) : null}

        {/* Footer para enlaces AdSense */}
        <footer className="dashboard-footer" style={{
          marginTop: '45px',
          padding: '30px 20px',
          borderTop: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '15px',
          color: 'var(--text-muted)',
          fontSize: '0.85rem',
          textAlign: 'center'
        }}>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onMouseEnter={(e) => e.target.style.color = 'var(--accent-blue)'}
              onMouseLeave={(e) => e.target.style.color = 'var(--text-muted)'}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('privacidad'); }}
            >
              🔒 Política de Privacidad
            </span>
            <span>|</span>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onMouseEnter={(e) => e.target.style.color = 'var(--accent-blue)'}
              onMouseLeave={(e) => e.target.style.color = 'var(--text-muted)'}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('terminos'); }}
            >
              📄 Términos y Condiciones
            </span>
            <span>|</span>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onMouseEnter={(e) => e.target.style.color = 'var(--accent-blue)'}
              onMouseLeave={(e) => e.target.style.color = 'var(--text-muted)'}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('cookies'); }}
            >
              🍪 Política de Cookies
            </span>
            <span>|</span>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onMouseEnter={(e) => e.target.style.color = 'var(--accent-blue)'}
              onMouseLeave={(e) => e.target.style.color = 'var(--text-muted)'}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('contacto'); }}
            >
              ✉️ Contacto
            </span>
          </div>
          <p style={{ margin: '5px 0 0 0', maxWidth: '700px', fontSize: '0.8rem', lineHeight: '1.6' }}>
            🎱 <strong>GanaBaloto Web</strong> © {new Date().getFullYear()}. Todos los derechos reservados. 
            Este sitio provee análisis estadístico descriptivo e histórico de sorteos de lotería colombianos. 
            No está afiliado, patrocinado ni asociado con Coljuegos, el operador oficial de Baloto/Revancha, ni ninguna entidad gubernamental de sorteos. 
            El análisis de datos sirve con fines de entretenimiento y divulgación probabilística. Juegue con responsabilidad.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;

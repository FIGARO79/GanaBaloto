import { useState, useEffect } from 'react';
import ConsolaAgente from './components/ConsolaAgente.jsx';
import Sugerencias from './components/Sugerencias.jsx';
import AnalizadorManual from './components/AnalizadorManual.jsx';
import RuedaCombinatoria from './components/RuedaCombinatoria.jsx';
import MetricasHistorial from './components/MetricasHistorial.jsx';
import Metodologia from './components/Metodologia.jsx';
import AcercaDe from './components/AcercaDe.jsx';
import Politicas from './components/Politicas.jsx';
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
    fetchSorteoData(sorteo);
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

  const regName = data?.regime_info?.current_regime || 'Equilibrio Central';
  const regProb = data?.regime_info?.transition_prob !== undefined ? data.regime_info.transition_prob.toFixed(2) : '0.85';

  return (
    <div className="dashboard-container">
      {/* Barra Lateral (Sidebar) */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-logo">GB</div>
          <span className="sidebar-brand-name">GanaBaloto</span>
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
          <div className="engine-box" style={{ marginBottom: '12px' }}>
            <span className="engine-title">Motor de Cálculo</span>
            <span className="engine-value">JAX (NVIDIA GPU / XLA)</span>
          </div>

          <div className="engine-box" style={{ background: 'rgba(59, 130, 246, 0.08)', borderColor: 'rgba(59, 130, 246, 0.2)' }}>
            <span className="engine-title">Régimen Dinámico (HMM)</span>
            <span className="engine-value" style={{ color: 'var(--accent-blue)', fontSize: '0.85rem' }}>
              {regName}
            </span>
          </div>
        </div>

        <div className="sidebar-section" style={{ marginTop: 'auto' }}>
          <button 
            className="btn btn-secondary" 
            onClick={recargarBaseDatos}
            disabled={reloadingDb}
            style={{ width: '100%', fontSize: '0.85rem' }}
          >
            {reloadingDb ? 'Recargando...' : 'Recargar Base de Datos'}
          </button>
        </div>
      </aside>

      {/* Contenido Principal */}
      <main className="main-content">
        <header className="main-header" style={{ marginBottom: '20px' }}>
          <div className="main-title-container">
            <div className="main-logo">GB</div>
            <div>
              <h1 className="main-title">GanaBaloto Intelligence</h1>
              <p className="main-subtitle">
                Motor de modelado estocástico multimodal, física estadística (Weibull & Ising) y aceleración JAX.
              </p>
            </div>
          </div>
        </header>

        {/* Navegación de Pestañas */}
        <nav className="tabs-navigation" style={{ marginBottom: '20px' }}>
          <button 
            className={`tab-btn ${activeTab === 'agente' ? 'active' : ''}`}
            onClick={() => setActiveTab('agente')}
            style={{ fontWeight: 'bold', borderBottom: activeTab === 'agente' ? '2px solid var(--accent-yellow)' : 'none' }}
          >
            Consola de Agente (Trigger)
          </button>
          <button 
            className={`tab-btn ${activeTab === 'sugerencias' ? 'active' : ''}`}
            onClick={() => setActiveTab('sugerencias')}
          >
            Sugerencias Inteligentes
          </button>
          <button 
            className={`tab-btn ${activeTab === 'analizador' ? 'active' : ''}`}
            onClick={() => setActiveTab('analizador')}
          >
            Analizador Manual (7D)
          </button>
          <button 
            className={`tab-btn ${activeTab === 'rueda' ? 'active' : ''}`}
            onClick={() => setActiveTab('rueda')}
          >
            Ruedas Reducidas
          </button>
          <button 
            className={`tab-btn ${activeTab === 'metricas' ? 'active' : ''}`}
            onClick={() => setActiveTab('metricas')}
          >
            Métricas e Historial
          </button>
          <button 
            className={`tab-btn ${activeTab === 'metodologia' ? 'active' : ''}`}
            onClick={() => setActiveTab('metodologia')}
          >
            Metodología y Modelos
          </button>
          <button 
            className={`tab-btn ${activeTab === 'acerca' ? 'active' : ''}`}
            onClick={() => setActiveTab('acerca')}
          >
            Acerca de
          </button>
          <button 
            className={`tab-btn ${activeTab === 'politicas' ? 'active' : ''}`}
            onClick={() => setActiveTab('politicas')}
          >
            Legal
          </button>
        </nav>

        {/* Estado de Carga / Error */}
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Sincronizando tensores de JAX, matrices de Ising y parámetros de Weibull...</p>
          </div>
        ) : error ? (
          <div className="alert alert-error">
            <span>Error al cargar los datos: {error}</span>
          </div>
        ) : data ? (
          <div>
            {/* Cabecera de Resumen y Métricas Clave del Sorteo */}
            <div className="card" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '20px', background: 'rgba(59, 130, 246, 0.04)', marginBottom: '24px' }}>
              <div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>
                  Última Extracción Registrada ({sorteo})
                </span>
                <div className="balotas-container" style={{ margin: '8px 0 0 0' }}>
                  {data.last_combination.map((num, i) => (
                    <div key={i} className="balota balota-principal" style={{ width: '38px', height: '38px' }}>
                      <div className="balota-inner" style={{ width: '22px', height: '22px', fontSize: '13px' }}>
                        {num < 10 ? `0${num}` : num}
                      </div>
                    </div>
                  ))}
                  <div className="balota-separator" style={{ fontSize: '20px' }}>+</div>
                  <div className="balota balota-super" style={{ width: '38px', height: '38px' }}>
                    <div className="balota-inner" style={{ width: '22px', height: '22px', fontSize: '13px' }}>
                      {data.last_sb < 10 ? `0${data.last_sb}` : data.last_sb}
                    </div>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Régimen (HMM)</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: '800', color: 'var(--accent-blue)' }}>{regName}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>P_persist: {regProb}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Meta ADN JAX</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: '800', color: 'var(--accent-green)' }}>{(data.score_meta || 0.1495).toFixed(4)}</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Promedio botes 5+1</div>
                </div>
                {data.lag_8_combination && data.lag_8_combination.length > 0 && (
                  <div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Resonancia Lag-8</div>
                    <div style={{ fontSize: '0.9rem', fontWeight: '700', color: 'var(--text-primary)' }}>
                      {data.lag_8_combination.map(x => x < 10 ? `0${x}` : x).join('-')}
                    </div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--accent-yellow)' }}>SB: [{data.lag_8_sb}]</div>
                  </div>
                )}
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 'bold', textTransform: 'uppercase' }}>Histórico</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: '800', color: 'var(--text-primary)' }}>{data.total_draws || 1022} sorteos</div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Base oficial baloto.json</div>
                </div>
              </div>
            </div>

            {/* Contenido de la pestaña activa */}
            {activeTab === 'agente' && (
              <ConsolaAgente />
            )}

            {activeTab === 'sugerencias' && (
              <Sugerencias 
                sorteo={sorteo} 
                scoreMediana={data.score_mediana} 
                scoreP75={data.score_p75}
                scoreMeta={data.score_meta}
              />
            )}
            
            {activeTab === 'analizador' && (
              <AnalizadorManual 
                sorteo={sorteo} 
                scoreMediana={data.score_mediana} 
                scoreP75={data.score_p75}
                scoreMeta={data.score_meta}
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

        {/* Footer Técnico y de Responsabilidad */}
        <footer className="dashboard-footer" style={{
          marginTop: '45px',
          padding: '24px 20px',
          borderTop: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '12px',
          color: 'var(--text-muted)',
          fontSize: '0.85rem',
          textAlign: 'center'
        }}>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('privacidad'); }}
            >
              Política de Privacidad
            </span>
            <span>•</span>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('terminos'); }}
            >
              Términos y Condiciones
            </span>
            <span>•</span>
            <span 
              style={{ cursor: 'pointer', transition: 'color 0.2s', fontWeight: '500' }}
              onClick={() => { setActiveTab('politicas'); setPoliticasSubTab('contacto'); }}
            >
              Contacto
            </span>
          </div>
          <p style={{ margin: '4px 0 0 0', maxWidth: '750px', fontSize: '0.8rem', lineHeight: '1.5' }}>
            <strong>GanaBaloto Intelligence</strong> © {new Date().getFullYear()}. Plataforma de computación estocástica y divulgación científica. 
            No está afiliada, patrocinada ni asociada con Coljuegos ni el operador oficial de Baloto/Revancha. 
            Los sorteos son eventos físicos independientes. Probabilidad teórica de 5+1: 1 en 15.401.568. Juegue con responsabilidad.
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;

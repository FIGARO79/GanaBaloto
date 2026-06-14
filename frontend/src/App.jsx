import React, { useState, useEffect } from 'react';
import Sugerencias from './components/Sugerencias.jsx';
import AnalizadorManual from './components/AnalizadorManual.jsx';
import MetricasHistorial from './components/MetricasHistorial.jsx';
import Metodologia from './components/Metodologia.jsx';
import './App.css';

function App() {
  const [sorteo, setSorteo] = useState('Baloto');
  const [activeTab, setActiveTab] = useState('sugerencias');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reloadingDb, setReloadingDb] = useState(false);

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
            className={`tab-btn ${activeTab === 'metricas' ? 'active' : ''}`}
            onClick={() => setActiveTab('metricas')}
          >
            📊 Métricas e Historial
          </button>
          <button 
            className={`tab-btn ${activeTab === 'metodologia' ? 'active' : ''}`}
            onClick={() => setActiveTab('metodologia')}
          >
            📘 Metodología y Guía
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
                  <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--text-primary)' }}>{data.last_markov !== undefined ? data.last_markov.toFixed(6) : '0.000000'}</div>
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

            {/* Contenido de la pestaña */}
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
                posTopData={data.pos_top_data}
              />
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
          </div>
        ) : null}
      </main>
    </div>
  );
}

export default App;

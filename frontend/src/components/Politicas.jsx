export default function Politicas({ activeSubTab, setActiveSubTab }) {

  return (
    <div className="politicas-section">
      <div className="card">
        <h3 className="card-title">⚖️ Legal, Políticas y Contacto</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', margin: '0' }}>
          En cumplimiento con las políticas de transparencia, protección de datos y el programa Google AdSense, ponemos a tu disposición los siguientes documentos legales y canales de comunicación.
        </p>
      </div>

      {/* Subnavegación de Políticas */}
      <nav className="tabs-navigation" style={{ marginBottom: '20px', background: 'var(--bg-secondary)', padding: '6px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
        <button 
          className={`tab-btn ${activeSubTab === 'privacidad' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('privacidad')}
          style={{ padding: '8px 12px', fontSize: '0.85rem' }}
        >
          🔒 Política de Privacidad
        </button>
        <button 
          className={`tab-btn ${activeSubTab === 'terminos' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('terminos')}
          style={{ padding: '8px 12px', fontSize: '0.85rem' }}
        >
          📄 Términos y Condiciones
        </button>
        <button 
          className={`tab-btn ${activeSubTab === 'cookies' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('cookies')}
          style={{ padding: '8px 12px', fontSize: '0.85rem' }}
        >
          🍪 Política de Cookies
        </button>
        <button 
          className={`tab-btn ${activeSubTab === 'contacto' ? 'active' : ''}`}
          onClick={() => setActiveSubTab('contacto')}
          style={{ padding: '8px 12px', fontSize: '0.85rem' }}
        >
          ✉️ Contacto y Soporte
        </button>
      </nav>

      {/* Contenido según la subpestaña */}
      {activeSubTab === 'privacidad' && (
        <div className="card" style={{ animation: 'fadeIn 0.2s ease', lineHeight: '1.7', color: 'var(--text-secondary)' }}>
          <h4 className="card-title" style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>🔒 Política de Privacidad</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Última actualización: 11 de Julio, 2026</p>
          
          <p>
            Tu privacidad es importante para nosotros. En esta Política de Privacidad se detalla qué tipo de información personal recopilamos, cómo la tratamos y cómo protegemos tus derechos al interactuar con el sitio web <strong>GanaBaloto Web</strong>.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>1. Información que recopilamos</h5>
          <p>
            Este sitio web no requiere registros de usuario ni almacena nombres, correos electrónicos o números telefónicos en sus servidores para su funcionamiento básico. La navegación es libre y anónima. Sin embargo, recopilamos información automatizada no identificable mediante archivos de registro de servidores, tales como la dirección IP, el tipo de navegador y la página de referencia, con fines meramente técnicos de seguridad y rendimiento.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>2. Cookies de Google AdSense y publicidad de terceros</h5>
          <p>
            Utilizamos servicios de publicidad de terceros, específicamente <strong>Google AdSense</strong>, para financiar el mantenimiento de este sitio. Google utiliza cookies para publicar anuncios en nuestro sitio web basados en las visitas anteriores de los usuarios a este u otros sitios web.
          </p>
          <ul>
            <li>
              El uso de cookies de publicidad (como la cookie de DoubleClick) permite a Google y a sus socios mostrar anuncios basados en las visitas de los usuarios a nuestros sitios y/o a otros sitios de Internet.
            </li>
            <li>
              Los usuarios pueden inhabilitar el uso de la publicidad personalizada. Para ello, deben acceder a la sección <a href="https://adssettings.google.com" target="_blank" rel="noopener noreferrer">Configuración de anuncios de Google</a>.
            </li>
            <li>
              Alternativamente, los usuarios pueden optar por evitar que terceros utilicen cookies para la publicidad personalizada visitando <a href="https://optout.aboutads.info" target="_blank" rel="noopener noreferrer">aboutads.info</a>.
            </li>
          </ul>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>3. Seguridad de los datos</h5>
          <p>
            Implementamos protocolos de seguridad estándar en la industria, incluyendo cifrado SSL de extremo a extremo, para evitar accesos no autorizados, alteraciones o pérdida de la información técnica recabada por los servidores de alojamiento.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>4. Enlaces a terceros</h5>
          <p>
            Este sitio web contiene enlaces a páginas oficiales de lotería (como Coljuegos o Baloto oficial) y servicios de terceros. No nos hacemos responsables de las políticas de privacidad ni del tratamiento de datos de dichos sitios externos. Te recomendamos revisar sus políticas al salir de nuestro sitio.
          </p>
        </div>
      )}

      {activeSubTab === 'terminos' && (
        <div className="card" style={{ animation: 'fadeIn 0.2s ease', lineHeight: '1.7', color: 'var(--text-secondary)' }}>
          <h4 className="card-title" style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>📄 Términos y Condiciones de Uso</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Última actualización: 11 de Julio, 2026</p>

          <p>
            Al acceder y utilizar el sitio web <strong>GanaBaloto Web</strong>, aceptas de manera incondicional cumplir con los siguientes términos y condiciones de uso. Si no estás de acuerdo con alguna parte de estas condiciones, te solicitamos abstenerte de utilizar la plataforma.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>1. Uso del sitio con fines informativos y educativos</h5>
          <p>
            GanaBaloto Web es una herramienta científica y educativa que procesa y visualiza estadísticas de sorteos históricos reales de Baloto y Revancha en Colombia mediante modelos estocásticos. <strong>Este sitio no es una plataforma de apuestas en línea, no vende boletos de lotería ni recauda dinero para juegos de azar.</strong>
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>2. Exclusión de Garantías y Limitación de Responsabilidad</h5>
          <p>
            A pesar de que el motor de cálculo matemático (JAX/NumPy) y los análisis de Cadenas de Markov están construidos con rigurosidad académica:
          </p>
          <ul>
            <li>
              <strong>No se garantizan premios ni resultados exitosos:</strong> Los sorteos de lotería reales son eventos gobernados por la aleatoriedad física y la independencia estadística. Los resultados pasados no determinan los resultados futuros.
            </li>
            <li>
              <strong>El usuario asume el riesgo:</strong> La decisión de apostar dinero en base a la información expuesta en este sitio es responsabilidad única y exclusiva del usuario. GanaBaloto Web y sus creadores declinan toda responsabilidad por pérdidas económicas derivadas del juego de azar.
            </li>
          </ul>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>3. Propiedad Intelectual</h5>
          <p>
            El diseño gráfico, la maquetación, los textos explicativos originales y el código fuente de los algoritmos son propiedad de GanaBaloto Web. Queda prohibida la reproducción parcial o total con fines comerciales sin autorización previa por escrito.
          </p>
        </div>
      )}

      {activeSubTab === 'cookies' && (
        <div className="card" style={{ animation: 'fadeIn 0.2s ease', lineHeight: '1.7', color: 'var(--text-secondary)' }}>
          <h4 className="card-title" style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>🍪 Política de Cookies</h4>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Última actualización: 11 de Julio, 2026</p>

          <p>
            En <strong>GanaBaloto Web</strong> utilizamos cookies propias y de terceros para optimizar la experiencia de navegación, analizar el tráfico del sitio y personalizar los anuncios que se te presentan.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>¿Qué es una cookie?</h5>
          <p>
            Una cookie es un pequeño archivo de texto que un sitio web almacena en tu navegador web. Permite que el sitio recuerde información sobre tu visita (como tu idioma de preferencia u otras opciones), lo que facilita tu próxima visita y hace que el sitio te resulte más útil.
          </p>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>¿Qué tipo de cookies utilizamos?</h5>
          <ul>
            <li>
              <strong>Cookies Técnicas y Esenciales:</strong> Necesarias para permitir la navegación por el sitio y el uso de sus diferentes opciones o servicios (como el control del tráfico y la carga dinámica de datos).
            </li>
            <li>
              <strong>Cookies Analíticas (de terceros):</strong> Nos permiten cuantificar el número de usuarios y realizar la medición y análisis estadístico de la utilización que hacen los usuarios de la web, con el fin de introducir mejoras técnicas.
            </li>
            <li>
              <strong>Cookies Publicitarias de Google AdSense:</strong> Permiten gestionar de la forma más eficaz posible la oferta de los espacios publicitarios del sitio web, adecuando el contenido del anuncio al uso realizado de nuestra página.
            </li>
          </ul>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '15px' }}>¿Cómo deshabilitar o configurar las cookies?</h5>
          <p>
            Puedes permitir, bloquear o eliminar las cookies instaladas en tu equipo mediante la configuración de las opciones del navegador instalado en tu ordenador o dispositivo móvil. A continuación se presentan enlaces directos a las guías de los principales navegadores:
          </p>
          <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', fontSize: '0.9rem', marginTop: '10px' }}>
            <a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer">Google Chrome</a>
            <a href="https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web-rastrear-preferencias" target="_blank" rel="noopener noreferrer">Mozilla Firefox</a>
            <a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer">Safari</a>
            <a href="https://support.microsoft.com/es-es/windows/eliminar-y-administrar-cookies-168dab11-0753-243d-7c16-ede5947fc64d" target="_blank" rel="noopener noreferrer">Microsoft Edge</a>
          </div>
        </div>
      )}

      {activeSubTab === 'contacto' && (
        <div className="card" style={{ animation: 'fadeIn 0.2s ease', lineHeight: '1.7', color: 'var(--text-secondary)' }}>
          <h4 className="card-title" style={{ fontSize: '1.3rem', color: 'var(--text-primary)' }}>✉️ Contacto y Soporte</h4>
          <p>
            ¿Tienes dudas, comentarios, sugerencias o requieres soporte técnico sobre el funcionamiento de la web? Puedes ponerte en contacto directo con nosotros. Estaremos encantados de atenderte.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginTop: '20px' }}>
            <div style={{ padding: '16px', background: 'var(--bg-primary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <h5 style={{ margin: '0 0 8px 0', fontSize: '1rem', color: 'var(--text-primary)' }}>📧 Correo Electrónico</h5>
              <p style={{ margin: '0 0 12px 0', fontWeight: 'bold' }}>soporte@ganabalotoweb.com</p>
              <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>Respondemos a todas tus inquietudes en un plazo máximo de 48 horas hábiles.</p>
            </div>
            
            <div style={{ padding: '16px', background: 'var(--bg-primary)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <h5 style={{ margin: '0 0 8px 0', fontSize: '1rem', color: 'var(--text-primary)' }}>📍 Ubicación y Autoría</h5>
              <p style={{ margin: '0 0 4px 0', fontWeight: 'bold' }}>GanaBaloto Inc.</p>
              <p style={{ margin: '0 0 12px 0', fontSize: '0.9rem' }}>Bogotá D.C., Colombia</p>
              <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-muted)' }}>Desarrollado de forma independiente con fines de investigación de datos.</p>
            </div>
          </div>

          <h5 style={{ color: 'var(--text-primary)', marginTop: '25px', marginBottom: '15px' }}>Formulario de Contacto Rápido</h5>
          <form onSubmit={(e) => { e.preventDefault(); alert('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.'); e.target.reset(); }} style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxWidth: '500px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 'bold', marginBottom: '4px' }}>Nombre completo</label>
              <input type="text" required style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 'bold', marginBottom: '4px' }}>Correo electrónico</label>
              <input type="email" required style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)' }} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 'bold', marginBottom: '4px' }}>Mensaje</label>
              <textarea required rows="4" style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-secondary)', color: 'var(--text-primary)', fontFamily: 'inherit' }}></textarea>
            </div>
            <button type="submit" className="btn btn-primary" style={{ alignSelf: 'flex-start', padding: '10px 20px' }}>Enviar Mensaje</button>
          </form>
        </div>
      )}
    </div>
  );
}

import { useEffect } from 'react';

/**
 * Componente reutilizable para bloques de anuncios (Google AdSense u otro servicio).
 * @param {string} slot - El identificador del bloque de anuncios provisto por tu ad network.
 * @param {string} format - Formato del anuncio (auto, horizontal, vertical, rectangle).
 * @param {boolean} responsive - Si el anuncio se ajusta al ancho del contenedor.
 */
const AdBanner = ({ slot, format = 'auto', responsive = true }) => {
  useEffect(() => {
    try {
      // Intenta inicializar el anuncio una vez que el componente se monta
      if (typeof window !== 'undefined') {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      }
    } catch (e) {
      console.warn('AdSense no está listo o fue bloqueado:', e);
    }
  }, []);

  return (
    <div 
      className="ad-container-wrapper" 
      style={{ 
        margin: '15px 0', 
        padding: '10px', 
        background: 'var(--bg-primary)', 
        borderRadius: '8px', 
        border: '1px dashed var(--border-color)',
        minHeight: '90px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative'
      }}
    >
      {/* Etiqueta decorativa para identificar el bloque en desarrollo */}
      <span 
        style={{ 
          position: 'absolute', 
          top: '2px', 
          left: '5px', 
          fontSize: '0.65rem', 
          color: 'var(--text-muted)', 
          fontWeight: 'bold', 
          textTransform: 'uppercase' 
        }}
      >
        Publicidad / Anuncio
      </span>

      <ins 
        className="adsbygoogle"
        style={{ display: 'block', width: '100%' }}
        data-ad-client="ca-pub-4632851046040252"
        data-ad-slot={slot || "0000000000"}
        data-ad-format={format}
        data-full-width-responsive={responsive ? "true" : "false"}
        aria-label="Publicidad"
      ></ins>
    </div>
  );
};

export default AdBanner;

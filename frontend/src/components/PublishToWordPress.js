import React, { useState } from 'react';
import './PublishToWordPress.css';

const PublishToWordPress = ({ article, onClose }) => {
  const [publishing, setPublishing] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [status, setStatus] = useState('draft'); // 'draft' o 'publish'
  const [publishedUrl, setPublishedUrl] = useState(null);

  if (!article) return null;

  const { title, content, affiliate_links, metadata } = article;

  const handlePublish = async () => {
    setPublishing(true);
    setError(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

      const response = await fetch(`${apiUrl}/publish_to_wordpress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title,
          content: content,
          affiliate_links: affiliate_links,
          error: metadata.error,
          model: metadata.model,
          status: status,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al publicar en WordPress');
      }

      const result = await response.json();
      setSuccess(true);
      setPublishedUrl(result.url);
      
      // Auto-cerrar después de 3 segundos
      setTimeout(() => {
        onClose();
      }, 3000);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="wordpress-modal">
      <div className="wordpress-modal-overlay" onClick={onClose} />
      
      <div className="wordpress-modal-content">
        <div className="modal-header">
          <h2>📝 Publicar en WordPress</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        {success ? (
          <div className="success-message">
            <h3>✅ ¡Publicado exitosamente!</h3>
            <p>El artículo se ha guardado como {status === 'draft' ? 'borrador' : 'publicado'}.</p>
            {publishedUrl && (
              <p>
                <strong>URL:</strong>{' '}
                <a href={publishedUrl} target="_blank" rel="noopener noreferrer">
                  {publishedUrl}
                </a>
              </p>
            )}
          </div>
        ) : (
          <>
            <div className="preview-section">
              <h3>Vista previa del artículo</h3>
              <div className="article-preview-small">
                <h4>{title}</h4>
                <p>{content.introduction}</p>
              </div>
            </div>

            <div className="status-selector">
              <label>
                <input
                  type="radio"
                  value="draft"
                  checked={status === 'draft'}
                  onChange={(e) => setStatus(e.target.value)}
                />
                📋 Guardar como borrador
              </label>
              <label>
                <input
                  type="radio"
                  value="publish"
                  checked={status === 'publish'}
                  onChange={(e) => setStatus(e.target.value)}
                />
                🚀 Publicar directamente
              </label>
            </div>

            <div className="info-box">
              <h4>Información que se publicará:</h4>
              <ul>
                <li><strong>Título:</strong> {title}</li>
                <li><strong>Modelo:</strong> {metadata.model}</li>
                <li><strong>Error:</strong> {metadata.error}</li>
                <li><strong>Categoría:</strong> Ayuda técnica (se creará si no existe)</li>
                <li><strong>Enlaces de afiliado:</strong> {affiliate_links.length} productos</li>
              </ul>
            </div>

            {error && (
              <div className="error-message-wordpress">
                <strong>⚠️ Error:</strong> {error}
              </div>
            )}

            <div className="modal-actions">
              <button
                onClick={onClose}
                className="cancel-button"
                disabled={publishing}
              >
                Cancelar
              </button>
              <button
                onClick={handlePublish}
                disabled={publishing}
                className={`publish-button ${publishing ? 'loading' : ''}`}
              >
                {publishing ? (
                  <>
                    <span className="spinner-small"></span>
                    Publicando...
                  </>
                ) : (
                  `${status === 'draft' ? 'Guardar' : 'Publicar'} en WordPress`
                )}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PublishToWordPress;

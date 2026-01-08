import React from 'react';
import './BatchResults.css';

const BatchResults = ({ batchResults, onPublishBatch, onNewBatch }) => {
  const { total, successful, failed, articles, errors_log } = batchResults;

  const handlePublishAll = () => {
    if (window.confirm(`¿Publicar los ${successful} artículos en WordPress?`)) {
      onPublishBatch(articles);
    }
  };

  const handleDownloadAll = () => {
    const data = JSON.stringify(articles, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `batch_articles_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="batch-results">
      {/* Resumen */}
      <div className="results-summary">
        <div className="summary-card">
          <div className="summary-icon">📊</div>
          <div className="summary-content">
            <h3>Total</h3>
            <p className="summary-number">{total}</p>
          </div>
        </div>
        
        <div className="summary-card success">
          <div className="summary-icon">✅</div>
          <div className="summary-content">
            <h3>Exitosos</h3>
            <p className="summary-number">{successful}</p>
          </div>
        </div>
        
        {failed > 0 && (
          <div className="summary-card error">
            <div className="summary-icon">❌</div>
            <div className="summary-content">
              <h3>Fallidos</h3>
              <p className="summary-number">{failed}</p>
            </div>
          </div>
        )}
      </div>

      {/* Acciones */}
      <div className="results-actions">
        <button onClick={handlePublishAll} className="btn-publish-all">
          📝 Publicar Todos en WordPress
        </button>
        <button onClick={handleDownloadAll} className="btn-download-all">
          💾 Descargar JSON
        </button>
        <button onClick={onNewBatch} className="btn-new-batch">
          🔄 Nueva Generación
        </button>
      </div>

      {/* Lista de artículos */}
      <div className="articles-list">
        <h3>📄 Artículos Generados</h3>
        
        {articles.map((article, index) => (
          <div key={index} className="article-card">
            <div className="article-header">
              <h4>{article.title}</h4>
              <span className="article-error">{article.metadata.error}</span>
            </div>
            
            <div className="article-preview">
              <p><strong>Introducción:</strong> {article.content.introduction.substring(0, 200)}...</p>
              
              {article.content.solution_steps && article.content.solution_steps.length > 0 && (
                <div className="solution-steps">
                  <strong>Pasos de solución:</strong>
                  <ol>
                    {article.content.solution_steps.slice(0, 3).map((step, i) => (
                      <li key={i}>{step}</li>
                    ))}
                  </ol>
                </div>
              )}
              
              {article.affiliate_links && article.affiliate_links.length > 0 && (
                <div className="products-count">
                  🛒 {article.affiliate_links.length} productos recomendados
                </div>
              )}
            </div>
            
            <div className="article-meta">
              <span>🔧 {article.metadata.model}</span>
              <span>📅 {new Date(article.metadata.generated_at).toLocaleString()}</span>
              <span className="article-status">{article.status}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Errores */}
      {errors_log && errors_log.length > 0 && (
        <div className="errors-section">
          <h3>⚠️ Errores Encontrados</h3>
          <ul className="errors-list">
            {errors_log.map((error, index) => (
              <li key={index}>
                <strong>{error.error}:</strong> {error.detail}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default BatchResults;

import React, { useState } from 'react';
import './ArticleResult.css';
import PublishToWordPress from './PublishToWordPress';

const ArticleResult = ({ article }) => {
  const [copied, setCopied] = useState(false);
  const [copyFormat, setCopyFormat] = useState('html'); // 'html' o 'markdown'
  const [showWordPressModal, setShowWordPressModal] = useState(false);

  if (!article) return null;

  const { title, content, affiliate_links, metadata } = article;

  // Formatear artículo para copiar
  const formatArticleHTML = () => {
    let html = `<article>\n`;
    html += `  <h1>${title}</h1>\n\n`;
    
    if (content.introduction) {
      html += `  <section class="introduction">\n`;
      html += `    <p>${content.introduction}</p>\n`;
      html += `  </section>\n\n`;
    }
    
    if (content.error_meaning) {
      html += `  <section class="error-meaning">\n`;
      html += `    <h2>¿Qué significa este error?</h2>\n`;
      html += `    <p>${content.error_meaning}</p>\n`;
      html += `  </section>\n\n`;
    }
    
    if (content.diagnosis) {
      html += `  <section class="diagnosis">\n`;
      html += `    <h2>Diagnóstico</h2>\n`;
      html += `    <p>${content.diagnosis}</p>\n`;
      html += `  </section>\n\n`;
    }
    
    if (content.solution_steps && content.solution_steps.length > 0) {
      html += `  <section class="solution">\n`;
      html += `    <h2>Solución paso a paso</h2>\n`;
      html += `    <ol>\n`;
      content.solution_steps.forEach(step => {
        html += `      <li>${step}</li>\n`;
      });
      html += `    </ol>\n`;
      html += `  </section>\n\n`;
    }
    
    if (content.common_failures && content.common_failures.length > 0) {
      html += `  <section class="common-failures">\n`;
      html += `    <h2>Fallos comunes relacionados</h2>\n`;
      html += `    <ul>\n`;
      content.common_failures.forEach(failure => {
        html += `      <li>${failure}</li>\n`;
      });
      html += `    </ul>\n`;
      html += `  </section>\n\n`;
    }
    
    if (affiliate_links && affiliate_links.length > 0) {
      html += `  <section class="recommended-products">\n`;
      html += `    <h2>Productos recomendados</h2>\n`;
      html += `    <div class="products">\n`;
      affiliate_links.forEach(product => {
        html += `      <div class="product">\n`;
        html += `        <h3>${product.name}</h3>\n`;
        html += `        <p>${product.reason}</p>\n`;
        html += `        <a href="${product.affiliate_link}" target="_blank" rel="noopener noreferrer">Ver en Amazon</a>\n`;
        html += `      </div>\n`;
      });
      html += `    </div>\n`;
      html += `  </section>\n`;
    }
    
    html += `</article>`;
    return html;
  };

  const formatArticleMarkdown = () => {
    let md = `# ${title}\n\n`;
    
    if (content.introduction) {
      md += `${content.introduction}\n\n`;
    }
    
    if (content.error_meaning) {
      md += `## ¿Qué significa este error?\n\n${content.error_meaning}\n\n`;
    }
    
    if (content.diagnosis) {
      md += `## Diagnóstico\n\n${content.diagnosis}\n\n`;
    }
    
    if (content.solution_steps && content.solution_steps.length > 0) {
      md += `## Solución paso a paso\n\n`;
      content.solution_steps.forEach((step, index) => {
        md += `${index + 1}. ${step}\n`;
      });
      md += `\n`;
    }
    
    if (content.common_failures && content.common_failures.length > 0) {
      md += `## Fallos comunes relacionados\n\n`;
      content.common_failures.forEach(failure => {
        md += `- ${failure}\n`;
      });
      md += `\n`;
    }
    
    if (affiliate_links && affiliate_links.length > 0) {
      md += `## Productos recomendados\n\n`;
      affiliate_links.forEach(product => {
        md += `### ${product.name}\n\n`;
        md += `${product.reason}\n\n`;
        md += `[Ver en Amazon](${product.affiliate_link})\n\n`;
      });
    }
    
    return md;
  };

  const handleCopyToClipboard = async () => {
    const content = copyFormat === 'html' ? formatArticleHTML() : formatArticleMarkdown();
    
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 3000);
    } catch (err) {
      console.error('Error al copiar:', err);
      alert('Error al copiar al portapapeles');
    }
  };

  const handleDownload = () => {
    const content = copyFormat === 'html' ? formatArticleHTML() : formatArticleMarkdown();
    const extension = copyFormat === 'html' ? 'html' : 'md';
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="article-result">
      <div className="result-header">
        <h2>✅ Artículo generado</h2>
        
        <div className="result-actions">
          <div className="format-selector">
            <label>Formato:</label>
            <select
              value={copyFormat}
              onChange={(e) => setCopyFormat(e.target.value)}
              className="format-select"
            >
              <option value="html">HTML</option>
              <option value="markdown">Markdown</option>
            </select>
          </div>
          
          <button
            onClick={handleCopyToClipboard}
            className={`action-button copy ${copied ? 'copied' : ''}`}
          >
            {copied ? '✓ Copiado' : '📋 Copiar'}
          </button>
          
          <button
            onClick={handleDownload}
            className="action-button download"
          >
            💾 Descargar
          </button>
          
          <button
            onClick={() => setShowWordPressModal(true)}
            className="action-button wordpress"
            title="Publicar en WordPress"
          >
            📝 WordPress
          </button>
        </div>
      </div>

      <div className="article-preview">
        <article className="article-content">
          <h1 className="article-title">{title}</h1>

          {content.introduction && (
            <section className="article-section introduction">
              <p>{content.introduction}</p>
            </section>
          )}

          {content.error_meaning && (
            <section className="article-section">
              <h2>¿Qué significa este error?</h2>
              <p>{content.error_meaning}</p>
            </section>
          )}

          {content.diagnosis && (
            <section className="article-section">
              <h2>Diagnóstico</h2>
              <p>{content.diagnosis}</p>
            </section>
          )}

          {content.solution_steps && content.solution_steps.length > 0 && (
            <section className="article-section">
              <h2>Solución paso a paso</h2>
              <ol className="solution-steps">
                {content.solution_steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </section>
          )}

          {content.common_failures && content.common_failures.length > 0 && (
            <section className="article-section">
              <h2>Fallos comunes relacionados</h2>
              <ul className="common-failures">
                {content.common_failures.map((failure, index) => (
                  <li key={index}>{failure}</li>
                ))}
              </ul>
            </section>
          )}

          {affiliate_links && affiliate_links.length > 0 && (
            <section className="article-section products">
              <h2>Productos recomendados</h2>
              <div className="products-grid">
                {affiliate_links.map((product, index) => (
                  <div key={index} className="product-card">
                    <h3>{product.name}</h3>
                    <p className="product-type">{product.type}</p>
                    <p className="product-reason">{product.reason}</p>
                    <a
                      href={product.affiliate_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="product-link"
                    >
                      Ver en Amazon →
                    </a>
                  </div>
                ))}
              </div>
            </section>
          )}
        </article>

        {metadata && (
          <div className="article-metadata">
            <h3>Información del proceso</h3>
            

      {/* Modal de WordPress */}
      {showWordPressModal && (
        <PublishToWordPress
          article={article}
          onClose={() => setShowWordPressModal(false)}
        />
      )}<ul>
              <li><strong>Modelo:</strong> {metadata.model}</li>
              <li><strong>Error:</strong> {metadata.error}</li>
              <li><strong>Chunks procesados:</strong> {metadata.pdf_chunks}</li>
              <li><strong>Longitud del texto:</strong> {metadata.text_length} caracteres</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default ArticleResult;

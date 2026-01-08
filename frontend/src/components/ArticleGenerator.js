import React, { useState } from 'react';
import './ArticleGenerator.css';

const ArticleGenerator = ({ onArticleGenerated }) => {
  const [formData, setFormData] = useState({
    pdfUrl: '',
    error: '',
    model: '',
  });
  const [pdfFile, setPdfFile] = useState(null);
  const [useFile, setUseFile] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      setError(null);
    } else {
      setError('Por favor selecciona un archivo PDF válido');
      setPdfFile(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      
      // Validar datos
      if (!formData.error || !formData.model) {
        throw new Error('Por favor completa todos los campos requeridos');
      }

      if (!useFile && !formData.pdfUrl) {
        throw new Error('Por favor proporciona una URL del PDF o sube un archivo');
      }

      if (useFile && !pdfFile) {
        throw new Error('Por favor selecciona un archivo PDF');
      }

      // TODO: Implementar subida de archivo cuando el backend esté listo
      // Por ahora solo soportamos URL
      if (useFile) {
        throw new Error('La subida de archivos estará disponible pronto. Por favor usa una URL del PDF.');
      }

      const response = await fetch(`${apiUrl}/generate_article`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pdf_url: formData.pdfUrl,
          error: formData.error,
          model: formData.model,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Error al generar el artículo');
      }

      const result = await response.json();
      onArticleGenerated(result);

    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="article-generator">
      <h2>Generar Artículo Técnico</h2>
      
      <form onSubmit={handleSubmit} className="generator-form">
        {/* Toggle entre URL y archivo */}
        <div className="input-mode-toggle">
          <label>
            <input
              type="radio"
              checked={!useFile}
              onChange={() => setUseFile(false)}
            />
            URL del PDF
          </label>
          <label>
            <input
              type="radio"
              checked={useFile}
              onChange={() => setUseFile(true)}
            />
            Subir archivo
          </label>
        </div>

        {/* Input de PDF */}
        {!useFile ? (
          <div className="form-group">
            <label htmlFor="pdfUrl">
              URL del Manual (PDF) <span className="required">*</span>
            </label>
            <input
              type="url"
              id="pdfUrl"
              name="pdfUrl"
              value={formData.pdfUrl}
              onChange={handleInputChange}
              placeholder="https://example.com/manual.pdf"
              required={!useFile}
              className="form-input"
            />
            <small className="form-hint">
              Proporciona la URL de un manual técnico en formato PDF
            </small>
          </div>
        ) : (
          <div className="form-group">
            <label htmlFor="pdfFile">
              Archivo PDF <span className="required">*</span>
            </label>
            <input
              type="file"
              id="pdfFile"
              accept=".pdf"
              onChange={handleFileChange}
              className="form-input-file"
            />
            {pdfFile && (
              <small className="form-hint success">
                ✓ {pdfFile.name} seleccionado
              </small>
            )}
          </div>
        )}

        {/* Error/Problema */}
        <div className="form-group">
          <label htmlFor="error">
            Error o Problema <span className="required">*</span>
          </label>
          <input
            type="text"
            id="error"
            name="error"
            value={formData.error}
            onChange={handleInputChange}
            placeholder="Ej: Error E03 - Fallo de comunicación"
            required
            className="form-input"
          />
          <small className="form-hint">
            Describe el error o problema técnico
          </small>
        </div>

        {/* Modelo del dispositivo */}
        <div className="form-group">
          <label htmlFor="model">
            Modelo del Dispositivo <span className="required">*</span>
          </label>
          <input
            type="text"
            id="model"
            name="model"
            value={formData.model}
            onChange={handleInputChange}
            placeholder="Ej: Amazon Echo Dot 4ta Generación"
            required
            className="form-input"
          />
          <small className="form-hint">
            Especifica el modelo exacto del producto
          </small>
        </div>

        {/* Error message */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {/* Submit button */}
        <button
          type="submit"
          disabled={loading}
          className={`submit-button ${loading ? 'loading' : ''}`}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Generando artículo...
            </>
          ) : (
            '✨ Generar Artículo'
          )}
        </button>
      </form>

      {loading && (
        <div className="loading-info">
          <p>⏳ Esto puede tardar 10-30 segundos...</p>
          <p>Estamos procesando el PDF y generando el artículo con IA</p>
        </div>
      )}
    </div>
  );
};

export default ArticleGenerator;

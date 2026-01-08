import React, { useState, useEffect } from 'react';
import { getSiteMetrics, getPageMetrics } from '../services/api';
import './MetricsDashboard.css';

const MetricsDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [siteMetrics, setSiteMetrics] = useState(null);
  const [selectedDays, setSelectedDays] = useState(30);
  const [pageUrl, setPageUrl] = useState('');
  const [pageMetrics, setPageMetrics] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSiteMetrics();
  }, [selectedDays]);

  const loadSiteMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getSiteMetrics(selectedDays);
      setSiteMetrics(data);
    } catch (err) {
      setError('Error al cargar métricas del sitio: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePageSearch = async (e) => {
    e.preventDefault();
    if (!pageUrl) return;

    try {
      setLoading(true);
      setError(null);
      const data = await getPageMetrics(pageUrl, selectedDays);
      setPageMetrics(data);
    } catch (err) {
      setError('Error al cargar métricas de página: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num;
  };

  const formatPercentage = (num) => {
    return (num * 100).toFixed(2) + '%';
  };

  return (
    <div className="metrics-dashboard">
      <div className="dashboard-header">
        <h2>📊 Google Search Console - Métricas de Tráfico</h2>
        
        {/* Selector de período */}
        <div className="period-selector">
          <label>Período:</label>
          <select value={selectedDays} onChange={(e) => setSelectedDays(Number(e.target.value))}>
            <option value={7}>Últimos 7 días</option>
            <option value={30}>Últimos 30 días</option>
            <option value={90}>Últimos 90 días</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          ⚠️ {error}
        </div>
      )}

      {/* Métricas del sitio */}
      {!loading && siteMetrics && (
        <div className="metrics-grid">
          <div className="metric-card impressions">
            <div className="metric-icon">👁️</div>
            <div className="metric-content">
              <h3>Impresiones</h3>
              <p className="metric-value">{formatNumber(siteMetrics.impressions || 0)}</p>
              <span className="metric-label">Veces que apareció en búsquedas</span>
            </div>
          </div>

          <div className="metric-card clicks">
            <div className="metric-icon">🖱️</div>
            <div className="metric-content">
              <h3>Clics</h3>
              <p className="metric-value">{formatNumber(siteMetrics.clicks || 0)}</p>
              <span className="metric-label">Visitas desde Google</span>
            </div>
          </div>

          <div className="metric-card ctr">
            <div className="metric-icon">📈</div>
            <div className="metric-content">
              <h3>CTR</h3>
              <p className="metric-value">{formatPercentage(siteMetrics.ctr || 0)}</p>
              <span className="metric-label">Tasa de clics</span>
            </div>
          </div>

          <div className="metric-card position">
            <div className="metric-icon">🎯</div>
            <div className="metric-content">
              <h3>Posición Media</h3>
              <p className="metric-value">{siteMetrics.position ? siteMetrics.position.toFixed(1) : '---'}</p>
              <span className="metric-label">En resultados de búsqueda</span>
            </div>
          </div>
        </div>
      )}

      {/* Búsqueda de página específica */}
      <div className="page-search">
        <h3>🔍 Métricas de Página Específica</h3>
        <form onSubmit={handlePageSearch} className="page-search-form">
          <input
            type="url"
            value={pageUrl}
            onChange={(e) => setPageUrl(e.target.value)}
            placeholder="https://tudominio.com/articulo"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
        </form>

        {pageMetrics && (
          <div className="page-metrics-result">
            <h4>📄 Métricas de: {pageUrl}</h4>
            <div className="metrics-grid-small">
              <div className="metric-small">
                <span className="metric-label">Impresiones</span>
                <p className="metric-value">{formatNumber(pageMetrics.impressions || 0)}</p>
              </div>
              <div className="metric-small">
                <span className="metric-label">Clics</span>
                <p className="metric-value">{formatNumber(pageMetrics.clicks || 0)}</p>
              </div>
              <div className="metric-small">
                <span className="metric-label">CTR</span>
                <p className="metric-value">{formatPercentage(pageMetrics.ctr || 0)}</p>
              </div>
              <div className="metric-small">
                <span className="metric-label">Posición</span>
                <p className="metric-value">{pageMetrics.position ? pageMetrics.position.toFixed(1) : '---'}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Información */}
      <div className="metrics-info">
        <h4>ℹ️ Información sobre las métricas</h4>
        <ul>
          <li><strong>Impresiones:</strong> Número de veces que tu sitio apareció en los resultados de búsqueda de Google.</li>
          <li><strong>Clics:</strong> Número de veces que los usuarios hicieron clic en tu sitio desde los resultados de búsqueda.</li>
          <li><strong>CTR (Click-Through Rate):</strong> Porcentaje de impresiones que resultaron en un clic (Clics / Impresiones).</li>
          <li><strong>Posición Media:</strong> Posición promedio de tu sitio en los resultados de búsqueda (1 = primera posición).</li>
        </ul>
      </div>

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Cargando métricas...</p>
        </div>
      )}
    </div>
  );
};

export default MetricsDashboard;

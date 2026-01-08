import React, { useState } from 'react';
import './App.css';
import ArticleGenerator from './components/ArticleGenerator';
import ArticleResult from './components/ArticleResult';
import BatchGenerator from './components/BatchGenerator';
import BatchResults from './components/BatchResults';
import MetricsDashboard from './components/MetricsDashboard';
import { batchPublish } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('single');
  const [generatedArticle, setGeneratedArticle] = useState(null);
  const [batchResults, setBatchResults] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [publishingBatch, setPublishingBatch] = useState(false);

  // Verificar estado de la API al cargar
  React.useEffect(() => {
    const checkAPI = async () => {
      try {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/health`);
        if (response.ok) {
          setApiStatus('online');
        } else {
          setApiStatus('offline');
        }
      } catch (error) {
        setApiStatus('offline');
      }
    };
    checkAPI();
  }, []);

  const handleArticleGenerated = (article) => {
    setGeneratedArticle(article);
    setTimeout(() => {
      document.querySelector('.article-result')?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }, 100);
  };

  const handleBatchGenerated = (results) => {
    setBatchResults(results);
    setTimeout(() => {
      document.querySelector('.batch-results')?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }, 100);
  };

  const handlePublishBatch = async (articles) => {
    try {
      setPublishingBatch(true);
      const result = await batchPublish(articles);
      
      if (result.success) {
        alert(`✅ ${result.published} artículos publicados exitosamente`);
      } else {
        alert(`⚠️ ${result.published} publicados, ${result.failed} fallaron`);
      }
    } catch (error) {
      alert('Error al publicar: ' + error.message);
    } finally {
      setPublishingBatch(false);
    }
  };

  const handleNewBatch = () => {
    setBatchResults(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleNewArticle = () => {
    setGeneratedArticle(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🤖 Generador de Artículos Técnicos</h1>
          <p>Genera artículos de ayuda técnica automáticamente con IA</p>
          
          <div className={`api-status ${apiStatus}`}>
            <span className="status-indicator"></span>
            {apiStatus === 'checking' && 'Verificando API...'}
            {apiStatus === 'online' && 'API conectada'}
            {apiStatus === 'offline' && '⚠️ API desconectada - Asegúrate de ejecutar el backend'}
          </div>
        </div>

        {/* Navegación por pestañas */}
        <nav className="nav-tabs">
          <button 
            className={`nav-tab ${activeTab === 'single' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('single');
              setGeneratedArticle(null);
            }}
          >
            ✏️ Artículo Individual
          </button>
          <button 
            className={`nav-tab ${activeTab === 'batch' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('batch');
              setGeneratedArticle(null);
            }}
          >
            🚀 Generación en Batch
          </button>
          <button 
            className={`nav-tab ${activeTab === 'metrics' ? 'active' : ''}`}
            onClick={() => setActiveTab('metrics')}
          >
            📊 Métricas
          </button>
        </nav>
      </header>

      <main className="App-main">
        {/* Tab: Artículo Individual */}
        {activeTab === 'single' && (
          <>
            <ArticleGenerator onArticleGenerated={handleArticleGenerated} />
            
            {generatedArticle && (
              <>
                <ArticleResult article={generatedArticle} />
                <div className="new-article-section">
                  <button onClick={handleNewArticle} className="new-article-button">
                    ✨ Generar otro artículo
                  </button>
                </div>
              </>
            )}
          </>
        )}

        {/* Tab: Batch */}
        {activeTab === 'batch' && (
          <>
            <BatchGenerator onBatchGenerated={handleBatchGenerated} />
            
            {batchResults && (
              <div className="batch-results">
                <BatchResults 
                  batchResults={batchResults}
                  onPublishBatch={handlePublishBatch}
                  onNewBatch={handleNewBatch}
                />
              </div>
            )}
          </>
        )}

        {/* Tab: Métricas */}
        {activeTab === 'metrics' && (
          <MetricsDashboard />
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by FastAPI + React + LangChain + GPT-4o + WordPress</p>
      </footer>
    </div>
  );
}

export default App;

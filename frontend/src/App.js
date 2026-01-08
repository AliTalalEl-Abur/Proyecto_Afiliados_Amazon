import React, { useState } from 'react';
import './App.css';
import ArticleGenerator from './components/ArticleGenerator';
import ArticleResult from './components/ArticleResult';

function App() {
  const [generatedArticle, setGeneratedArticle] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

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
    // Scroll suave al resultado
    setTimeout(() => {
      document.querySelector('.article-result')?.scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    }, 100);
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
      </header>

      <main className="App-main">
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
      </main>

      <footer className="App-footer">
        <p>Powered by FastAPI + React + LangChain + GPT-4o</p>
      </footer>
    </div>
  );
}

export default App;

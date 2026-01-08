import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },

  // Generar artículo desde URL de PDF
  async generateArticle(pdfUrl, error, model) {
    const response = await api.post('/generate_article', {
      pdf_url: pdfUrl,
      error: error,
      model: model,
    });
    return response.data;
  },

  // Subir PDF directamente
  async uploadPDF(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload_pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default apiService;

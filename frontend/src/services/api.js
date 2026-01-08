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
  
  // Publicar en WordPress
  async publishToWordPress(articleData) {
    const response = await api.post('/publish_to_wordpress', articleData);
    return response.data;
  },
  
  // Generación en batch
  async generateBatch(batchData) {
    const response = await api.post('/batch_generate', batchData);
    return response.data;
  },
  
  // Publicar múltiples artículos
  async batchPublish(articles) {
    const response = await api.post('/batch_publish', articles);
    return response.data;
  },
  
  // Obtener tipos de dispositivos
  async getDeviceTypes() {
    const response = await api.get('/device_types');
    return response.data;
  },
  
  // Métricas del sitio
  async getSiteMetrics(days = 30) {
    const response = await api.get(`/metrics/site?days=${days}`);
    return response.data;
  },
  
  // Métricas de página específica
  async getPageMetrics(url, days = 30) {
    const response = await api.get(`/metrics/page`, {
      params: { url, days }
    });
    return response.data;
  },
};

// Exportaciones individuales para compatibilidad
export const healthCheck = apiService.healthCheck;
export const generateArticle = apiService.generateArticle;
export const uploadPDF = apiService.uploadPDF;
export const publishToWordPress = apiService.publishToWordPress;
export const generateBatch = apiService.generateBatch;
export const batchPublish = apiService.batchPublish;
export const getDeviceTypes = apiService.getDeviceTypes;
export const getSiteMetrics = apiService.getSiteMetrics;
export const getPageMetrics = apiService.getPageMetrics;

export default apiService;

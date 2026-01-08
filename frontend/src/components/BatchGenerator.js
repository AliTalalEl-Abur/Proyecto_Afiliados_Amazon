import React, { useState, useEffect } from 'react';
import { generateBatch, getDeviceTypes } from '../services/api';
import './BatchGenerator.css';

const BatchGenerator = ({ onBatchGenerated }) => {
  const [loading, setLoading] = useState(false);
  const [deviceTypes, setDeviceTypes] = useState({});
  const [formData, setFormData] = useState({
    pdf_url: '',
    model: '',
    device_type: '',
    use_common_errors: false,
    errors: ['']
  });
  const [progress, setProgress] = useState({
    total: 0,
    current: 0,
    currentError: ''
  });

  useEffect(() => {
    // Cargar tipos de dispositivos disponibles
    const loadDeviceTypes = async () => {
      try {
        const types = await getDeviceTypes();
        setDeviceTypes(types);
      } catch (error) {
        console.error('Error cargando tipos de dispositivos:', error);
      }
    };
    
    loadDeviceTypes();
  }, []);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleDeviceTypeChange = (e) => {
    const deviceType = e.target.value;
    setFormData(prev => ({
      ...prev,
      device_type: deviceType,
      use_common_errors: deviceType !== ''
    }));
  };

  const handleErrorChange = (index, value) => {
    const newErrors = [...formData.errors];
    newErrors[index] = value;
    setFormData(prev => ({ ...prev, errors: newErrors }));
  };

  const addErrorField = () => {
    if (formData.errors.length < 10) {
      setFormData(prev => ({
        ...prev,
        errors: [...prev.errors, '']
      }));
    }
  };

  const removeErrorField = (index) => {
    if (formData.errors.length > 1) {
      const newErrors = formData.errors.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, errors: newErrors }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setProgress({ total: 0, current: 0, currentError: '' });

    try {
      const errors = formData.use_common_errors 
        ? [] 
        : formData.errors.filter(e => e.trim() !== '');

      if (!formData.use_common_errors && errors.length === 0) {
        alert('Debes especificar al menos un error o seleccionar errores comunes');
        setLoading(false);
        return;
      }

      const result = await generateBatch({
        pdf_url: formData.pdf_url,
        model: formData.model,
        device_type: formData.device_type,
        use_common_errors: formData.use_common_errors,
        errors: errors
      });

      setLoading(false);
      
      if (result.successful > 0) {
        onBatchGenerated(result);
      } else {
        alert('No se pudieron generar artículos. Revisa los errores.');
      }
      
    } catch (error) {
      setLoading(false);
      alert('Error al generar artículos: ' + error.message);
    }
  };

  return (
    <div className="batch-generator">
      <div className="batch-header">
        <h2>🚀 Generación en Batch</h2>
        <p>Genera hasta 10 artículos para el mismo dispositivo de forma automática</p>
      </div>

      <form onSubmit={handleSubmit} className="batch-form">
        {/* URL del PDF */}
        <div className="form-group">
          <label htmlFor="pdf_url">📄 URL del Manual PDF *</label>
          <input
            type="url"
            id="pdf_url"
            name="pdf_url"
            value={formData.pdf_url}
            onChange={handleInputChange}
            placeholder="https://ejemplo.com/manual.pdf"
            required
          />
        </div>

        {/* Modelo del dispositivo */}
        <div className="form-group">
          <label htmlFor="model">🔧 Modelo del Dispositivo *</label>
          <input
            type="text"
            id="model"
            name="model"
            value={formData.model}
            onChange={handleInputChange}
            placeholder="Ej: Echo Dot 4, TP-Link Archer C7"
            required
          />
        </div>

        {/* Tipo de dispositivo */}
        <div className="form-group">
          <label htmlFor="device_type">📱 Tipo de Dispositivo</label>
          <select
            id="device_type"
            name="device_type"
            value={formData.device_type}
            onChange={handleDeviceTypeChange}
          >
            <option value="">-- Selecciona para usar errores comunes --</option>
            {Object.entries(deviceTypes).map(([key, info]) => (
              <option key={key} value={key}>
                {info.name} ({info.errors_count} errores)
              </option>
            ))}
          </select>
          {formData.device_type && deviceTypes[formData.device_type] && (
            <small className="device-type-hint">
              📝 Ejemplos: {deviceTypes[formData.device_type].sample_errors.join(', ')}
            </small>
          )}
        </div>

        {/* Errores personalizados */}
        {!formData.use_common_errors && (
          <div className="form-group">
            <label>⚠️ Errores a Procesar (máx. 10)</label>
            {formData.errors.map((error, index) => (
              <div key={index} className="error-input-group">
                <input
                  type="text"
                  value={error}
                  onChange={(e) => handleErrorChange(index, e.target.value)}
                  placeholder={`Error ${index + 1}`}
                  required
                />
                {formData.errors.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeErrorField(index)}
                    className="btn-remove"
                  >
                    ✖
                  </button>
                )}
              </div>
            ))}
            {formData.errors.length < 10 && (
              <button
                type="button"
                onClick={addErrorField}
                className="btn-add-error"
              >
                + Agregar Error
              </button>
            )}
          </div>
        )}

        {/* Botón de submit */}
        <button
          type="submit"
          className="btn-generate-batch"
          disabled={loading}
        >
          {loading ? '⏳ Generando...' : '🚀 Generar Artículos'}
        </button>

        {/* Barra de progreso */}
        {loading && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill"
                style={{ width: `${(progress.current / progress.total) * 100}%` }}
              />
            </div>
            <p className="progress-text">
              Generando artículo {progress.current} de {progress.total}
              {progress.currentError && <><br />📄 {progress.currentError}</>}
            </p>
          </div>
        )}
      </form>

      {/* Información de ayuda */}
      <div className="batch-info">
        <h4>ℹ️ Información</h4>
        <ul>
          <li>✅ Genera entre 5 y 10 artículos automáticamente</li>
          <li>📝 Usa errores comunes o especifica los tuyos</li>
          <li>⚡ El PDF se procesa una sola vez para todos los artículos</li>
          <li>💾 Los artículos se generan como borradores</li>
        </ul>
      </div>
    </div>
  );
};

export default BatchGenerator;

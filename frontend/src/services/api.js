import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Sensor Data API
export const getSensorReadings = async (panelId = null, hours = 24, limit = 100) => {
  const params = { hours, limit }
  if (panelId) params.panel_id = panelId
  const response = await api.get('/api/sensor/readings', { params })
  return response.data
}

export const getLatestReading = async (panelId) => {
  const response = await api.get(`/api/sensor/readings/latest/${panelId}`)
  return response.data
}

// Analytics API
export const getAnalyticsSummary = async (panelId, hours = 24) => {
  const response = await api.get(`/api/analytics/summary/${panelId}`, {
    params: { hours }
  })
  return response.data
}

export const getPredictions = async (panelId = null, limit = 100) => {
  const params = { limit }
  if (panelId) params.panel_id = panelId
  const response = await api.get('/api/analytics/predictions', { params })
  return response.data
}

export const createPrediction = async (panelId) => {
  const response = await api.post(`/api/analytics/predict/${panelId}`)
  return response.data
}

export const getPerformanceTrend = async (panelId, hours = 168) => {
  const response = await api.get(`/api/analytics/trend/${panelId}`, {
    params: { hours }
  })
  return response.data
}

// Alerts API
export const getAlerts = async (panelId = null, status = 'open', limit = 100) => {
  const params = { status, limit }
  if (panelId) params.panel_id = panelId
  const response = await api.get('/api/alerts/', { params })
  return response.data
}

export const updateAlertStatus = async (alertId, newStatus) => {
  const response = await api.patch(`/api/alerts/${alertId}/status`, null, {
    params: { new_status: newStatus }
  })
  return response.data
}

// Health Check
export const getHealthCheck = async () => {
  const response = await api.get('/api/health')
  return response.data
}

export const getSystemStatus = async () => {
  const response = await api.get('/api/status')
  return response.data
}

export default api

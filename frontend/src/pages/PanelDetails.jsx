import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import DashboardCard from '../components/DashboardCard'
import PowerOutputChart from '../components/Charts/PowerOutputChart'
import EnvironmentalChart from '../components/Charts/EnvironmentalChart'
import AlertsPanel from '../components/AlertsPanel'
import { 
  getSensorReadings, 
  getAnalyticsSummary, 
  getLatestReading,
  createPrediction 
} from '../services/api'

const PanelDetails = () => {
  const { panelId } = useParams()
  const [analytics, setAnalytics] = useState(null)
  const [latestReading, setLatestReading] = useState(null)
  const [readings, setReadings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPanelData()
    const interval = setInterval(loadPanelData, 10000)
    return () => clearInterval(interval)
  }, [panelId])

  const loadPanelData = async () => {
    try {
      const [analyticsData, latest, readingsData] = await Promise.all([
        getAnalyticsSummary(panelId, 24),
        getLatestReading(panelId),
        getSensorReadings(panelId, 24, 100)
      ])
      
      setAnalytics(analyticsData)
      setLatestReading(latest)
      setReadings(readingsData)
    } catch (error) {
      console.error('Failed to load panel data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRunPrediction = async () => {
    try {
      await createPrediction(panelId)
      loadPanelData()
    } catch (error) {
      console.error('Prediction failed:', error)
    }
  }

  if (loading) {
    return <div className="text-center py-8">Loading panel details...</div>
  }

  if (!latestReading) {
    return <div className="text-center py-8">No data available for {panelId}</div>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <Link to="/" className="text-sm text-blue-600 hover:text-blue-800 mb-2 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">{panelId}</h1>
          <p className="text-gray-600">Detailed performance metrics</p>
        </div>
        <button
          onClick={handleRunPrediction}
          className="btn-primary"
        >
          Run Prediction
        </button>
      </div>

      {/* Current Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <DashboardCard
          title="Power Output"
          value={latestReading.power_output.toFixed(0)}
          unit="W"
          color="primary"
        />
        <DashboardCard
          title="Irradiance"
          value={latestReading.irradiance.toFixed(0)}
          unit="W/m²"
          color="secondary"
        />
        <DashboardCard
          title="Temperature"
          value={latestReading.temperature.toFixed(1)}
          unit="°C"
          color="warning"
        />
        <DashboardCard
          title="PM10"
          value={latestReading.pm10.toFixed(0)}
          unit="μg/m³"
          color={latestReading.pm10 > 150 ? 'danger' : 'success'}
        />
      </div>

      {/* Performance Chart */}
      <PowerOutputChart data={readings} />

      {/* Environmental Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <EnvironmentalChart 
          data={readings}
          metric="pm10"
          title="PM10 Dust Levels"
          color="#ef4444"
        />
        <EnvironmentalChart 
          data={readings}
          metric="temperature"
          title="Temperature"
          color="#f59e0b"
        />
        <EnvironmentalChart 
          data={readings}
          metric="humidity"
          title="Humidity"
          color="#3b82f6"
        />
        <EnvironmentalChart 
          data={readings}
          metric="irradiance"
          title="Solar Irradiance"
          color="#10b981"
        />
      </div>

      {/* Alerts */}
      <AlertsPanel panelId={panelId} />
    </div>
  )
}

export default PanelDetails

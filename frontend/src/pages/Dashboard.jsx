import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import DashboardCard from '../components/DashboardCard'
import AlertsPanel from '../components/AlertsPanel'
import PowerOutputChart from '../components/Charts/PowerOutputChart'
import { getSensorReadings, getSystemStatus, getAnalyticsSummary } from '../services/api'

const PANELS = ['panel_001', 'panel_002', 'panel_003']

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null)
  const [panelData, setPanelData] = useState({})
  const [recentReadings, setRecentReadings] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
    // Refresh every 10 seconds
    const interval = setInterval(loadDashboardData, 10000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      // Load system status
      const status = await getSystemStatus()
      setSystemStatus(status)

      // Load data for each panel
      const panelPromises = PANELS.map(async (panelId) => {
        const analytics = await getAnalyticsSummary(panelId, 24)
        return [panelId, analytics]
      })
      const results = await Promise.all(panelPromises)
      const panelDataMap = Object.fromEntries(results)
      setPanelData(panelDataMap)

      // Load recent readings for chart
      const readings = await getSensorReadings(null, 6, 50)
      setRecentReadings(readings)

    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  const totalPower = Object.values(panelData).reduce((sum, p) => sum + p.avg_power_output, 0)
  const avgDegradation = Object.values(panelData).reduce((sum, p) => sum + p.avg_degradation_score, 0) / PANELS.length

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Real-time solar panel performance monitoring</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Total Power Output"
          value={totalPower.toFixed(0)}
          unit="W"
          color="primary"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          }
        />
        
        <DashboardCard
          title="Active Panels"
          value={PANELS.length}
          unit="panels"
          color="success"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
        />
        
        <DashboardCard
          title="Avg Degradation"
          value={avgDegradation.toFixed(1)}
          unit="%"
          color={avgDegradation > 15 ? 'warning' : 'success'}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          }
        />
        
        <DashboardCard
          title="Total Readings"
          value={systemStatus?.statistics?.total_sensor_readings || 0}
          color="secondary"
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          }
        />
      </div>

      {/* Power Output Chart */}
      <PowerOutputChart data={recentReadings} />

      {/* Panel Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Solar Panels</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {PANELS.map(panelId => {
            const data = panelData[panelId]
            if (!data) return null

            return (
              <Link 
                key={panelId}
                to={`/panel/${panelId}`}
                className="card hover:shadow-lg transition-shadow cursor-pointer"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{panelId}</h3>
                    <p className="text-sm text-gray-500">Active</p>
                  </div>
                  <span className={`badge ${data.avg_degradation_score > 15 ? 'badge-warning' : 'badge-success'}`}>
                    {data.avg_degradation_score.toFixed(1)}% loss
                  </span>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Power Output:</span>
                    <span className="font-semibold">{data.avg_power_output.toFixed(0)} W</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Readings (24h):</span>
                    <span className="font-semibold">{data.total_readings}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Active Alerts:</span>
                    <span className={`font-semibold ${data.active_alerts > 0 ? 'text-red-600' : 'text-green-600'}`}>
                      {data.active_alerts}
                    </span>
                  </div>
                </div>
              </Link>
            )
          })}
        </div>
      </div>

      {/* Alerts Panel */}
      <AlertsPanel />
    </div>
  )
}

export default Dashboard

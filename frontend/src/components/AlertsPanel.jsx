import React, { useState, useEffect } from 'react'
import { getAlerts, updateAlertStatus } from '../services/api'
import { format } from 'date-fns'

const AlertsPanel = ({ panelId = null }) => {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAlerts()
    // Refresh every 30 seconds
    const interval = setInterval(loadAlerts, 30000)
    return () => clearInterval(interval)
  }, [panelId])

  const loadAlerts = async () => {
    try {
      const data = await getAlerts(panelId, 'open')
      setAlerts(data)
    } catch (error) {
      console.error('Failed to load alerts:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleResolve = async (alertId) => {
    try {
      await updateAlertStatus(alertId, 'resolved')
      loadAlerts()
    } catch (error) {
      console.error('Failed to resolve alert:', error)
    }
  }

  const getPriorityBadge = (priority) => {
    const badges = {
      critical: 'badge badge-danger',
      high: 'badge bg-orange-100 text-orange-800',
      normal: 'badge badge-warning',
      low: 'badge bg-blue-100 text-blue-800'
    }
    return badges[priority] || badges.normal
  }

  if (loading) {
    return <div className="card">Loading alerts...</div>
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Maintenance Alerts</h2>
        <span className="badge badge-danger">{alerts.length}</span>
      </div>

      {alerts.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <svg 
            className="w-16 h-16 mx-auto mb-2 text-green-500" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
          <p className="font-medium">No active alerts</p>
          <p className="text-sm">All systems operational</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div 
              key={alert.id}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className={getPriorityBadge(alert.priority)}>
                      {alert.priority.toUpperCase()}
                    </span>
                    <span className="text-sm text-gray-600">
                      {alert.panel_id}
                    </span>
                  </div>
                  <p className="text-gray-900 font-medium">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {format(new Date(alert.timestamp), 'MMM dd, yyyy HH:mm')}
                  </p>
                </div>
                <button
                  onClick={() => handleResolve(alert.id)}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Resolve
                </button>
              </div>
              {alert.estimated_days_until_critical && (
                <div className="text-sm text-orange-600 mt-2">
                  ⚠️ Critical in ~{alert.estimated_days_until_critical} days
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AlertsPanel

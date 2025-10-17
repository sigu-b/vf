import React, { useState, useEffect } from 'react'
import { getSystemStatus, getHealthCheck } from '../services/api'

const Settings = () => {
  const [systemStatus, setSystemStatus] = useState(null)
  const [healthStatus, setHealthStatus] = useState(null)

  useEffect(() => {
    loadSystemInfo()
  }, [])

  const loadSystemInfo = async () => {
    try {
      const [status, health] = await Promise.all([
        getSystemStatus(),
        getHealthCheck()
      ])
      setSystemStatus(status)
      setHealthStatus(health)
    } catch (error) {
      console.error('Failed to load system info:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-gray-600">System configuration and status</p>
      </div>

      {/* System Status */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-4">System Status</h2>
        <div className="space-y-3">
          <div className="flex justify-between py-2 border-b">
            <span className="text-gray-600">Status:</span>
            <span className="font-semibold text-green-600">
              {systemStatus?.status || 'Loading...'}
            </span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span className="text-gray-600">Total Sensor Readings:</span>
            <span className="font-semibold">
              {systemStatus?.statistics?.total_sensor_readings || 0}
            </span>
          </div>
          <div className="flex justify-between py-2 border-b">
            <span className="text-gray-600">Total Predictions:</span>
            <span className="font-semibold">
              {systemStatus?.statistics?.total_predictions || 0}
            </span>
          </div>
          <div className="flex justify-between py-2">
            <span className="text-gray-600">Open Alerts:</span>
            <span className="font-semibold text-orange-600">
              {systemStatus?.statistics?.open_maintenance_alerts || 0}
            </span>
          </div>
        </div>
      </div>

      {/* Configuration */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Configuration</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Degradation Alert Threshold
            </label>
            <input
              type="number"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary"
              defaultValue="15"
              disabled
            />
            <p className="text-xs text-gray-500 mt-1">Alert when degradation exceeds this percentage</p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data Refresh Interval
            </label>
            <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary" disabled>
              <option>10 seconds</option>
              <option>30 seconds</option>
              <option>1 minute</option>
            </select>
          </div>
        </div>
      </div>

      {/* About */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-800 mb-4">About</h2>
        <div className="space-y-2 text-sm text-gray-600">
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Description:</strong> AI-driven predictive maintenance system for solar panels</p>
          <p><strong>Technology Stack:</strong> FastAPI, React, PostgreSQL, Scikit-learn</p>
        </div>
      </div>
    </div>
  )
}

export default Settings

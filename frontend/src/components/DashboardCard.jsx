import React from 'react'

const DashboardCard = ({ title, value, unit, icon, color = 'primary', subtitle }) => {
  const colorClasses = {
    primary: 'text-primary bg-orange-50',
    secondary: 'text-secondary bg-blue-50',
    success: 'text-success bg-green-50',
    warning: 'text-warning bg-yellow-50',
    danger: 'text-danger bg-red-50',
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <div className="flex items-baseline space-x-2">
            <h3 className="text-3xl font-bold text-gray-900">
              {value}
            </h3>
            {unit && <span className="text-sm text-gray-500">{unit}</span>}
          </div>
          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}
        </div>
        {icon && (
          <div className={`p-3 rounded-full ${colorClasses[color]}`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}

export default DashboardCard

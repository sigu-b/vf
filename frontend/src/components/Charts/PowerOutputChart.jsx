import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { format } from 'date-fns'

const PowerOutputChart = ({ data }) => {
  const chartData = data.map(item => ({
    ...item,
    time: format(new Date(item.timestamp), 'HH:mm'),
    actual: item.power_output,
    predicted: item.predicted_output
  }))

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Power Output Trend</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis label={{ value: 'Power (W)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="actual" 
            stroke="#3b82f6" 
            strokeWidth={2}
            name="Actual Output"
            dot={false}
          />
          {chartData.some(d => d.predicted) && (
            <Line 
              type="monotone" 
              dataKey="predicted" 
              stroke="#f59e0b" 
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Predicted Output"
              dot={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PowerOutputChart

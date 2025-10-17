import React from 'react'
import { Link } from 'react-router-dom'

const NavBar = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3">
            <svg 
              className="w-8 h-8 text-primary" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" 
              />
            </svg>
            <div>
              <h1 className="text-xl font-bold text-gray-800">
                Solar Predictive Maintenance
              </h1>
              <p className="text-xs text-gray-500">AI-Powered Performance Monitoring</p>
            </div>
          </Link>
          
          <div className="flex space-x-6">
            <Link 
              to="/" 
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              Dashboard
            </Link>
            <Link 
              to="/settings" 
              className="text-gray-700 hover:text-primary transition-colors font-medium"
            >
              Settings
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default NavBar

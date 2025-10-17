import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import Dashboard from './pages/Dashboard'
import PanelDetails from './pages/PanelDetails'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <NavBar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/panel/:panelId" element={<PanelDetails />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

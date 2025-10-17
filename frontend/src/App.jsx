import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import PackageRegister from './pages/PackageRegister'
import PackageDetail from './pages/PackageDetail'
import Calculator from './pages/Calculator'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Toaster position="top-right" />
        <Header activeTab={activeTab} setActiveTab={setActiveTab} />

        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/register" element={<PackageRegister />} />
            <Route path="/package/:id" element={<PackageDetail />} />
            <Route path="/calculator" element={<Calculator />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App


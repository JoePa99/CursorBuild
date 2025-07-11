import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ContentStudio from './pages/ContentStudio';
import QAChat from './pages/QAChat';
import SalesGenerator from './pages/SalesGenerator';
import DocumentAnalysis from './pages/DocumentAnalysis';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/content-studio" element={<ContentStudio />} />
            <Route path="/qa-chat" element={<QAChat />} />
            <Route path="/sales-generator" element={<SalesGenerator />} />
            <Route path="/document-analysis" element={<DocumentAnalysis />} />
          </Routes>
        </main>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App; 
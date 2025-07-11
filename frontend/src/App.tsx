import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import CompanySetup from './pages/CompanySetup';
import KnowledgeBase from './pages/KnowledgeBase';
import ContextChat from './pages/ContextChat';
import KnowledgeGraph from './pages/KnowledgeGraph';
import BusinessIntelligence from './pages/BusinessIntelligence';
import DocumentManager from './pages/DocumentManager';
import Dashboard from './pages/Dashboard';

interface CompanyData {
  name: string;
  industry: string;
  description: string;
  business_processes: string[];
  goals: string[];
  context_summary: string;
  documents: any[];
}

function App() {
  const [companyData, setCompanyData] = useState<CompanyData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchCompanyContext();
  }, []);

  const fetchCompanyContext = async () => {
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/company-context');
      if (response.ok) {
        const data = await response.json();
        if (data.company.name) {
          setCompanyData(data.company);
        }
      }
    } catch (error) {
      console.error('Error fetching company context:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateCompanyData = (newData: CompanyData) => {
    setCompanyData(newData);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Blueprint AI...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {companyData ? (
          <>
            <Navbar companyData={companyData} />
            <main className="pt-16">
              <Routes>
                <Route path="/" element={<Dashboard companyData={companyData} />} />
                <Route path="/knowledge-base" element={<KnowledgeBase companyData={companyData} updateCompanyData={updateCompanyData} />} />
                <Route path="/knowledge-graph" element={<KnowledgeGraph companyData={companyData} />} />
                <Route path="/context-chat" element={<ContextChat companyData={companyData} />} />
                <Route path="/business-intelligence" element={<BusinessIntelligence companyData={companyData} />} />
                <Route path="/document-manager" element={<DocumentManager companyData={companyData} updateCompanyData={updateCompanyData} />} />
              </Routes>
            </main>
          </>
        ) : (
          <CompanySetup onSetupComplete={updateCompanyData} />
        )}
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
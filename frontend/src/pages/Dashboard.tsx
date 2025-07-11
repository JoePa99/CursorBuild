import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Upload, 
  Brain, 
  Database, 
  Network, 
  MessageSquare, 
  TrendingUp, 
  FileText, 
  Building2,
  ArrowRight,
  Sparkles
} from 'lucide-react';

interface CompanyData {
  name: string;
  industry: string;
  description: string;
  business_processes: string[];
  goals: string[];
  context_summary: string;
  documents: any[];
  departments: string[];
  products_services: string[];
  key_metrics: string[];
}

interface DashboardProps {
  companyData: CompanyData | null;
}

const Dashboard = ({ companyData }: DashboardProps) => {
  const hasCompanyData = companyData && companyData.name;

  if (!hasCompanyData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <Building2 className="h-16 w-16 text-primary-600 mr-4" />
            <div>
              <h1 className="text-4xl font-bold text-gray-900">Blueprint AI</h1>
              <p className="text-xl text-gray-600">Corporate Intelligence Platform</p>
            </div>
          </div>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Upload your company documents and let AI build your complete business intelligence system.
            No setup required - just upload and watch the magic happen.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          <div className="card text-center">
            <Upload className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Documents</h3>
            <p className="text-gray-600 mb-4">
              Upload PDFs, Word docs, and text files containing your company information
            </p>
            <Link to="/document-manager" className="btn-primary inline-flex items-center">
              <Upload className="h-4 w-4 mr-2" />
              Start Uploading
            </Link>
          </div>

          <div className="card text-center">
            <Sparkles className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Extraction</h3>
            <p className="text-gray-600 mb-4">
              AI automatically extracts company info, processes, goals, and builds knowledge graphs
            </p>
            <div className="text-sm text-gray-500">
              Happens automatically as you upload
            </div>
          </div>

          <div className="card text-center">
            <Brain className="h-12 w-12 text-primary-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Intelligence</h3>
            <p className="text-gray-600 mb-4">
              Access context-aware AI chat, business insights, and knowledge visualization
            </p>
            <div className="text-sm text-gray-500">
              Available after first upload
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">What Blueprint AI Does</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Automatic Company Discovery</h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Extracts company name, industry, and description
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Identifies business processes and departments
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Maps products, services, and key metrics
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Discovers business goals and objectives
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Intelligent Knowledge Building</h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Creates semantic search across all documents
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Builds knowledge graphs with entity relationships
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Enables context-aware AI conversations
                </li>
                <li className="flex items-start">
                  <ArrowRight className="h-4 w-4 text-primary-600 mr-2 mt-0.5 flex-shrink-0" />
                  Generates business content and insights
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome to {companyData.name}</h1>
        <p className="mt-2 text-gray-600">
          Your AI-powered corporate intelligence dashboard
        </p>
      </div>

      {/* Company Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Company Overview</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium text-gray-900">{companyData.name}</h3>
                <p className="text-gray-600">{companyData.industry}</p>
                <p className="text-gray-700 mt-2">{companyData.description}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Business Processes</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {companyData.business_processes.slice(0, 3).map((process, index) => (
                      <li key={index}>• {process}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Goals</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    {companyData.goals.slice(0, 3).map((goal, index) => (
                      <li key={index}>• {goal}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Stats</h2>
            <div className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-blue-800">Documents</p>
                    <p className="text-2xl font-bold text-blue-900">{companyData.documents.length}</p>
                  </div>
                  <FileText className="h-8 w-8 text-blue-600" />
                </div>
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-green-800">Departments</p>
                    <p className="text-2xl font-bold text-green-900">{companyData.departments.length}</p>
                  </div>
                  <Building2 className="h-8 w-8 text-green-600" />
                </div>
              </div>

              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-purple-800">Products/Services</p>
                    <p className="text-2xl font-bold text-purple-900">{companyData.products_services.length}</p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-purple-600" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link to="/document-manager" className="quick-action-card">
            <Upload className="h-6 w-6 text-primary-600" />
            <span>Upload Documents</span>
          </Link>
          
          <Link to="/context-chat" className="quick-action-card">
            <MessageSquare className="h-6 w-6 text-primary-600" />
            <span>AI Chat</span>
          </Link>
          
          <Link to="/knowledge-graph" className="quick-action-card">
            <Network className="h-6 w-6 text-primary-600" />
            <span>Knowledge Graph</span>
          </Link>
          
          <Link to="/business-intelligence" className="quick-action-card">
            <TrendingUp className="h-6 w-6 text-primary-600" />
            <span>Business Intelligence</span>
          </Link>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Documents</h2>
        {companyData.documents.length > 0 ? (
          <div className="space-y-3">
            {companyData.documents.slice(0, 5).map((doc, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium text-gray-900">{doc.filename}</p>
                    <p className="text-sm text-gray-500">{doc.content_type}</p>
                  </div>
                </div>
                <span className="text-sm text-gray-500">{doc.chunks} chunks</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Upload className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No documents uploaded yet</p>
            <Link to="/document-manager" className="text-primary-600 hover:text-primary-700">
              Upload your first document
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 
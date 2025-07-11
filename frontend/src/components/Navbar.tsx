import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Brain, MessageSquare, Database, TrendingUp, FileText, Building2 } from 'lucide-react';

interface CompanyData {
  name: string;
  industry: string;
  description: string;
  business_processes: string[];
  goals: string[];
  context_summary: string;
  documents: any[];
}

interface NavbarProps {
  companyData: CompanyData;
}

const Navbar = ({ companyData }: NavbarProps) => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Brain },
    { path: '/knowledge-base', label: 'Knowledge Base', icon: Database },
    { path: '/context-chat', label: 'Context Chat', icon: MessageSquare },
    { path: '/business-intelligence', label: 'Business Intelligence', icon: TrendingUp },
    { path: '/document-manager', label: 'Document Manager', icon: FileText },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Building2 className="h-8 w-8 text-primary-600" />
              <div>
                <span className="text-xl font-bold text-gray-900">Blueprint AI</span>
                {companyData.name && (
                  <p className="text-xs text-gray-500 -mt-1">{companyData.name}</p>
                )}
              </div>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden md:block text-right">
              <p className="text-sm font-medium text-gray-900">{companyData.industry}</p>
              <p className="text-xs text-gray-500">{companyData.documents.length} documents</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 
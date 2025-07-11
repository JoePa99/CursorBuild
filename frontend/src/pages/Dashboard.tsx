import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, MessageSquare, FileText, TrendingUp, Zap, Users, Clock, Target, Database, Building2 } from 'lucide-react';

interface CompanyData {
  name: string;
  industry: string;
  description: string;
  business_processes: string[];
  goals: string[];
  context_summary: string;
  documents: any[];
}

interface DashboardProps {
  companyData: CompanyData;
}

const Dashboard = ({ companyData }: DashboardProps) => {
  const features = [
    {
      title: 'Knowledge Base',
      description: 'View and manage your company knowledge',
      icon: Database,
      path: '/knowledge-base',
      color: 'bg-blue-500',
    },
    {
      title: 'Context Chat',
      description: 'AI conversations using company context',
      icon: MessageSquare,
      path: '/context-chat',
      color: 'bg-green-500',
    },
    {
      title: 'Business Intelligence',
      description: 'Generate context-aware business content',
      icon: TrendingUp,
      path: '/business-intelligence',
      color: 'bg-purple-500',
    },
    {
      title: 'Document Manager',
      description: 'Upload and process company documents',
      icon: FileText,
      path: '/document-manager',
      color: 'bg-orange-500',
    },
  ];

  const stats = [
    { label: 'Company', value: companyData.name, icon: Building2 },
    { label: 'Documents', value: companyData.documents.length.toString(), icon: Database },
    { label: 'Processes', value: companyData.business_processes.length.toString(), icon: Target },
    { label: 'Goals', value: companyData.goals.length.toString(), icon: TrendingUp },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Welcome to {companyData.name}</h1>
        <p className="mt-2 text-gray-600">
          Your AI-powered corporate intelligence platform for {companyData.industry}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="card">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Icon className="h-8 w-8 text-primary-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon;
          return (
            <Link
              key={feature.title}
              to={feature.path}
              className="card hover:shadow-lg transition-shadow duration-200 group"
            >
              <div className="flex items-center mb-4">
                <div className={`p-2 rounded-lg ${feature.color} text-white`}>
                  <Icon className="h-6 w-6" />
                </div>
                <h3 className="ml-3 text-lg font-semibold text-gray-900 group-hover:text-primary-600">
                  {feature.title}
                </h3>
              </div>
              <p className="text-gray-600">{feature.description}</p>
            </Link>
          );
        })}
      </div>

      {/* Quick Start */}
      <div className="mt-12 card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Start</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-primary-600 font-semibold">1</span>
            </div>
            <span className="text-gray-700">Choose a feature from above</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-primary-600 font-semibold">2</span>
            </div>
            <span className="text-gray-700">Input your requirements</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <span className="text-primary-600 font-semibold">3</span>
            </div>
            <span className="text-gray-700">Get AI-powered results</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 
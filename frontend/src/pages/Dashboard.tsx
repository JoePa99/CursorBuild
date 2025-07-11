import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, MessageSquare, FileText, TrendingUp, Zap, Users, Clock, Target } from 'lucide-react';

const Dashboard = () => {
  const features = [
    {
      title: 'Content Studio',
      description: 'Generate compelling content with AI assistance',
      icon: FileText,
      path: '/content-studio',
      color: 'bg-blue-500',
    },
    {
      title: 'Q&A Chat',
      description: 'Ask questions and get intelligent answers',
      icon: MessageSquare,
      path: '/qa-chat',
      color: 'bg-green-500',
    },
    {
      title: 'Sales Generator',
      description: 'Create persuasive sales content',
      icon: TrendingUp,
      path: '/sales-generator',
      color: 'bg-purple-500',
    },
    {
      title: 'Document Analysis',
      description: 'Analyze documents with AI insights',
      icon: Brain,
      path: '/document-analysis',
      color: 'bg-orange-500',
    },
  ];

  const stats = [
    { label: 'AI Models', value: '1', icon: Brain },
    { label: 'Features', value: '4', icon: Zap },
    { label: 'Response Time', value: '<2s', icon: Clock },
    { label: 'Accuracy', value: '95%', icon: Target },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Blueprint AI Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Your AI-powered corporate intelligence platform
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
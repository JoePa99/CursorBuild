import React, { useState } from 'react';
import { TrendingUp, FileText, Target, Users, Upload } from 'lucide-react';
import toast from 'react-hot-toast';

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

interface BusinessIntelligenceProps {
  companyData: CompanyData | null;
}

const BusinessIntelligence = ({ companyData }: BusinessIntelligenceProps) => {
  const [contentType, setContentType] = useState('email');
  const [topic, setTopic] = useState('');
  const [targetAudience, setTargetAudience] = useState('');
  const [tone, setTone] = useState('professional');
  const [generatedContent, setGeneratedContent] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const contentTypes = [
    { value: 'email', label: 'Email', icon: FileText },
    { value: 'proposal', label: 'Proposal', icon: FileText },
    { value: 'report', label: 'Report', icon: TrendingUp },
    { value: 'presentation', label: 'Presentation', icon: Target },
    { value: 'social_media', label: 'Social Media', icon: Users }
  ];

  const tones = [
    'professional',
    'friendly',
    'formal',
    'casual',
    'persuasive',
    'informative'
  ];

  const generateContent = async () => {
    if (!topic.trim() || !targetAudience.trim() || !companyData) return;

    setIsGenerating(true);
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/generate-business-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          content_type: contentType,
          topic: topic,
          target_audience: targetAudience,
          tone: tone
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedContent(data.content);
        toast.success('Content generated successfully!');
      } else {
        throw new Error('Failed to generate content');
      }
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Failed to generate content. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  if (!companyData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <TrendingUp className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Business Intelligence</h2>
          <p className="text-gray-600 mb-6">
            Upload some documents first to enable AI-powered business content generation
          </p>
          <a href="/document-manager" className="btn-primary inline-flex items-center">
            <Upload className="h-4 w-4 mr-2" />
            Upload Documents
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Business Intelligence</h1>
        <p className="mt-2 text-gray-600">
          Generate context-aware business content using your company's knowledge
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Content Generator */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2" />
            Content Generator
          </h2>
          
          <div className="space-y-4">
            {/* Content Type */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content Type
              </label>
              <div className="grid grid-cols-2 gap-2">
                {contentTypes.map((type) => {
                  const Icon = type.icon;
                  return (
                    <button
                      key={type.value}
                      onClick={() => setContentType(type.value)}
                      className={`flex items-center space-x-2 p-3 rounded-lg text-left transition-colors ${
                        contentType === type.value
                          ? 'bg-primary-50 text-primary-700 border border-primary-200'
                          : 'text-gray-600 hover:bg-gray-50 border border-gray-200'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      <span className="text-sm font-medium">{type.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Topic */}
            <div>
              <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                Topic *
              </label>
              <input
                type="text"
                id="topic"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Q4 sales strategy, new product launch, customer onboarding"
                className="input-field"
              />
            </div>

            {/* Target Audience */}
            <div>
              <label htmlFor="audience" className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience *
              </label>
              <input
                type="text"
                id="audience"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                placeholder="e.g., sales team, customers, investors, employees"
                className="input-field"
              />
            </div>

            {/* Tone */}
            <div>
              <label htmlFor="tone" className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                id="tone"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="input-field"
              >
                {tones.map((toneOption) => (
                  <option key={toneOption} value={toneOption}>
                    {toneOption.charAt(0).toUpperCase() + toneOption.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={generateContent}
              disabled={isGenerating || !topic.trim() || !targetAudience.trim()}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Generating Content...</span>
                </>
              ) : (
                <>
                  <TrendingUp className="h-4 w-4" />
                  <span>Generate Content</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Generated Content */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <FileText className="h-5 w-5 mr-2" />
            Generated Content
          </h2>
          
          {generatedContent ? (
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-2">Generated Content:</h3>
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">{generatedContent}</p>
                </div>
              </div>
              
              <div className="flex space-x-2">
                <button
                  onClick={() => navigator.clipboard.writeText(generatedContent)}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <FileText className="h-4 w-4" />
                  <span>Copy</span>
                </button>
                <button
                  onClick={() => setGeneratedContent('')}
                  className="btn-secondary flex items-center space-x-2"
                >
                  <span>Clear</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No content generated yet</p>
              <p className="text-sm mt-1">Fill out the form and click generate to create content</p>
            </div>
          )}
        </div>
      </div>

      {/* Company Context */}
      <div className="mt-8 card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Company Context</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">Business Processes</h3>
            <div className="space-y-1">
              {companyData.business_processes.slice(0, 3).map((process, index) => (
                <p key={index} className="text-xs text-gray-600">• {process}</p>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">Goals</h3>
            <div className="space-y-1">
              {companyData.goals.slice(0, 3).map((goal, index) => (
                <p key={index} className="text-xs text-gray-600">• {goal}</p>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">Products/Services</h3>
            <div className="space-y-1">
              {companyData.products_services.slice(0, 3).map((product, index) => (
                <p key={index} className="text-xs text-gray-600">• {product}</p>
              ))}
            </div>
          </div>
          
          <div>
            <h3 className="text-sm font-medium text-gray-900 mb-2">Key Metrics</h3>
            <div className="space-y-1">
              {companyData.key_metrics.slice(0, 3).map((metric, index) => (
                <p key={index} className="text-xs text-gray-600">• {metric}</p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BusinessIntelligence; 
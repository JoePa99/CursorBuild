import React, { useState } from 'react';
import { TrendingUp, FileText, Target, Users, Copy, Check, Send } from 'lucide-react';
import toast from 'react-hot-toast';

interface CompanyData {
  name: string;
  industry: string;
  description: string;
  business_processes: string[];
  goals: string[];
  context_summary: string;
  documents: any[];
}

interface BusinessIntelligenceProps {
  companyData: CompanyData;
}

const BusinessIntelligence = ({ companyData }: BusinessIntelligenceProps) => {
  const [formData, setFormData] = useState({
    content_type: '',
    topic: '',
    target_audience: '',
    tone: 'professional'
  });
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const contentTypes = [
    'Blog Post',
    'Email Campaign',
    'Sales Pitch',
    'Product Description',
    'Company Update',
    'Training Material',
    'Marketing Copy',
    'Process Documentation',
    'Customer Communication',
    'Internal Memo'
  ];

  const tones = [
    'Professional',
    'Casual',
    'Enthusiastic',
    'Authoritative',
    'Friendly',
    'Technical',
    'Persuasive'
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.content_type || !formData.topic) {
      toast.error('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    try {
      const formDataToSend = new FormData();
      formDataToSend.append('content_type', formData.content_type);
      formDataToSend.append('topic', formData.topic);
      formDataToSend.append('target_audience', formData.target_audience);
      formDataToSend.append('tone', formData.tone);

      const response = await fetch('https://cursorbuild-production.up.railway.app/generate-business-content', {
        method: 'POST',
        body: formDataToSend,
      });

      if (!response.ok) {
        throw new Error('Failed to generate content');
      }

      const data = await response.json();
      setContent(data.content);
      toast.success('Business content generated successfully!');
    } catch (error) {
      console.error('Error generating content:', error);
      toast.error('Failed to generate content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      toast.success('Content copied to clipboard!');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      toast.error('Failed to copy content');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Business Intelligence</h1>
        <p className="mt-2 text-gray-600">
          Generate intelligent business content using your company's context and knowledge
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Content Generation Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <TrendingUp className="h-5 w-5 mr-2" />
            Generate Business Content
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="content_type" className="block text-sm font-medium text-gray-700 mb-2">
                Content Type *
              </label>
              <select
                id="content_type"
                name="content_type"
                value={formData.content_type}
                onChange={handleInputChange}
                className="input-field"
                required
              >
                <option value="">Select Content Type</option>
                {contentTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="topic" className="block text-sm font-medium text-gray-700 mb-2">
                Topic/Subject *
              </label>
              <input
                type="text"
                id="topic"
                name="topic"
                value={formData.topic}
                onChange={handleInputChange}
                placeholder="e.g., New product launch, Q4 strategy, Customer success story"
                className="input-field"
                required
              />
            </div>

            <div>
              <label htmlFor="target_audience" className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <input
                type="text"
                id="target_audience"
                name="target_audience"
                value={formData.target_audience}
                onChange={handleInputChange}
                placeholder="e.g., Existing customers, Prospects, Internal team"
                className="input-field"
              />
            </div>

            <div>
              <label htmlFor="tone" className="block text-sm font-medium text-gray-700 mb-2">
                Tone
              </label>
              <select
                id="tone"
                name="tone"
                value={formData.tone}
                onChange={handleInputChange}
                className="input-field"
              >
                {tones.map((tone) => (
                  <option key={tone} value={tone.toLowerCase()}>{tone}</option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={isLoading || !formData.content_type || !formData.topic}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Generating Content...</span>
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  <span>Generate Business Content</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start">
              <Target className="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
              <div className="text-sm text-blue-800">
                <p className="font-medium">Context-Aware Generation:</p>
                <p className="mt-1">
                  Content is generated using your company's specific context, 
                  processes, and knowledge base for maximum relevance.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Generated Content */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <FileText className="h-5 w-5 mr-2" />
              Generated Content
            </h2>
            {content && (
              <button
                onClick={copyToClipboard}
                className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900"
              >
                {copied ? (
                  <>
                    <Check className="h-4 w-4" />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4" />
                    <span>Copy</span>
                  </>
                )}
              </button>
            )}
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 min-h-[400px]">
            {content ? (
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-gray-800 font-sans">{content}</pre>
              </div>
            ) : (
              <div className="flex items-center justify-center h-full text-gray-500">
                <Users className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <div className="text-center">
                  <p>Generated content will appear here</p>
                  <p className="text-sm mt-1">Content will be tailored to {companyData.name}</p>
                </div>
              </div>
            )}
          </div>

          {content && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-start">
                <TrendingUp className="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div className="text-sm text-green-800">
                  <p className="font-medium">Content Generated:</p>
                  <p className="mt-1">
                    This content is specifically tailored to {companyData.name}'s 
                    business context, processes, and goals.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BusinessIntelligence; 
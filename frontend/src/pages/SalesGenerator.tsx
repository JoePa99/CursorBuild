import React, { useState } from 'react';
import { Send, TrendingUp, Copy, Check, Target, Users, DollarSign } from 'lucide-react';
import toast from 'react-hot-toast';

const SalesGenerator = () => {
  const [formData, setFormData] = useState({
    product: '',
    targetAudience: '',
    painPoints: '',
    benefits: '',
    tone: 'professional',
  });
  const [content, setContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.product.trim()) return;

    setIsLoading(true);
    try {
      const prompt = `Create sales content for:
Product: ${formData.product}
Target Audience: ${formData.targetAudience}
Pain Points: ${formData.painPoints}
Benefits: ${formData.benefits}
Tone: ${formData.tone}

Generate compelling sales copy that addresses the pain points and highlights the benefits.`;

      const response = await fetch('https://cursorbuild-production.up.railway.app/generate-sales-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate sales content');
      }

      const data = await response.json();
      setContent(data.content);
      toast.success('Sales content generated successfully!');
    } catch (error) {
      console.error('Error generating sales content:', error);
      toast.error('Failed to generate sales content. Please try again.');
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
        <h1 className="text-3xl font-bold text-gray-900">Sales Generator</h1>
        <p className="mt-2 text-gray-600">
          Create persuasive sales content with AI assistance
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Sales Content Details
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="product" className="block text-sm font-medium text-gray-700 mb-2">
                Product/Service Name *
              </label>
              <input
                type="text"
                id="product"
                name="product"
                value={formData.product}
                onChange={handleInputChange}
                placeholder="e.g., AI-powered CRM solution"
                className="input-field"
                required
              />
            </div>

            <div>
              <label htmlFor="targetAudience" className="block text-sm font-medium text-gray-700 mb-2">
                Target Audience
              </label>
              <input
                type="text"
                id="targetAudience"
                name="targetAudience"
                value={formData.targetAudience}
                onChange={handleInputChange}
                placeholder="e.g., Small business owners, Sales managers"
                className="input-field"
              />
            </div>

            <div>
              <label htmlFor="painPoints" className="block text-sm font-medium text-gray-700 mb-2">
                Pain Points
              </label>
              <textarea
                id="painPoints"
                name="painPoints"
                value={formData.painPoints}
                onChange={handleInputChange}
                placeholder="e.g., Manual data entry, lost leads, poor customer tracking"
                className="input-field h-20 resize-none"
              />
            </div>

            <div>
              <label htmlFor="benefits" className="block text-sm font-medium text-gray-700 mb-2">
                Key Benefits
              </label>
              <textarea
                id="benefits"
                name="benefits"
                value={formData.benefits}
                onChange={handleInputChange}
                placeholder="e.g., Automated workflows, increased conversion rates, better insights"
                className="input-field h-20 resize-none"
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
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="enthusiastic">Enthusiastic</option>
                <option value="authoritative">Authoritative</option>
                <option value="friendly">Friendly</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isLoading || !formData.product.trim()}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <TrendingUp className="h-4 w-4" />
                  <span>Generate Sales Content</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Output Section */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <DollarSign className="h-5 w-5 mr-2" />
              Generated Sales Content
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
                <Users className="h-12 w-12 opacity-50" />
                <p className="ml-3">Generated sales content will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalesGenerator; 
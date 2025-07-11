import React, { useState } from 'react';
import { Building2, Target, Users, TrendingUp, CheckCircle } from 'lucide-react';
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

interface CompanySetupProps {
  onSetupComplete: (data: CompanyData) => void;
}

const CompanySetup = ({ onSetupComplete }: CompanySetupProps) => {
  const [formData, setFormData] = useState({
    name: '',
    industry: '',
    description: '',
    key_processes: [''],
    goals: ['']
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleArrayChange = (field: 'key_processes' | 'goals', index: number, value: string) => {
    const newArray = [...formData[field]];
    newArray[index] = value;
    setFormData({
      ...formData,
      [field]: newArray,
    });
  };

  const addArrayItem = (field: 'key_processes' | 'goals') => {
    setFormData({
      ...formData,
      [field]: [...formData[field], ''],
    });
  };

  const removeArrayItem = (field: 'key_processes' | 'goals', index: number) => {
    const newArray = formData[field].filter((_, i) => i !== index);
    setFormData({
      ...formData,
      [field]: newArray,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.industry.trim()) {
      toast.error('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/setup-company', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          industry: formData.industry,
          description: formData.description,
          key_processes: formData.key_processes.filter(p => p.trim()),
          goals: formData.goals.filter(g => g.trim())
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to setup company');
      }

      const data = await response.json();
      onSetupComplete(data.company_data);
      toast.success(`Welcome to ${formData.name}! Your company context has been configured.`);
    } catch (error) {
      console.error('Error setting up company:', error);
      toast.error('Failed to setup company. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8">
          <Building2 className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to Blueprint AI</h1>
          <p className="text-gray-600">Let's build your company's intelligent context</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Company Basic Info */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Building2 className="h-5 w-5 mr-2" />
                Company Information
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    placeholder="e.g., Acme Corp"
                    className="input-field"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
                    Industry *
                  </label>
                  <select
                    id="industry"
                    name="industry"
                    value={formData.industry}
                    onChange={handleInputChange}
                    className="input-field"
                    required
                  >
                    <option value="">Select Industry</option>
                    <option value="Technology">Technology</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Finance">Finance</option>
                    <option value="Retail">Retail</option>
                    <option value="Manufacturing">Manufacturing</option>
                    <option value="Education">Education</option>
                    <option value="Consulting">Consulting</option>
                    <option value="Real Estate">Real Estate</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div className="mt-4">
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                  Company Description
                </label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  placeholder="Describe your company, what you do, and your unique value proposition..."
                  className="input-field h-24 resize-none"
                />
              </div>
            </div>

            {/* Key Business Processes */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Target className="h-5 w-5 mr-2" />
                Key Business Processes
              </h3>
              
              {formData.key_processes.map((process, index) => (
                <div key={index} className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    value={process}
                    onChange={(e) => handleArrayChange('key_processes', index, e.target.value)}
                    placeholder="e.g., Customer onboarding, Product development"
                    className="input-field flex-1"
                  />
                  {formData.key_processes.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeArrayItem('key_processes', index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              
              <button
                type="button"
                onClick={() => addArrayItem('key_processes')}
                className="text-primary-600 hover:text-primary-800 text-sm font-medium"
              >
                + Add Process
              </button>
            </div>

            {/* Business Goals */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <TrendingUp className="h-5 w-5 mr-2" />
                Business Goals
              </h3>
              
              {formData.goals.map((goal, index) => (
                <div key={index} className="flex space-x-2 mb-2">
                  <input
                    type="text"
                    value={goal}
                    onChange={(e) => handleArrayChange('goals', index, e.target.value)}
                    placeholder="e.g., Increase market share by 25%"
                    className="input-field flex-1"
                  />
                  {formData.goals.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeArrayItem('goals', index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              
              <button
                type="button"
                onClick={() => addArrayItem('goals')}
                className="text-primary-600 hover:text-primary-800 text-sm font-medium"
              >
                + Add Goal
              </button>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Setting up your company...</span>
                </>
              ) : (
                <>
                  <CheckCircle className="h-4 w-4" />
                  <span>Setup Company Context</span>
                </>
              )}
            </button>
          </form>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>This information will be used to build your company's AI context</p>
          <p>You can update these details later in the settings</p>
        </div>
      </div>
    </div>
  );
};

export default CompanySetup; 
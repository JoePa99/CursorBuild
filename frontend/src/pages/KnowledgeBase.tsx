import React, { useState, useEffect } from 'react';
import { Database, Search, FileText, TrendingUp, Brain, Upload } from 'lucide-react';
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

interface KnowledgeBaseProps {
  companyData: CompanyData | null;
  updateCompanyData: (data: CompanyData) => void;
}

const KnowledgeBase = ({ companyData, updateCompanyData }: KnowledgeBaseProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<any>(null);

  const searchKnowledge = async () => {
    if (!searchQuery.trim() || !companyData) return;

    setIsSearching(true);
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/query-context', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          context_type: 'general'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSearchResults([data]);
        toast.success('Search completed successfully');
      }
    } catch (error) {
      console.error('Error searching knowledge base:', error);
      toast.error('Failed to search knowledge base');
    } finally {
      setIsSearching(false);
    }
  };

  const getDocumentStats = () => {
    if (!companyData) return { total: 0, types: {} };
    
    const types = companyData.documents.reduce((acc: any, doc: any) => {
      acc[doc.content_type] = (acc[doc.content_type] || 0) + 1;
      return acc;
    }, {});
    
    return {
      total: companyData.documents.length,
      types
    };
  };

  const stats = getDocumentStats();

  if (!companyData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <Database className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Knowledge Base</h2>
          <p className="text-gray-600 mb-6">
            Upload some documents first to build your knowledge base
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
        <h1 className="text-3xl font-bold text-gray-900">Knowledge Base</h1>
        <p className="mt-2 text-gray-600">
          Search and explore your company's knowledge and insights
        </p>
      </div>

      {/* Search Section */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Search className="h-5 w-5 mr-2" />
          Search Knowledge Base
        </h2>
        
        <div className="flex space-x-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Ask questions about your company, processes, or documents..."
            className="input-field flex-1"
            onKeyPress={(e) => e.key === 'Enter' && searchKnowledge()}
          />
          <button
            onClick={searchKnowledge}
            disabled={isSearching || !searchQuery.trim()}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSearching ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Searching...</span>
              </>
            ) : (
              <>
                <Search className="h-4 w-4" />
                <span>Search</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Knowledge Stats */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Database className="h-5 w-5 mr-2" />
              Knowledge Stats
            </h2>
            
            <div className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-blue-800">Total Documents</p>
                    <p className="text-2xl font-bold text-blue-900">{stats.total}</p>
                  </div>
                  <FileText className="h-8 w-8 text-blue-600" />
                </div>
              </div>

              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-green-800">Business Processes</p>
                    <p className="text-2xl font-bold text-green-900">{companyData.business_processes.length}</p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-green-600" />
                </div>
              </div>

              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-purple-800">Company Goals</p>
                    <p className="text-2xl font-bold text-purple-900">{companyData.goals.length}</p>
                  </div>
                  <Brain className="h-8 w-8 text-purple-600" />
                </div>
              </div>

              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-3">Document Types</h3>
                <div className="space-y-2">
                  {Object.entries(stats.types).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <span className="text-sm text-gray-700">{type}</span>
                      <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                        {count as number}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Search Results */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Brain className="h-5 w-5 mr-2" />
              Search Results
            </h2>
            
            {searchResults.length > 0 ? (
              <div className="space-y-4">
                {searchResults.map((result, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-6">
                    <div className="mb-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">Query: {result.query}</h3>
                      <p className="text-sm text-gray-600">Context Type: {result.context_type}</p>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">AI Response:</h4>
                      <p className="text-gray-700 whitespace-pre-wrap">{result.response}</p>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-gray-900">Relevant Documents:</span>
                        <span className="text-gray-600 ml-2">{result.relevant_documents.length}</span>
                      </div>
                      <div>
                        <span className="font-medium text-gray-900">Knowledge Graph Results:</span>
                        <span className="text-gray-600 ml-2">{result.knowledge_graph_results}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : searchQuery ? (
              <div className="text-center py-8 text-gray-500">
                <Search className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No results found for "{searchQuery}"</p>
                <p className="text-sm mt-1">Try searching for different terms</p>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Brain className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Search your knowledge base to find insights</p>
                <p className="text-sm mt-1">Ask questions about your company, processes, or documents</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase; 
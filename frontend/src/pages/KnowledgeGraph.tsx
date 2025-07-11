import React, { useState, useEffect } from 'react';
import { Network, Search, Database, TrendingUp, Users, FileText, Target, Upload } from 'lucide-react';
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

interface KnowledgeGraphProps {
  companyData: CompanyData | null;
}

interface GraphStats {
  node_types: Array<{type: string, count: number}>;
  relationship_types: Array<{type: string, count: number}>;
  total_nodes: number;
  total_relationships: number;
}

const KnowledgeGraph = ({ companyData }: KnowledgeGraphProps) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [graphStats, setGraphStats] = useState<GraphStats | null>(null);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (companyData) {
      fetchGraphStats();
    }
  }, [companyData]);

  const fetchGraphStats = async () => {
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/knowledge-graph-stats');
      if (response.ok) {
        const data = await response.json();
        setGraphStats(data);
      }
    } catch (error) {
      console.error('Error fetching graph stats:', error);
    }
  };

  const searchGraph = async () => {
    if (!searchQuery.trim() || !companyData) return;

    setIsLoading(true);
    try {
      const response = await fetch('https://cursorbuild-production.up.railway.app/query-knowledge-graph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: searchQuery,
          depth: 2
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.results);
        toast.success(`Found ${data.total_relationships} relationships`);
      }
    } catch (error) {
      console.error('Error searching graph:', error);
      toast.error('Failed to search knowledge graph');
    } finally {
      setIsLoading(false);
    }
  };

  const getNodeIcon = (nodeType: string) => {
    switch (nodeType) {
      case 'Company':
        return '🏢';
      case 'Process':
        return '⚙️';
      case 'Goal':
        return '🎯';
      case 'Entity':
        return '👤';
      case 'Concept':
        return '💡';
      case 'Document':
        return '📄';
      default:
        return '🔗';
    }
  };

  const getRelationshipColor = (relType: string) => {
    switch (relType) {
      case 'HAS_PROCESS':
        return 'text-blue-600';
      case 'HAS_GOAL':
        return 'text-green-600';
      case 'HAS_DOCUMENT':
        return 'text-purple-600';
      case 'MENTIONS':
        return 'text-orange-600';
      case 'RELATES_TO':
        return 'text-red-600';
      case 'DEFINES':
        return 'text-indigo-600';
      default:
        return 'text-gray-600';
    }
  };

  if (!companyData) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <Network className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Knowledge Graph</h2>
          <p className="text-gray-600 mb-6">
            Upload some documents first to build your knowledge graph
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
        <h1 className="text-3xl font-bold text-gray-900">Knowledge Graph</h1>
        <p className="mt-2 text-gray-600">
          Visualize your company's knowledge ontology and relationships
        </p>
      </div>

      {/* Search Section */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Search className="h-5 w-5 mr-2" />
          Search Knowledge Graph
        </h2>
        
        <div className="flex space-x-4">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for entities, relationships, or concepts..."
            className="input-field flex-1"
            onKeyPress={(e) => e.key === 'Enter' && searchGraph()}
          />
          <button
            onClick={searchGraph}
            disabled={isLoading || !searchQuery.trim()}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
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
        {/* Graph Statistics */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Database className="h-5 w-5 mr-2" />
              Graph Statistics
            </h2>
            
            {graphStats ? (
              <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-blue-800">Total Nodes</p>
                      <p className="text-2xl font-bold text-blue-900">{graphStats.total_nodes}</p>
                    </div>
                    <Database className="h-8 w-8 text-blue-600" />
                  </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-green-800">Total Relationships</p>
                      <p className="text-2xl font-bold text-green-900">{graphStats.total_relationships}</p>
                    </div>
                    <Network className="h-8 w-8 text-green-600" />
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-3">Node Types</h3>
                  <div className="space-y-2">
                    {graphStats.node_types.map((node, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <span className="text-sm text-gray-700">{node.type}</span>
                        <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                          {node.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-3">Relationship Types</h3>
                  <div className="space-y-2">
                    {graphStats.relationship_types.map((rel, index) => (
                      <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <span className="text-sm text-gray-700">{rel.type}</span>
                        <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded">
                          {rel.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Database className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Loading graph statistics...</p>
              </div>
            )}
          </div>
        </div>

        {/* Search Results */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
              <Network className="h-5 w-5 mr-2" />
              Graph Relationships
            </h2>
            
            {searchResults.length > 0 ? (
              <div className="space-y-4">
                {searchResults.slice(0, 10).map((result, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center space-x-4">
                      {result.n && (
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{getNodeIcon(result.n.labels?.[0] || 'Entity')}</span>
                          <div>
                            <p className="font-medium text-gray-900">{result.n.properties?.name || 'Unknown'}</p>
                            <p className="text-xs text-gray-500">{result.n.labels?.[0] || 'Entity'}</p>
                          </div>
                        </div>
                      )}
                      
                      {result.r && (
                        <div className="flex items-center space-x-2">
                          <span className="text-gray-400">→</span>
                          <span className={`text-sm font-medium ${getRelationshipColor(result.r.type)}`}>
                            {result.r.type}
                          </span>
                          <span className="text-gray-400">→</span>
                        </div>
                      )}
                      
                      {result.m && (
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{getNodeIcon(result.m.labels?.[0] || 'Entity')}</span>
                          <div>
                            <p className="font-medium text-gray-900">{result.m.properties?.name || 'Unknown'}</p>
                            <p className="text-xs text-gray-500">{result.m.labels?.[0] || 'Entity'}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : searchQuery ? (
              <div className="text-center py-8 text-gray-500">
                <Search className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No relationships found for "{searchQuery}"</p>
                <p className="text-sm mt-1">Try searching for different terms</p>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Network className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Search for entities and relationships in your knowledge graph</p>
                <p className="text-sm mt-1">Enter a query above to explore connections</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Knowledge Graph Info */}
      <div className="mt-8">
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">About Your Knowledge Graph</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <Target className="h-4 w-4 mr-2" />
                What It Contains
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Company structure and processes</li>
                <li>• Business goals and objectives</li>
                <li>• Document entities and concepts</li>
                <li>• Relationships between people, departments, and processes</li>
                <li>• Key business concepts and definitions</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-3 flex items-center">
                <TrendingUp className="h-4 w-4 mr-2" />
                How It Works
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Automatically extracts entities from uploaded documents</li>
                <li>• Identifies relationships between business concepts</li>
                <li>• Builds semantic connections across your knowledge base</li>
                <li>• Enables intelligent context-aware AI responses</li>
                <li>• Grows richer as you add more documents</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KnowledgeGraph; 
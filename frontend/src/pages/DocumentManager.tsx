import React, { useState } from 'react';
import { Upload, FileText, Database, Trash2, Eye, CheckCircle, AlertCircle } from 'lucide-react';
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

interface DocumentManagerProps {
  companyData: CompanyData | null;
  updateCompanyData: (data: CompanyData) => void;
}

const DocumentManager = ({ companyData, updateCompanyData }: DocumentManagerProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState('');
  const [description, setDescription] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const documentTypes = [
    'Company Policy',
    'Process Documentation',
    'Training Material',
    'Product Information',
    'Customer Data',
    'Financial Reports',
    'Marketing Content',
    'Technical Documentation',
    'Legal Documents',
    'Other'
  ];

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['.pdf', '.docx', '.txt', '.md'];
      const fileExt = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
      
      if (!allowedTypes.includes(fileExt)) {
        toast.error('Please select a PDF, DOCX, TXT, or MD file');
        return;
      }
      
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB');
        return;
      }
      
      setSelectedFile(file);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile || !documentType) {
      toast.error('Please select a file and document type');
      return;
    }

    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('document_type', documentType);
      formData.append('description', description);

      const response = await fetch('https://cursorbuild-production.up.railway.app/api/v1/documents/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Upload failed:', response.status, errorText);
        toast.error(`Failed to upload document: ${response.status}`);
        return;
      }

      const data = await response.json();
      if (!data || !data.document_info) {
        console.error('Upload succeeded but response is missing document_info:', data);
        toast.error('Upload succeeded but response is invalid.');
        return;
      }
      // Update company data with new document
      if (companyData) {
        const updatedCompanyData = {
          ...companyData,
          documents: [...companyData.documents, data.document_info]
        };
        updateCompanyData(updatedCompanyData);
      }

      toast.success(`Document "${selectedFile.name}" uploaded successfully!`);
      // Reset form
      setSelectedFile(null);
      setDocumentType('');
      setDescription('');
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error) {
      console.error('Error uploading document:', error);
      toast.error('Failed to upload document. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.toLowerCase().substring(filename.lastIndexOf('.'));
    switch (ext) {
      case '.pdf':
        return '📄';
      case '.docx':
        return '📝';
      case '.txt':
        return '📄';
      case '.md':
        return '📋';
      default:
        return '📄';
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Document Manager</h1>
        <p className="mt-2 text-gray-600">
          Upload and manage your company documents to build intelligent context
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <Upload className="h-5 w-5 mr-2" />
            Upload New Document
          </h2>
          
          <form onSubmit={handleUpload} className="space-y-4">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Document
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <input
                  type="file"
                  id="file-input"
                  onChange={handleFileSelect}
                  accept=".pdf,.docx,.txt,.md"
                  className="hidden"
                  disabled={isUploading}
                />
                <label
                  htmlFor="file-input"
                  className="cursor-pointer flex flex-col items-center"
                >
                  <Upload className="h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-sm text-gray-600">
                    {selectedFile ? selectedFile.name : 'Click to upload or drag and drop'}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Supports PDF, DOCX, TXT, MD (max 10MB)
                  </p>
                </label>
              </div>
            </div>

            {/* Document Type */}
            <div>
              <label htmlFor="documentType" className="block text-sm font-medium text-gray-700 mb-2">
                Document Type *
              </label>
              <select
                id="documentType"
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                className="input-field"
                required
                disabled={isUploading}
              >
                <option value="">Select Document Type</option>
                {documentTypes.map((type) => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description (Optional)
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of this document's content and purpose..."
                className="input-field h-20 resize-none"
                disabled={isUploading}
              />
            </div>

            <button
              type="submit"
              disabled={isUploading || !selectedFile || !documentType}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isUploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Processing Document...</span>
                </>
              ) : (
                <>
                  <Database className="h-4 w-4" />
                  <span>Add to Knowledge Base</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start">
              <CheckCircle className="h-4 w-4 text-blue-600 mt-0.5 mr-2" />
              <div className="text-sm text-blue-800">
                <p className="font-medium">Document Processing:</p>
                <p className="mt-1">
                  Documents are automatically parsed, chunked, and added to your company's 
                  vector knowledge base for context-aware AI responses.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Document Library */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <FileText className="h-5 w-5 mr-2" />
            Knowledge Base ({companyData?.documents?.length || 0} documents)
          </h2>
          
          <div className="space-y-4">
            {!companyData || companyData.documents.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No documents uploaded yet</p>
                <p className="text-sm">Upload your first document to start building context</p>
              </div>
            ) : (
              companyData?.documents?.map((doc, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3">
                      <span className="text-2xl">{getFileIcon(doc.filename)}</span>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900">{doc.filename}</h3>
                        <p className="text-sm text-gray-600">{doc.content_type}</p>
                        <p className="text-xs text-gray-500">
                          {doc.chunks} chunks • {(doc.size / 1024).toFixed(1)} KB
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="p-1 text-gray-400 hover:text-gray-600">
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="p-1 text-gray-400 hover:text-red-600">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {companyData && companyData.documents.length > 0 && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-start">
                <Database className="h-4 w-4 text-green-600 mt-0.5 mr-2" />
                <div className="text-sm text-green-800">
                  <p className="font-medium">Knowledge Base Active:</p>
                  <p className="mt-1">
                    Your documents are being used to provide context-aware responses 
                    in the Context Chat and Business Intelligence features.
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

export default DocumentManager; 
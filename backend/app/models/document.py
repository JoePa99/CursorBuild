from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from .base import BaseEntity

class DocumentStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    INDEXED = "indexed"

class DocumentType(str, Enum):
    """Supported document types"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    CSV = "csv"
    XLSX = "xlsx"
    PPTX = "pptx"

class DocumentSource(str, Enum):
    """Document source types"""
    UPLOAD = "upload"
    SALESFORCE = "salesforce"
    GOOGLE_DRIVE = "google_drive"
    SHAREPOINT = "sharepoint"
    SLACK = "slack"

class Document(BaseEntity):
    """Document model for knowledge core"""
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Storage path")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")
    document_type: DocumentType = Field(..., description="Document type")
    source: DocumentSource = Field(default=DocumentSource.UPLOAD, description="Document source")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED, description="Processing status")
    
    # Processing metadata
    extracted_text: Optional[str] = Field(default=None, description="Extracted text content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    processing_errors: List[str] = Field(default_factory=list, description="Processing errors")
    
    # Indexing information
    chunk_count: Optional[int] = Field(default=None, description="Number of text chunks")
    vectorized: bool = Field(default=False, description="Whether document is vectorized")
    graph_entities: List[str] = Field(default_factory=list, description="Extracted entities")

class DocumentUpload(BaseModel):
    """Document upload request model"""
    filename: str = Field(..., description="Original filename")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")
    source: DocumentSource = Field(default=DocumentSource.UPLOAD, description="Document source")

class DocumentChunk(BaseEntity):
    """Text chunk model for vector storage"""
    document_id: str = Field(..., description="Parent document ID")
    chunk_index: int = Field(..., description="Chunk index in document")
    content: str = Field(..., description="Chunk text content")
    start_position: int = Field(..., description="Start position in original text")
    end_position: int = Field(..., description="End position in original text")
    embedding: Optional[List[float]] = Field(default=None, description="Vector embedding")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chunk metadata")

class DocumentProcessingRequest(BaseModel):
    """Document processing request"""
    document_id: str = Field(..., description="Document ID to process")
    force_reprocess: bool = Field(default=False, description="Force reprocessing")

class DocumentSearchRequest(BaseModel):
    """Document search request"""
    query: str = Field(..., description="Search query")
    document_types: Optional[List[DocumentType]] = Field(default=None, description="Filter by document types")
    sources: Optional[List[DocumentSource]] = Field(default=None, description="Filter by sources")
    limit: int = Field(default=10, description="Maximum results")
    include_content: bool = Field(default=False, description="Include chunk content in results") 
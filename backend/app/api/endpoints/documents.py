from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import shutil
from pathlib import Path

from app.models.document import Document, DocumentUpload, DocumentProcessingRequest, DocumentSearchRequest
from app.models.base import BaseResponse, PaginatedResponse
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.services.knowledge_graph import KnowledgeGraph
from app.services.ai_service import AIService
from app.core.config import settings

router = APIRouter()

# Initialize services
document_processor = DocumentProcessor()
vector_store = VectorStore()
knowledge_graph = KnowledgeGraph()
ai_service = AIService()

@router.post("/upload", response_model=BaseResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source: str = "upload"
):
    """Upload a document for processing"""
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Validate file size
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Create document record
        document = Document(
            filename=file.filename,
            file_path="",  # Will be set after saving
            file_size=file.size,
            mime_type=file.content_type,
            document_type=file_extension[1:],  # Remove the dot
            source=source
        )
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{document.id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        document.file_path = file_path
        
        # Add metadata
        metadata = document_processor.get_document_metadata(file_path)
        document.metadata = metadata
        
        # Process document in background
        background_tasks.add_task(process_document_background, document)
        
        return BaseResponse(
            success=True,
            message="Document uploaded successfully. Processing started in background.",
            data={"document_id": str(document.id), "filename": document.filename}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/", response_model=PaginatedResponse)
async def list_documents(
    page: int = 1,
    size: int = 20,
    status: Optional[str] = None,
    document_type: Optional[str] = None
):
    """List uploaded documents with pagination"""
    try:
        # This would typically query a database
        # For now, return mock data
        documents = [
            {
                "id": "mock-id-1",
                "filename": "sample.pdf",
                "status": "processed",
                "document_type": "pdf",
                "file_size": 1024000,
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        return PaginatedResponse(
            success=True,
            data=documents,
            total=len(documents),
            page=page,
            size=size,
            pages=1
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

@router.get("/{document_id}", response_model=BaseResponse)
async def get_document(document_id: str):
    """Get document details"""
    try:
        # This would typically query a database
        # For now, return mock data
        document = {
            "id": document_id,
            "filename": "sample.pdf",
            "status": "processed",
            "document_type": "pdf",
            "file_size": 1024000,
            "chunk_count": 15,
            "vectorized": True,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        return BaseResponse(
            success=True,
            data=document
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document: {str(e)}")

@router.post("/{document_id}/process", response_model=BaseResponse)
async def process_document(document_id: str, request: DocumentProcessingRequest):
    """Manually trigger document processing"""
    try:
        # This would typically fetch the document from database
        # For now, return success
        return BaseResponse(
            success=True,
            message="Document processing started"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.post("/search", response_model=BaseResponse)
async def search_documents(request: DocumentSearchRequest):
    """Search documents using semantic search"""
    try:
        # Search in vector store
        results = await vector_store.search_similar(
            query=request.query,
            limit=request.limit,
            document_ids=request.sources if request.sources else None
        )
        
        return BaseResponse(
            success=True,
            data={
                "results": results,
                "query": request.query,
                "total_found": len(results)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.delete("/{document_id}", response_model=BaseResponse)
async def delete_document(document_id: str):
    """Delete a document and its associated data"""
    try:
        # Delete from vector store
        await vector_store.delete_document_chunks(document_id)
        
        # Delete from knowledge graph (entities/relationships)
        # This would require additional implementation
        
        # Delete file
        # This would require fetching the file path from database
        
        return BaseResponse(
            success=True,
            message="Document deleted successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")

@router.get("/{document_id}/download")
async def download_document(document_id: str):
    """Download a document file"""
    try:
        # This would typically fetch the file path from database
        # For now, return a mock file
        file_path = "uploads/sample.pdf"
        
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename="sample.pdf",
                media_type="application/pdf"
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

async def process_document_background(document: Document):
    """Background task for document processing"""
    try:
        # Process document
        processed_document, chunks = await document_processor.process_document(document)
        
        # Add chunks to vector store
        if chunks:
            await vector_store.add_chunks(chunks)
            processed_document.vectorized = True
        
        # Extract entities and relationships
        if processed_document.extracted_text:
            extraction_result = await ai_service.extract_entities_and_relationships(
                processed_document.extracted_text
            )
            
            # Create entities in knowledge graph
            for entity_data in extraction_result.get("entities", []):
                # This would create Entity objects and save to knowledge graph
                pass
            
            # Create relationships in knowledge graph
            for rel_data in extraction_result.get("relationships", []):
                # This would create Relationship objects and save to knowledge graph
                pass
        
        # Update document status
        processed_document.status = "indexed"
        
        # This would save the updated document to database
        
    except Exception as e:
        # Update document status to failed
        document.status = "failed"
        document.processing_errors.append(str(e))
        # This would save the updated document to database 
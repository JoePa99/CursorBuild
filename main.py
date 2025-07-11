#!/usr/bin/env python3
"""
Blueprint AI - Corporate Intelligence Platform
Root entry point for Railway deployment
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
import uuid
from typing import List, Optional
import google.generativeai as genai
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
import hashlib
import fitz  # PyMuPDF
from docx import Document
import tempfile
import shutil

# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

app = FastAPI(title="Blueprint AI - Corporate Intelligence Platform", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB for vector storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="company_knowledge",
    metadata={"description": "Company knowledge base and context"}
)

# Store company metadata
company_data = {
    "name": "",
    "industry": "",
    "documents": [],
    "context_summary": "",
    "business_processes": [],
    "key_metrics": []
}

class CompanySetup(BaseModel):
    name: str
    industry: str
    description: str
    key_processes: List[str]
    goals: List[str]

class ContextQuery(BaseModel):
    query: str
    context_type: str = "general"  # general, sales, support, process, etc.

class DocumentInfo(BaseModel):
    filename: str
    content_type: str
    size: int
    chunks: int

@app.get("/")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Blueprint AI Corporate Intelligence Platform",
        "version": "2.0.0",
        "company_configured": bool(company_data["name"]),
        "documents_loaded": len(company_data["documents"])
    }

@app.post("/setup-company")
async def setup_company(setup: CompanySetup):
    """Initialize company context and business profile"""
    global company_data
    
    company_data.update({
        "name": setup.name,
        "industry": setup.industry,
        "description": setup.description,
        "business_processes": setup.key_processes,
        "goals": setup.goals
    })
    
    # Generate initial context summary
    context_prompt = f"""
    Company: {setup.name}
    Industry: {setup.industry}
    Description: {setup.description}
    Key Processes: {', '.join(setup.key_processes)}
    Goals: {', '.join(setup.goals)}
    
    Create a comprehensive business context summary that captures the essence of this company.
    Include typical challenges, opportunities, and business context for this type of organization.
    """
    
    if GOOGLE_API_KEY:
        response = model.generate_content(context_prompt)
        company_data["context_summary"] = response.text
    
    return {
        "status": "success",
        "message": f"Company {setup.name} configured successfully",
        "company_data": company_data
    }

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    description: str = Form("")
):
    """Upload and process company documents for context building"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Validate file type
    allowed_types = ['.pdf', '.docx', '.txt', '.md']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File type {file_ext} not supported")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
    
    try:
        # Extract text based on file type
        text_content = ""
        if file_ext == '.pdf':
            doc = fitz.open(temp_path)
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            doc.close()
        elif file_ext == '.docx':
            doc = Document(temp_path)
            text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:  # .txt or .md
            with open(temp_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        
        # Split into chunks for vector storage
        chunks = split_text_into_chunks(text_content, 1000)
        
        # Store in vector database
        document_id = str(uuid.uuid4())
        collection.add(
            documents=chunks,
            metadatas=[{
                "filename": file.filename,
                "document_type": document_type,
                "description": description,
                "chunk_index": i
            } for i in range(len(chunks))],
            ids=[f"{document_id}_{i}" for i in range(len(chunks))]
        )
        
        # Update company data
        doc_info = DocumentInfo(
            filename=file.filename,
            content_type=document_type,
            size=len(text_content),
            chunks=len(chunks)
        )
        company_data["documents"].append(doc_info.dict())
        
        return {
            "status": "success",
            "message": f"Document {file.filename} processed successfully",
            "chunks_created": len(chunks),
            "document_info": doc_info.dict()
        }
        
    finally:
        os.unlink(temp_path)

@app.post("/query-context")
async def query_context(query: ContextQuery):
    """Query company knowledge with full context awareness"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Search relevant documents
    results = collection.query(
        query_texts=[query.query],
        n_results=5
    )
    
    # Build context from company data and relevant documents
    context = build_context(query.query, results, query.context_type)
    
    # Generate AI response with full context
    if GOOGLE_API_KEY:
        response = generate_contextual_response(query.query, context, query.context_type)
    else:
        response = "AI service not configured"
    
    return {
        "query": query.query,
        "context_type": query.context_type,
        "response": response,
        "relevant_documents": results["metadatas"][0] if results["metadatas"] else [],
        "context_used": context["summary"]
    }

@app.get("/company-context")
async def get_company_context():
    """Get current company context and knowledge base status"""
    return {
        "company": company_data,
        "knowledge_base": {
            "total_documents": len(company_data["documents"]),
            "total_chunks": sum(doc["chunks"] for doc in company_data["documents"]),
            "document_types": list(set(doc["content_type"] for doc in company_data["documents"]))
        }
    }

@app.post("/generate-business-content")
async def generate_business_content(
    content_type: str = Form(...),
    topic: str = Form(...),
    target_audience: str = Form(...),
    tone: str = Form("professional")
):
    """Generate business content using company context"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Build business context
    business_context = f"""
    Company: {company_data['name']}
    Industry: {company_data['industry']}
    Context: {company_data['context_summary']}
    Processes: {', '.join(company_data['business_processes'])}
    Goals: {', '.join(company_data['goals'])}
    """
    
    # Generate content with company context
    prompt = f"""
    {business_context}
    
    Generate {content_type} about: {topic}
    Target Audience: {target_audience}
    Tone: {tone}
    
    Make this content highly relevant to {company_data['name']} and their specific business context.
    """
    
    if GOOGLE_API_KEY:
        response = model.generate_content(prompt)
        content = response.text
    else:
        content = "AI service not configured"
    
    return {
        "content_type": content_type,
        "topic": topic,
        "content": content,
        "context_used": business_context
    }

def split_text_into_chunks(text: str, chunk_size: int) -> List[str]:
    """Split text into overlapping chunks for better context"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size // 2):  # 50% overlap
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def build_context(query: str, search_results: dict, context_type: str) -> dict:
    """Build comprehensive context from company data and search results"""
    
    # Extract relevant document content
    relevant_docs = []
    if search_results["documents"]:
        relevant_docs = search_results["documents"][0]
    
    # Build context summary
    context_summary = f"""
    Company Context:
    - Name: {company_data['name']}
    - Industry: {company_data['industry']}
    - Business Context: {company_data['context_summary']}
    
    Query Context: {query}
    Context Type: {context_type}
    
    Relevant Company Knowledge:
    {chr(10).join(relevant_docs[:3]) if relevant_docs else 'No specific documents found'}
    """
    
    return {
        "summary": context_summary,
        "relevant_documents": relevant_docs,
        "company_data": company_data
    }

def generate_contextual_response(query: str, context: dict, context_type: str) -> str:
    """Generate AI response with full company context"""
    
    prompt = f"""
    You are an AI assistant for {company_data['name']}, a {company_data['industry']} company.
    
    Company Context:
    {context['summary']}
    
    User Query: {query}
    
    Provide a comprehensive, contextually relevant response that:
    1. Uses specific knowledge about {company_data['name']}
    2. References relevant company processes and goals
    3. Provides actionable insights based on the company's context
    4. Maintains professional tone appropriate for {context_type} context
    
    Response:
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
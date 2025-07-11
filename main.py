#!/usr/bin/env python3
"""
Blueprint AI - Corporate Intelligence Platform
Root entry point for Railway deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os

# Import AI service
from ai_service import get_ai_service

# Create FastAPI app
app = FastAPI(
    title="Blueprint AI - Corporate Intelligence Platform",
    description="AI-powered corporate intelligence and content generation application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ContentGenerationRequest(BaseModel):
    prompt: str
    context: Optional[str] = ""

class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = ""

class SalesContentRequest(BaseModel):
    product_info: str
    target_audience: str

class DocumentAnalysisRequest(BaseModel):
    document_text: str
    analysis_type: str = "general"  # general, summary, key_points, sentiment

@app.get("/")
async def root():
    """Root endpoint with application information"""
    return {
        "message": "Blueprint AI - Corporate Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "blueprint-ai"}

@app.get("/api/v1/health")
async def api_health():
    """API health check endpoint"""
    return {"status": "healthy", "api": "v1"}

# AI Endpoints
@app.post("/api/v1/ai/generate-content")
async def generate_content(request: ContentGenerationRequest):
    """Generate content using Gemini AI"""
    try:
        ai_service = get_ai_service()
        result = await ai_service.generate_content(request.prompt, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.post("/api/v1/ai/answer-question")
async def answer_question(request: QuestionRequest):
    """Answer questions using Gemini AI"""
    try:
        ai_service = get_ai_service()
        result = await ai_service.answer_question(request.question, request.context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.post("/api/v1/ai/generate-sales-content")
async def generate_sales_content(request: SalesContentRequest):
    """Generate sales content using Gemini AI"""
    try:
        ai_service = get_ai_service()
        result = await ai_service.generate_sales_content(request.product_info, request.target_audience)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.post("/api/v1/ai/analyze-document")
async def analyze_document(request: DocumentAnalysisRequest):
    """Analyze document content using Gemini AI"""
    try:
        ai_service = get_ai_service()
        result = await ai_service.analyze_document(request.document_text, request.analysis_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.get("/api/v1/ai/models")
async def get_ai_models():
    """Get available AI models"""
    return {
        "models": [
            {
                "name": "gemini-pro",
                "provider": "Google",
                "capabilities": ["text-generation", "content-creation", "q&a", "document-analysis"]
            }
        ]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Blueprint AI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 
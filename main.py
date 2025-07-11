#!/usr/bin/env python3
"""
Blueprint AI - Corporate Intelligence Platform
Root entry point for Railway deployment
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Blueprint AI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 
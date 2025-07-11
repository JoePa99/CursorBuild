from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.models.base import BaseResponse
from app.services.context_engine import ContextEngine
from app.services.ai_service import AIService

router = APIRouter()

# Initialize services
context_engine = ContextEngine()
ai_service = AIService()

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    context_type: Optional[str] = "auto"  # "auto", "factual", "strategic", "creative"

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    context_used: dict
    confidence_score: float
    sources: List[dict]

@router.post("/", response_model=BaseResponse)
async def chat_with_ai(request: ChatRequest):
    """Chat with the AI assistant using corporate knowledge"""
    try:
        # Analyze query intent
        intent_analysis = await ai_service.analyze_query_intent(request.message)
        
        # Build context based on query and intent
        context = await context_engine.build_context(
            query=request.message,
            task_type=intent_analysis.get("query_type", "general")
        )
        
        # Determine system prompt based on intent
        system_prompt = _get_system_prompt_for_intent(intent_analysis)
        
        # Generate response
        response = await ai_service.generate_text(
            prompt=request.message,
            context=context,
            system_prompt=system_prompt
        )
        
        # Prepare response data
        response_data = {
            "response": response,
            "context_used": {
                "entities_count": len(context.entities),
                "relationships_count": len(context.relationships),
                "documents_count": len(context.documents),
                "chunks_count": len(context.semantic_chunks),
                "context_summary": context.context_summary
            },
            "confidence_score": intent_analysis.get("confidence", 0.5),
            "sources": [
                {
                    "type": "entity",
                    "name": entity.name,
                    "entity_type": entity.entity_type.value
                } for entity in context.entities[:3]
            ] + [
                {
                    "type": "document",
                    "document_id": chunk.get("document_id"),
                    "similarity_score": chunk.get("similarity_score")
                } for chunk in context.semantic_chunks[:3]
            ]
        }
        
        return BaseResponse(
            success=True,
            data=response_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.post("/stream", response_model=BaseResponse)
async def chat_stream(request: ChatRequest):
    """Stream chat response (for real-time chat interface)"""
    try:
        # This would implement streaming response
        # For now, return the same as regular chat
        return await chat_with_ai(request)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stream chat failed: {str(e)}")

@router.post("/factual", response_model=BaseResponse)
async def factual_query(request: ChatRequest):
    """Get factual answers from corporate knowledge"""
    try:
        # Build context focused on factual information
        context = await context_engine.build_context(
            query=request.message,
            task_type="factual",
            max_entities=5,
            max_chunks=3
        )
        
        system_prompt = """
        You are a factual corporate knowledge assistant. Provide accurate, 
        concise answers based on the available corporate information. 
        If you don't have enough information, say so clearly.
        """
        
        response = await ai_service.generate_text(
            prompt=request.message,
            context=context,
            system_prompt=system_prompt
        )
        
        return BaseResponse(
            success=True,
            data={
                "response": response,
                "query_type": "factual",
                "sources": [
                    {
                        "type": "document",
                        "document_id": chunk.get("document_id"),
                        "similarity_score": chunk.get("similarity_score")
                    } for chunk in context.semantic_chunks[:3]
                ]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Factual query failed: {str(e)}")

@router.post("/strategic", response_model=BaseResponse)
async def strategic_query(request: ChatRequest):
    """Get strategic insights and analysis"""
    try:
        # Build comprehensive context for strategic analysis
        context = await context_engine.get_context_for_strategic_analysis(request.message)
        
        system_prompt = """
        You are a strategic advisor with access to comprehensive corporate knowledge.
        Provide strategic insights, analysis, and recommendations based on the available information.
        Consider market context, competitive landscape, and business implications.
        """
        
        response = await ai_service.generate_text(
            prompt=request.message,
            context=context,
            system_prompt=system_prompt
        )
        
        return BaseResponse(
            success=True,
            data={
                "response": response,
                "query_type": "strategic",
                "analysis_depth": "comprehensive",
                "entities_analyzed": len(context.entities),
                "relationships_considered": len(context.relationships)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategic query failed: {str(e)}")

@router.get("/suggestions", response_model=BaseResponse)
async def get_chat_suggestions():
    """Get suggested questions for the chat interface"""
    try:
        suggestions = [
            {
                "category": "Company Information",
                "questions": [
                    "What is our company's mission and vision?",
                    "What are our core values?",
                    "Who are our key executives?",
                    "What markets do we operate in?"
                ]
            },
            {
                "category": "Strategic Analysis",
                "questions": [
                    "What are our main competitive advantages?",
                    "How do we compare to our competitors?",
                    "What are the key trends in our industry?",
                    "What strategic initiatives are we pursuing?"
                ]
            },
            {
                "category": "Operations",
                "questions": [
                    "What are our main products and services?",
                    "How do we handle customer support?",
                    "What is our sales process?",
                    "What are our key performance metrics?"
                ]
            }
        ]
        
        return BaseResponse(
            success=True,
            data={"suggestions": suggestions}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get suggestions: {str(e)}")

def _get_system_prompt_for_intent(intent_analysis: dict) -> str:
    """Get appropriate system prompt based on query intent"""
    query_type = intent_analysis.get("query_type", "factual")
    
    prompts = {
        "factual": """
        You are a factual corporate knowledge assistant. Provide accurate, 
        concise answers based on the available corporate information. 
        If you don't have enough information, say so clearly.
        """,
        "strategic": """
        You are a strategic advisor with access to comprehensive corporate knowledge.
        Provide strategic insights, analysis, and recommendations based on the available information.
        Consider market context, competitive landscape, and business implications.
        """,
        "creative": """
        You are a creative content assistant with deep knowledge of the company.
        Help generate creative ideas, content suggestions, and innovative approaches
        while staying true to the company's brand and values.
        """,
        "analytical": """
        You are an analytical expert with access to corporate data and knowledge.
        Provide data-driven insights, analysis, and recommendations.
        Use the available information to support your analysis with specific details.
        """
    }
    
    return prompts.get(query_type, prompts["factual"]) 
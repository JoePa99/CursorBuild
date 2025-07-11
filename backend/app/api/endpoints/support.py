from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel

from app.models.base import BaseResponse
from app.services.context_engine import ContextEngine
from app.services.ai_service import AIService

router = APIRouter()

# Initialize services
context_engine = ContextEngine()
ai_service = AIService()

class CustomerInquiry(BaseModel):
    """Customer inquiry model"""
    customer_name: str
    customer_email: Optional[str] = None
    company: Optional[str] = None
    inquiry_type: str  # "technical", "billing", "general", "feature_request"
    subject: str
    message: str
    priority: str = "medium"  # "low", "medium", "high", "urgent"
    category: Optional[str] = None

class SupportResponse(BaseModel):
    """Support response model"""
    response_content: str
    internal_notes: str
    suggested_actions: List[str]
    confidence_score: float

@router.post("/analyze", response_model=BaseResponse)
async def analyze_inquiry(inquiry: CustomerInquiry):
    """Analyze customer inquiry and provide insights"""
    try:
        # Build context for the inquiry
        context = await context_engine.build_context(
            query=f"{inquiry.subject} {inquiry.message} {inquiry.inquiry_type}",
            task_type="customer_support"
        )
        
        # Analyze the inquiry
        analysis_prompt = f"""
        Analyze this customer inquiry and provide insights:
        
        Customer: {inquiry.customer_name}
        Company: {inquiry.company}
        Type: {inquiry.inquiry_type}
        Subject: {inquiry.subject}
        Message: {inquiry.message}
        Priority: {inquiry.priority}
        
        Provide:
        - Inquiry classification
        - Sentiment analysis
        - Key issues identified
        - Recommended response approach
        - Escalation needs
        """
        
        analysis = await ai_service.generate_text(
            prompt=analysis_prompt,
            context=context,
            system_prompt="You are an expert customer support analyst."
        )
        
        return BaseResponse(
            success=True,
            data={
                "inquiry": inquiry.dict(),
                "analysis": analysis,
                "context_used": {
                    "entities_count": len(context.entities),
                    "documents_count": len(context.documents)
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inquiry analysis failed: {str(e)}")

@router.post("/respond", response_model=BaseResponse)
async def generate_response(inquiry: CustomerInquiry):
    """Generate customer support response"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"{inquiry.subject} {inquiry.message}",
            task_type="customer_response"
        )
        
        # Generate response
        response_prompt = f"""
        Generate a professional customer support response for:
        
        Customer: {inquiry.customer_name}
        Company: {inquiry.company}
        Inquiry Type: {inquiry.inquiry_type}
        Subject: {inquiry.subject}
        Message: {inquiry.message}
        Priority: {inquiry.priority}
        
        Create a helpful, professional response that:
        - Addresses the customer's concerns
        - Provides clear next steps
        - Maintains brand voice
        - Shows empathy and understanding
        """
        
        response_content = await ai_service.generate_text(
            prompt=response_prompt,
            context=context,
            system_prompt="You are an expert customer support representative."
        )
        
        # Generate internal notes
        internal_prompt = f"""
        Create internal notes for this customer inquiry:
        
        {inquiry.message}
        
        Include:
        - Key action items
        - Follow-up requirements
        - Escalation recommendations
        - Knowledge base updates needed
        """
        
        internal_notes = await ai_service.generate_text(
            prompt=internal_prompt,
            context=context,
            system_prompt="You are a customer support manager creating internal notes."
        )
        
        return BaseResponse(
            success=True,
            data={
                "customer_response": response_content,
                "internal_notes": internal_notes,
                "inquiry": inquiry.dict(),
                "suggested_actions": [
                    "Follow up within 24 hours",
                    "Update knowledge base",
                    "Escalate if needed"
                ]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response generation failed: {str(e)}")

@router.post("/escalate", response_model=BaseResponse)
async def escalate_inquiry(inquiry: CustomerInquiry, escalation_reason: str):
    """Escalate customer inquiry with AI-generated summary"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"{inquiry.subject} {inquiry.message} escalation",
            task_type="escalation"
        )
        
        # Generate escalation summary
        escalation_prompt = f"""
        Create an escalation summary for this customer inquiry:
        
        Customer: {inquiry.customer_name}
        Company: {inquiry.company}
        Inquiry: {inquiry.message}
        Escalation Reason: {escalation_reason}
        
        Provide:
        - Brief summary of the issue
        - What has been tried so far
        - Why escalation is needed
        - Recommended next steps
        - Priority level
        """
        
        escalation_summary = await ai_service.generate_text(
            prompt=escalation_prompt,
            context=context,
            system_prompt="You are a customer support manager creating escalation summaries."
        )
        
        return BaseResponse(
            success=True,
            data={
                "escalation_summary": escalation_summary,
                "inquiry": inquiry.dict(),
                "escalation_reason": escalation_reason,
                "priority": inquiry.priority
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Escalation failed: {str(e)}")

@router.post("/knowledge-base", response_model=BaseResponse)
async def generate_knowledge_base_entry(inquiry: CustomerInquiry):
    """Generate knowledge base entry from customer inquiry"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"{inquiry.subject} {inquiry.message} knowledge base",
            task_type="knowledge_base"
        )
        
        # Generate knowledge base entry
        kb_prompt = f"""
        Create a knowledge base entry based on this customer inquiry:
        
        Subject: {inquiry.subject}
        Message: {inquiry.message}
        Type: {inquiry.inquiry_type}
        
        Create:
        - Clear title
        - Problem description
        - Step-by-step solution
        - Related articles
        - Tags for categorization
        """
        
        kb_entry = await ai_service.generate_text(
            prompt=kb_prompt,
            context=context,
            system_prompt="You are a technical writer creating knowledge base articles."
        )
        
        return BaseResponse(
            success=True,
            data={
                "knowledge_base_entry": kb_entry,
                "inquiry": inquiry.dict(),
                "tags": [inquiry.inquiry_type, inquiry.category] if inquiry.category else [inquiry.inquiry_type]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge base generation failed: {str(e)}")

@router.get("/templates", response_model=BaseResponse)
async def get_response_templates():
    """Get common response templates"""
    try:
        templates = {
            "technical_support": {
                "title": "Technical Issue Resolution",
                "template": "Thank you for reaching out about [issue]. We understand this can be frustrating. Here's how we can help...",
                "variables": ["issue", "customer_name", "next_steps"]
            },
            "billing_inquiry": {
                "title": "Billing Question Response",
                "template": "Thank you for your inquiry about your billing. Let me clarify the charges on your account...",
                "variables": ["customer_name", "account_number", "billing_period"]
            },
            "feature_request": {
                "title": "Feature Request Acknowledgment",
                "template": "Thank you for your feature request for [feature]. We appreciate your input and will consider it for future updates...",
                "variables": ["feature", "customer_name", "timeline"]
            },
            "general_inquiry": {
                "title": "General Information Response",
                "template": "Thank you for contacting us. I'd be happy to help you with [topic]...",
                "variables": ["topic", "customer_name", "additional_info"]
            }
        }
        
        return BaseResponse(
            success=True,
            data={"templates": templates}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get templates: {str(e)}")

@router.post("/sentiment", response_model=BaseResponse)
async def analyze_sentiment(message: str):
    """Analyze customer message sentiment"""
    try:
        sentiment_prompt = f"""
        Analyze the sentiment of this customer message:
        
        "{message}"
        
        Provide:
        - Sentiment (positive, negative, neutral)
        - Sentiment score (1-10)
        - Key emotions detected
        - Urgency level
        - Recommended tone for response
        """
        
        sentiment_analysis = await ai_service.generate_text(
            prompt=sentiment_prompt,
            system_prompt="You are an expert in sentiment analysis and customer communication."
        )
        
        return BaseResponse(
            success=True,
            data={
                "message": message,
                "sentiment_analysis": sentiment_analysis
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}") 
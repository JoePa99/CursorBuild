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

class LeadData(BaseModel):
    """Lead data model"""
    name: str
    company: str
    title: str
    email: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    pain_points: Optional[List[str]] = []
    interests: Optional[List[str]] = []

class OutreachRequest(BaseModel):
    """Outreach generation request"""
    lead: LeadData
    outreach_type: str  # "email", "linkedin", "call_script"
    campaign_type: str  # "cold_outreach", "follow_up", "nurture"
    personalization_level: str = "high"  # "low", "medium", "high"
    key_message: Optional[str] = None

class OutreachSequence(BaseModel):
    """Outreach sequence model"""
    sequence_name: str
    steps: List[dict]
    total_duration_days: int

@router.post("/outreach", response_model=BaseResponse)
async def generate_outreach(request: OutreachRequest):
    """Generate personalized outreach content"""
    try:
        # Build context for the lead
        context = await context_engine.build_context(
            query=f"{request.lead.company} {request.lead.industry} {request.lead.title}",
            task_type="sales_outreach"
        )
        
        # Generate outreach content
        outreach_prompt = _build_outreach_prompt(request)
        
        content = await ai_service.generate_text(
            prompt=outreach_prompt,
            context=context,
            system_prompt=_get_sales_system_prompt(request)
        )
        
        return BaseResponse(
            success=True,
            data={
                "outreach_content": content,
                "lead": request.lead.dict(),
                "outreach_type": request.outreach_type,
                "campaign_type": request.campaign_type,
                "personalization_level": request.personalization_level
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outreach generation failed: {str(e)}")

@router.post("/sequence", response_model=BaseResponse)
async def generate_outreach_sequence(request: OutreachRequest):
    """Generate a complete outreach sequence"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"{request.lead.company} {request.lead.industry}",
            task_type="sales_sequence"
        )
        
        # Generate sequence
        sequence_prompt = f"""
        Create a complete outreach sequence for {request.lead.name} at {request.lead.company}.
        
        Lead details:
        - Name: {request.lead.name}
        - Company: {request.lead.company}
        - Title: {request.lead.title}
        - Industry: {request.lead.industry}
        - Company size: {request.lead.company_size}
        - Pain points: {', '.join(request.lead.pain_points) if request.lead.pain_points else 'Not specified'}
        
        Campaign type: {request.campaign_type}
        Personalization level: {request.personalization_level}
        
        Create a 5-7 step sequence with:
        - Email subject lines
        - Email content
        - Follow-up timing
        - Call-to-action recommendations
        """
        
        sequence_content = await ai_service.generate_text(
            prompt=sequence_prompt,
            context=context,
            system_prompt="You are an expert sales strategist and outreach specialist."
        )
        
        return BaseResponse(
            success=True,
            data={
                "sequence_content": sequence_content,
                "lead": request.lead.dict(),
                "campaign_type": request.campaign_type
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sequence generation failed: {str(e)}")

@router.post("/enrich", response_model=BaseResponse)
async def enrich_lead_data(lead: LeadData):
    """Enrich lead data with additional information"""
    try:
        # This would typically integrate with external APIs (LinkedIn, ZoomInfo, etc.)
        # For now, return mock enriched data
        
        enriched_data = {
            "original_lead": lead.dict(),
            "enriched_data": {
                "company_revenue": "$10M - $50M",
                "employee_count": "50-200",
                "funding_stage": "Series B",
                "technologies_used": ["Salesforce", "HubSpot", "Slack"],
                "recent_news": "Company recently expanded to new markets",
                "decision_makers": ["CEO", "CTO", "VP Sales"],
                "pain_points": ["Scaling operations", "Customer retention", "Market expansion"],
                "opportunity_size": "High"
            }
        }
        
        return BaseResponse(
            success=True,
            data=enriched_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead enrichment failed: {str(e)}")

@router.post("/qualify", response_model=BaseResponse)
async def qualify_lead(lead: LeadData):
    """Qualify a lead using AI analysis"""
    try:
        # Build context for qualification
        context = await context_engine.build_context(
            query=f"{lead.company} {lead.industry} {lead.title} qualification",
            task_type="lead_qualification"
        )
        
        qualification_prompt = f"""
        Qualify this lead based on the available information:
        
        Lead: {lead.name}
        Company: {lead.company}
        Title: {lead.title}
        Industry: {lead.industry}
        Company size: {lead.company_size}
        Pain points: {', '.join(lead.pain_points) if lead.pain_points else 'Not specified'}
        
        Provide:
        - Qualification score (1-10)
        - BANT assessment (Budget, Authority, Need, Timeline)
        - Recommended next steps
        - Priority level (High/Medium/Low)
        """
        
        qualification = await ai_service.generate_text(
            prompt=qualification_prompt,
            context=context,
            system_prompt="You are an expert sales qualification specialist."
        )
        
        return BaseResponse(
            success=True,
            data={
                "lead": lead.dict(),
                "qualification_analysis": qualification
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead qualification failed: {str(e)}")

def _build_outreach_prompt(request: OutreachRequest) -> str:
    """Build outreach generation prompt"""
    prompt = f"""
    Create a personalized {request.outreach_type} outreach for:
    
    Lead: {request.lead.name}
    Company: {request.lead.company}
    Title: {request.lead.title}
    Industry: {request.lead.industry}
    Company size: {request.lead.company_size}
    
    Campaign type: {request.campaign_type}
    Personalization level: {request.personalization_level}
    """
    
    if request.lead.pain_points:
        prompt += f"\nPain points: {', '.join(request.lead.pain_points)}"
    
    if request.key_message:
        prompt += f"\nKey message to include: {request.key_message}"
    
    prompt += f"\n\nCreate compelling, personalized content that resonates with this specific lead."
    
    return prompt

def _get_sales_system_prompt(request: OutreachRequest) -> str:
    """Get system prompt for sales outreach"""
    return f"""
    You are an expert sales professional specializing in {request.outreach_type} outreach.
    Create personalized, compelling content that:
    - Addresses the specific needs and pain points of the lead
    - Demonstrates understanding of their industry and role
    - Provides clear value proposition
    - Includes appropriate call-to-action
    - Maintains professional tone while being engaging
    - Uses {request.personalization_level} personalization level
    """ 
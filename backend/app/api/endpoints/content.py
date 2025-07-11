from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel

from app.models.base import BaseResponse
from app.services.context_engine import ContextEngine
from app.services.ai_service import AIService

router = APIRouter()

# Initialize services
context_engine = ContextEngine()
ai_service = AIService()

class ContentRequest(BaseModel):
    """Content generation request"""
    content_type: str  # "blog", "whitepaper", "letter", "report"
    topic: str
    target_audience: Optional[str] = None
    tone: Optional[str] = "professional"  # "professional", "casual", "formal"
    length: Optional[str] = "medium"  # "short", "medium", "long"
    key_points: Optional[list] = []
    brand_guidelines: Optional[str] = None

class ContentResponse(BaseModel):
    """Content generation response"""
    content: str
    title: str
    summary: str
    key_points: list
    word_count: int

@router.post("/generate", response_model=BaseResponse)
async def generate_content(request: ContentRequest):
    """Generate long-form content"""
    try:
        # Get context for content generation
        context = await context_engine.get_context_for_content_generation(
            content_type=request.content_type,
            topic=request.topic,
            target_audience=request.target_audience
        )
        
        # Build content generation prompt
        prompt = _build_content_prompt(request)
        
        # Generate content
        content = await ai_service.generate_text(
            prompt=prompt,
            context=context,
            system_prompt=_get_content_system_prompt(request)
        )
        
        # Extract title and summary
        title = await _extract_title(content, request.topic)
        summary = await _extract_summary(content)
        key_points = await _extract_key_points(content)
        
        return BaseResponse(
            success=True,
            data={
                "content": content,
                "title": title,
                "summary": summary,
                "key_points": key_points,
                "word_count": len(content.split()),
                "content_type": request.content_type,
                "topic": request.topic
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@router.post("/outline", response_model=BaseResponse)
async def generate_outline(request: ContentRequest):
    """Generate content outline"""
    try:
        context = await context_engine.get_context_for_content_generation(
            content_type=request.content_type,
            topic=request.topic,
            target_audience=request.target_audience
        )
        
        outline_prompt = f"""
        Create a detailed outline for a {request.content_type} about {request.topic}.
        Target audience: {request.target_audience or 'General business audience'}
        Tone: {request.tone}
        Length: {request.length}
        
        Include:
        - Main sections and subsections
        - Key points for each section
        - Suggested word count distribution
        - Call-to-action recommendations
        """
        
        outline = await ai_service.generate_text(
            prompt=outline_prompt,
            context=context,
            system_prompt="You are an expert content strategist and outline creator."
        )
        
        return BaseResponse(
            success=True,
            data={
                "outline": outline,
                "content_type": request.content_type,
                "topic": request.topic
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outline generation failed: {str(e)}")

@router.post("/improve", response_model=BaseResponse)
async def improve_content(content: str, improvement_type: str = "general"):
    """Improve existing content"""
    try:
        improvement_prompts = {
            "general": "Improve this content for clarity, flow, and impact while maintaining the original message.",
            "tone": "Adjust the tone to be more professional and engaging while keeping the same content.",
            "structure": "Improve the structure and organization of this content for better readability.",
            "seo": "Optimize this content for search engines while maintaining readability and value."
        }
        
        prompt = f"{improvement_prompts.get(improvement_type, improvement_prompts['general'])}\n\nContent:\n{content}"
        
        improved_content = await ai_service.generate_text(
            prompt=prompt,
            system_prompt="You are an expert content editor and copywriter."
        )
        
        return BaseResponse(
            success=True,
            data={
                "original_content": content,
                "improved_content": improved_content,
                "improvement_type": improvement_type
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content improvement failed: {str(e)}")

def _build_content_prompt(request: ContentRequest) -> str:
    """Build content generation prompt"""
    prompt = f"""
    Create a {request.content_type} about {request.topic}.
    
    Requirements:
    - Content type: {request.content_type}
    - Target audience: {request.target_audience or 'General business audience'}
    - Tone: {request.tone}
    - Length: {request.length}
    """
    
    if request.key_points:
        prompt += f"\nKey points to include:\n"
        for point in request.key_points:
            prompt += f"- {point}\n"
    
    if request.brand_guidelines:
        prompt += f"\nBrand guidelines: {request.brand_guidelines}"
    
    prompt += f"\n\nPlease create comprehensive, engaging content that provides value to the target audience."
    
    return prompt

def _get_content_system_prompt(request: ContentRequest) -> str:
    """Get system prompt for content generation"""
    return f"""
    You are an expert content creator specializing in {request.content_type} content.
    Create high-quality, engaging content that:
    - Provides clear value to the target audience
    - Maintains a {request.tone} tone throughout
    - Uses appropriate length for {request.length} content
    - Includes relevant examples and insights
    - Follows best practices for {request.content_type} writing
    - Incorporates the company's knowledge and expertise
    """

async def _extract_title(content: str, topic: str) -> str:
    """Extract or generate title from content"""
    title_prompt = f"Generate a compelling title for this content about {topic}:\n\n{content[:500]}..."
    
    title = await ai_service.generate_text(
        prompt=title_prompt,
        system_prompt="You are an expert at creating compelling, SEO-friendly titles."
    )
    
    return title.strip()

async def _extract_summary(content: str) -> str:
    """Extract summary from content"""
    summary_prompt = f"Create a concise 2-3 sentence summary of this content:\n\n{content}"
    
    summary = await ai_service.generate_text(
        prompt=summary_prompt,
        system_prompt="You are an expert at creating concise, informative summaries."
    )
    
    return summary.strip()

async def _extract_key_points(content: str) -> list:
    """Extract key points from content"""
    points_prompt = f"Extract 3-5 key points from this content:\n\n{content}"
    
    points_text = await ai_service.generate_text(
        prompt=points_prompt,
        system_prompt="You are an expert at identifying and extracting key points from content."
    )
    
    # Simple parsing - in practice you might want more sophisticated parsing
    points = [point.strip() for point in points_text.split('\n') if point.strip() and not point.strip().startswith('#')]
    return points[:5]  # Limit to 5 points 
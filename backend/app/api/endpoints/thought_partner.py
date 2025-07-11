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

class StrategicQuestion(BaseModel):
    """Strategic question model"""
    question: str
    context: Optional[str] = None
    timeframe: Optional[str] = None  # "short_term", "medium_term", "long_term"
    focus_areas: Optional[List[str]] = []  # "market", "competition", "operations", "finance", "technology"

class ScenarioAnalysis(BaseModel):
    """Scenario analysis model"""
    scenario_name: str
    description: str
    assumptions: List[str]
    variables: List[str]
    timeframe: str

class StrategicAnalysis(BaseModel):
    """Strategic analysis model"""
    analysis_type: str  # "swot", "pestle", "competitive", "market", "risk"
    focus_area: str
    depth: str = "comprehensive"  # "basic", "detailed", "comprehensive"

@router.post("/analyze", response_model=BaseResponse)
async def analyze_strategic_question(request: StrategicQuestion):
    """Analyze strategic questions using comprehensive knowledge context"""
    try:
        # Build comprehensive context for strategic analysis
        context = await context_engine.get_context_for_strategic_analysis(request.question)
        
        # Generate strategic analysis
        analysis_prompt = f"""
        Provide a comprehensive strategic analysis for this question:
        
        Question: {request.question}
        Context: {request.context or 'No additional context provided'}
        Timeframe: {request.timeframe or 'Not specified'}
        Focus Areas: {', '.join(request.focus_areas) if request.focus_areas else 'All areas'}
        
        Provide:
        - Executive summary
        - Key insights and findings
        - Strategic implications
        - Recommendations
        - Risk considerations
        - Success metrics
        """
        
        analysis = await ai_service.generate_text(
            prompt=analysis_prompt,
            context=context,
            system_prompt="You are a senior strategic advisor with expertise in business strategy and corporate intelligence."
        )
        
        return BaseResponse(
            success=True,
            data={
                "question": request.question,
                "analysis": analysis,
                "context_used": {
                    "entities_analyzed": len(context.entities),
                    "relationships_considered": len(context.relationships),
                    "documents_referenced": len(context.documents),
                    "context_summary": context.context_summary
                },
                "analysis_metadata": {
                    "timeframe": request.timeframe,
                    "focus_areas": request.focus_areas,
                    "analysis_depth": "comprehensive"
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategic analysis failed: {str(e)}")

@router.post("/scenarios", response_model=BaseResponse)
async def generate_scenarios(request: ScenarioAnalysis):
    """Generate strategic scenarios and analysis"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"{request.scenario_name} {request.description}",
            task_type="scenario_analysis"
        )
        
        # Generate scenarios
        scenario_prompt = f"""
        Create strategic scenarios for: {request.scenario_name}
        
        Description: {request.description}
        Assumptions: {', '.join(request.assumptions)}
        Key Variables: {', '.join(request.variables)}
        Timeframe: {request.timeframe}
        
        Create:
        - Best case scenario
        - Worst case scenario
        - Most likely scenario
        - Probability assessments
        - Strategic implications for each scenario
        - Contingency plans
        """
        
        scenarios = await ai_service.generate_text(
            prompt=scenario_prompt,
            context=context,
            system_prompt="You are an expert strategic planner and scenario analyst."
        )
        
        return BaseResponse(
            success=True,
            data={
                "scenario_name": request.scenario_name,
                "scenarios_analysis": scenarios,
                "assumptions": request.assumptions,
                "variables": request.variables,
                "timeframe": request.timeframe
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scenario generation failed: {str(e)}")

@router.post("/swot", response_model=BaseResponse)
async def perform_swot_analysis(focus_area: str = "company"):
    """Perform SWOT analysis"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"SWOT analysis {focus_area}",
            task_type="swot_analysis"
        )
        
        # Generate SWOT analysis
        swot_prompt = f"""
        Perform a comprehensive SWOT analysis for {focus_area}:
        
        Strengths:
        - Internal positive factors
        - Competitive advantages
        - Core competencies
        
        Weaknesses:
        - Internal negative factors
        - Areas for improvement
        - Resource limitations
        
        Opportunities:
        - External positive factors
        - Market opportunities
        - Growth potential
        
        Threats:
        - External negative factors
        - Competitive threats
        - Market risks
        """
        
        swot_analysis = await ai_service.generate_text(
            prompt=swot_prompt,
            context=context,
            system_prompt="You are an expert strategic analyst specializing in SWOT analysis."
        )
        
        return BaseResponse(
            success=True,
            data={
                "focus_area": focus_area,
                "swot_analysis": swot_analysis,
                "context_used": {
                    "entities_count": len(context.entities),
                    "relationships_count": len(context.relationships)
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SWOT analysis failed: {str(e)}")

@router.post("/competitive", response_model=BaseResponse)
async def competitive_analysis(competitor_name: Optional[str] = None):
    """Perform competitive analysis"""
    try:
        # Build context
        query = f"competitive analysis {competitor_name}" if competitor_name else "competitive landscape"
        context = await context_engine.build_context(
            query=query,
            task_type="competitive_analysis"
        )
        
        # Generate competitive analysis
        competitive_prompt = f"""
        Perform a competitive analysis{f" for {competitor_name}" if competitor_name else ""}:
        
        Include:
        - Market positioning
        - Competitive advantages
        - Product/service comparison
        - Pricing strategies
        - Market share analysis
        - Strategic recommendations
        """
        
        competitive_analysis = await ai_service.generate_text(
            prompt=competitive_prompt,
            context=context,
            system_prompt="You are an expert competitive intelligence analyst."
        )
        
        return BaseResponse(
            success=True,
            data={
                "competitor": competitor_name or "General competitive landscape",
                "competitive_analysis": competitive_analysis,
                "analysis_type": "comprehensive"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitive analysis failed: {str(e)}")

@router.post("/market", response_model=BaseResponse)
async def market_analysis(market_segment: str):
    """Perform market analysis"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"market analysis {market_segment}",
            task_type="market_analysis"
        )
        
        # Generate market analysis
        market_prompt = f"""
        Perform a comprehensive market analysis for {market_segment}:
        
        Include:
        - Market size and growth
        - Key trends and drivers
        - Customer segments
        - Market opportunities
        - Entry barriers
        - Regulatory environment
        - Strategic recommendations
        """
        
        market_analysis = await ai_service.generate_text(
            prompt=market_prompt,
            context=context,
            system_prompt="You are an expert market analyst and business strategist."
        )
        
        return BaseResponse(
            success=True,
            data={
                "market_segment": market_segment,
                "market_analysis": market_analysis,
                "analysis_depth": "comprehensive"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market analysis failed: {str(e)}")

@router.post("/risk", response_model=BaseResponse)
async def risk_assessment(risk_area: str = "general"):
    """Perform risk assessment"""
    try:
        # Build context
        context = await context_engine.build_context(
            query=f"risk assessment {risk_area}",
            task_type="risk_assessment"
        )
        
        # Generate risk assessment
        risk_prompt = f"""
        Perform a comprehensive risk assessment for {risk_area}:
        
        Include:
        - Risk identification
        - Risk categorization (strategic, operational, financial, compliance)
        - Risk probability and impact assessment
        - Risk mitigation strategies
        - Contingency plans
        - Risk monitoring recommendations
        """
        
        risk_assessment = await ai_service.generate_text(
            prompt=risk_prompt,
            context=context,
            system_prompt="You are an expert risk management specialist."
        )
        
        return BaseResponse(
            success=True,
            data={
                "risk_area": risk_area,
                "risk_assessment": risk_assessment,
                "assessment_type": "comprehensive"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")

@router.get("/insights", response_model=BaseResponse)
async def get_strategic_insights():
    """Get strategic insights and recommendations"""
    try:
        # This would typically analyze recent data and provide insights
        # For now, return mock insights
        
        insights = {
            "market_trends": [
                "Increasing focus on sustainability and ESG",
                "Digital transformation acceleration",
                "Remote work adoption continuing"
            ],
            "competitive_moves": [
                "Key competitor expanding into new markets",
                "Technology partnerships on the rise",
                "M&A activity increasing in the sector"
            ],
            "opportunities": [
                "Untapped market segments identified",
                "Technology integration opportunities",
                "Strategic partnership potential"
            ],
            "risks": [
                "Regulatory changes on the horizon",
                "Supply chain disruptions continuing",
                "Talent retention challenges"
            ]
        }
        
        return BaseResponse(
            success=True,
            data={"strategic_insights": insights}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}") 
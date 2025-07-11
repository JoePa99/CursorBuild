import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
import json

from app.models.knowledge import KnowledgeContext, Entity, Relationship
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI service using Google Gemini for text generation and analysis"""
    
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        
        logger.info("AI service initialized with Gemini")
    
    async def generate_text(self, prompt: str, context: Optional[KnowledgeContext] = None, 
                          system_prompt: Optional[str] = None) -> str:
        """Generate text using Gemini with optional context"""
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt(prompt, context, system_prompt)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                logger.info("Text generation completed successfully")
                return response.text
            else:
                logger.warning("Empty response from Gemini")
                return "I couldn't generate a response for that request."
                
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    async def extract_entities_and_relationships(self, text: str) -> Dict[str, Any]:
        """Extract entities and relationships from text using LLM"""
        try:
            extraction_prompt = f"""
            Analyze the following text and extract entities and relationships. 
            Return the result as a JSON object with the following structure:
            {{
                "entities": [
                    {{
                        "name": "entity name",
                        "entity_type": "company|person|product|service|location|industry|technology|concept|event|organization",
                        "description": "brief description",
                        "attributes": {{"key": "value"}},
                        "confidence_score": 0.0-1.0
                    }}
                ],
                "relationships": [
                    {{
                        "source_entity": "source entity name",
                        "target_entity": "target entity name", 
                        "relationship_type": "competes_with|partners_with|acquires|invests_in|employs|founded|located_in|operates_in|provides|uses|similar_to|parent_of|subsidiary_of",
                        "properties": {{"key": "value"}},
                        "confidence_score": 0.0-1.0
                    }}
                ]
            }}
            
            Text to analyze:
            {text}
            """
            
            response = self.model.generate_content(extraction_prompt)
            
            if response.text:
                # Try to parse JSON response
                try:
                    result = json.loads(response.text)
                    logger.info(f"Extracted {len(result.get('entities', []))} entities and {len(result.get('relationships', []))} relationships")
                    return result
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response from entity extraction")
                    return {"entities": [], "relationships": []}
            else:
                return {"entities": [], "relationships": []}
                
        except Exception as e:
            logger.error(f"Error extracting entities and relationships: {str(e)}")
            return {"entities": [], "relationships": []}
    
    async def generate_image_prompt(self, content_request: str, context: Optional[KnowledgeContext] = None) -> str:
        """Generate an image prompt based on content request and context"""
        try:
            image_prompt_template = f"""
            You are an expert at creating detailed, descriptive prompts for AI image generation.
            
            Context about the brand and company:
            {self._format_context_for_image(context) if context else "No specific context provided"}
            
            Content request: {content_request}
            
            Create a detailed, descriptive prompt for generating an image that matches this request.
            The prompt should be:
            - Specific and detailed
            - Professional and on-brand
            - Suitable for business/ corporate use
            - Include style, composition, and mood details
            
            Return only the image prompt, no additional text.
            """
            
            response = self.model.generate_content(image_prompt_template)
            
            if response.text:
                logger.info("Image prompt generated successfully")
                return response.text.strip()
            else:
                return "Professional business meeting in modern office"
                
        except Exception as e:
            logger.error(f"Error generating image prompt: {str(e)}")
            return "Professional business meeting in modern office"
    
    async def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user query to determine intent and required context"""
        try:
            intent_prompt = f"""
            Analyze the following query and determine:
            1. Query type (factual, strategic, creative, analytical)
            2. Required context types (entities, relationships, documents)
            3. Complexity level (simple, moderate, complex)
            4. Suggested response approach
            
            Query: {query}
            
            Return as JSON:
            {{
                "query_type": "factual|strategic|creative|analytical",
                "required_context": ["entities", "relationships", "documents"],
                "complexity": "simple|moderate|complex",
                "response_approach": "direct_answer|contextual_analysis|creative_generation",
                "confidence": 0.0-1.0
            }}
            """
            
            response = self.model.generate_content(intent_prompt)
            
            if response.text:
                try:
                    result = json.loads(response.text)
                    logger.info(f"Query intent analyzed: {result.get('query_type')}")
                    return result
                except json.JSONDecodeError:
                    logger.warning("Failed to parse JSON response from intent analysis")
                    return self._default_intent_analysis()
            else:
                return self._default_intent_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing query intent: {str(e)}")
            return self._default_intent_analysis()
    
    def _build_prompt(self, prompt: str, context: Optional[KnowledgeContext] = None, 
                     system_prompt: Optional[str] = None) -> str:
        """Build the full prompt with context and system instructions"""
        full_prompt = ""
        
        # Add system prompt if provided
        if system_prompt:
            full_prompt += f"System Instructions: {system_prompt}\n\n"
        
        # Add context if provided
        if context:
            context_section = self._format_context(context)
            full_prompt += f"Context Information:\n{context_section}\n\n"
        
        # Add user prompt
        full_prompt += f"User Request: {prompt}\n\n"
        full_prompt += "Please provide a comprehensive response based on the context and request."
        
        return full_prompt
    
    def _format_context(self, context: KnowledgeContext) -> str:
        """Format knowledge context for prompt inclusion"""
        context_parts = []
        
        # Add entities
        if context.entities:
            entity_info = "Relevant Entities:\n"
            for entity in context.entities:
                entity_info += f"- {entity.name} ({entity.entity_type.value}): {entity.description or 'No description'}\n"
            context_parts.append(entity_info)
        
        # Add relationships
        if context.relationships:
            rel_info = "Relevant Relationships:\n"
            for rel in context.relationships:
                rel_info += f"- {rel.source_entity_id} {rel.relationship_type.value} {rel.target_entity_id}\n"
            context_parts.append(rel_info)
        
        # Add semantic chunks
        if context.semantic_chunks:
            chunk_info = "Relevant Information:\n"
            for chunk in context.semantic_chunks[:3]:  # Limit to top 3 chunks
                chunk_info += f"- {chunk.get('content', '')[:200]}...\n"
            context_parts.append(chunk_info)
        
        # Add context summary
        if context.context_summary:
            context_parts.append(f"Context Summary: {context.context_summary}")
        
        return "\n".join(context_parts)
    
    def _format_context_for_image(self, context: KnowledgeContext) -> str:
        """Format context specifically for image generation"""
        if not context:
            return "Professional business environment"
        
        # Extract brand-relevant information
        brand_info = []
        
        for entity in context.entities:
            if entity.entity_type.value in ['company', 'organization']:
                brand_info.append(f"Company: {entity.name}")
                if entity.description:
                    brand_info.append(f"Description: {entity.description}")
        
        return "; ".join(brand_info) if brand_info else "Professional business environment"
    
    def _default_intent_analysis(self) -> Dict[str, Any]:
        """Default intent analysis when parsing fails"""
        return {
            "query_type": "factual",
            "required_context": ["entities", "documents"],
            "complexity": "simple",
            "response_approach": "direct_answer",
            "confidence": 0.5
        } 
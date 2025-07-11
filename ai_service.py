import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """AI Service for Google Gemini integration"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Configure Google Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def generate_content(self, prompt: str, context: str = "") -> Dict[str, Any]:
        """Generate content using Gemini AI"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            response = self.model.generate_content(full_prompt)
            
            return {
                "success": True,
                "content": response.text,
                "prompt": prompt,
                "model": "gemini-pro"
            }
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt
            }
    
    async def answer_question(self, question: str, context: str = "") -> Dict[str, Any]:
        """Answer questions using Gemini AI"""
        try:
            prompt = f"Please answer the following question based on the provided context:\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
            
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "answer": response.text,
                "question": question,
                "context": context,
                "model": "gemini-pro"
            }
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
    
    async def generate_sales_content(self, product_info: str, target_audience: str) -> Dict[str, Any]:
        """Generate sales content using Gemini AI"""
        try:
            prompt = f"""
            Create compelling sales content for the following product/service:
            
            Product/Service: {product_info}
            Target Audience: {target_audience}
            
            Please include:
            1. A compelling headline
            2. Key benefits and features
            3. A call-to-action
            4. Social proof suggestions
            
            Make it engaging and persuasive.
            """
            
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "content": response.text,
                "product_info": product_info,
                "target_audience": target_audience,
                "model": "gemini-pro"
            }
        except Exception as e:
            logger.error(f"Error generating sales content: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "product_info": product_info
            }
    
    async def analyze_document(self, document_text: str, analysis_type: str = "general") -> Dict[str, Any]:
        """Analyze document content using Gemini AI"""
        try:
            if analysis_type == "summary":
                prompt = f"Please provide a comprehensive summary of the following document:\n\n{document_text}"
            elif analysis_type == "key_points":
                prompt = f"Please extract the key points and insights from the following document:\n\n{document_text}"
            elif analysis_type == "sentiment":
                prompt = f"Please analyze the sentiment and tone of the following document:\n\n{document_text}"
            else:
                prompt = f"Please provide a general analysis of the following document:\n\n{document_text}"
            
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "analysis": response.text,
                "analysis_type": analysis_type,
                "document_length": len(document_text),
                "model": "gemini-pro"
            }
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }

# Global AI service instance
ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service 
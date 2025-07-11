from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from app.models.knowledge import KnowledgeContext, Entity, Relationship
from app.services.knowledge_graph import KnowledgeGraph
from app.services.vector_store import VectorStore
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

class ContextEngine:
    """Context engineering service for assembling relevant knowledge context"""
    
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph()
        self.vector_store = VectorStore()
        self.ai_service = AIService()
        
        logger.info("Context engine initialized")
    
    async def build_context(self, query: str, task_type: str = "general", 
                          max_entities: int = 10, max_chunks: int = 5) -> KnowledgeContext:
        """Build comprehensive context for a given query and task"""
        try:
            logger.info(f"Building context for query: {query}")
            
            # Analyze query intent
            intent_analysis = await self.ai_service.analyze_query_intent(query)
            
            # Initialize context
            context = KnowledgeContext()
            
            # Get relevant entities from knowledge graph
            entities = await self._get_relevant_entities(query, intent_analysis, max_entities)
            context.entities = entities
            
            # Get relevant relationships
            relationships = await self._get_relevant_relationships(entities, intent_analysis)
            context.relationships = relationships
            
            # Get relevant document chunks
            semantic_chunks = await self._get_relevant_chunks(query, intent_analysis, max_chunks)
            context.semantic_chunks = semantic_chunks
            
            # Get source document IDs
            document_ids = self._extract_document_ids(entities, relationships, semantic_chunks)
            context.documents = document_ids
            
            # Generate context summary
            context.context_summary = await self._generate_context_summary(
                query, entities, relationships, semantic_chunks, task_type
            )
            
            logger.info(f"Context built with {len(entities)} entities, {len(relationships)} relationships, {len(semantic_chunks)} chunks")
            return context
            
        except Exception as e:
            logger.error(f"Error building context: {str(e)}")
            return KnowledgeContext()
    
    async def _get_relevant_entities(self, query: str, intent_analysis: Dict[str, Any], 
                                   max_entities: int) -> List[Entity]:
        """Get relevant entities from knowledge graph"""
        try:
            # Search for entities by query
            entities = await self.knowledge_graph.search_entities(query, limit=max_entities)
            
            # If not enough entities found, try broader search
            if len(entities) < max_entities // 2:
                # Extract key terms from query for broader search
                key_terms = self._extract_key_terms(query)
                for term in key_terms[:3]:  # Try top 3 terms
                    additional_entities = await self.knowledge_graph.search_entities(term, limit=max_entities//2)
                    entities.extend(additional_entities)
                    entities = list({entity.id: entity for entity in entities}.values())  # Remove duplicates
            
            return entities[:max_entities]
            
        except Exception as e:
            logger.error(f"Error getting relevant entities: {str(e)}")
            return []
    
    async def _get_relevant_relationships(self, entities: List[Entity], 
                                        intent_analysis: Dict[str, Any]) -> List[Relationship]:
        """Get relevant relationships for the entities"""
        try:
            relationships = []
            
            for entity in entities[:5]:  # Limit to top 5 entities to avoid too many relationships
                entity_relationships = await self.knowledge_graph.get_entity_relationships(
                    str(entity.id)
                )
                
                # Convert to Relationship objects
                for rel_data in entity_relationships:
                    # This is a simplified conversion - in practice you'd need to fetch the actual Relationship objects
                    # For now, we'll create a minimal representation
                    relationship = Relationship(
                        source_entity_id=rel_data['source_entity']['id'],
                        target_entity_id=rel_data['target_entity']['id'],
                        relationship_type=rel_data['relationship']['type']
                    )
                    relationships.append(relationship)
            
            return relationships[:20]  # Limit total relationships
            
        except Exception as e:
            logger.error(f"Error getting relevant relationships: {str(e)}")
            return []
    
    async def _get_relevant_chunks(self, query: str, intent_analysis: Dict[str, Any], 
                                 max_chunks: int) -> List[Dict[str, Any]]:
        """Get relevant document chunks from vector store"""
        try:
            # Get document IDs from entities and relationships if available
            document_ids = None  # We'll implement this based on available context
            
            # Search for similar chunks
            chunks = await self.vector_store.search_similar(
                query=query,
                limit=max_chunks,
                document_ids=document_ids,
                threshold=0.6  # Lower threshold for broader results
            )
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error getting relevant chunks: {str(e)}")
            return []
    
    async def _generate_context_summary(self, query: str, entities: List[Entity], 
                                      relationships: List[Relationship], 
                                      semantic_chunks: List[Dict[str, Any]], 
                                      task_type: str) -> str:
        """Generate a summary of the assembled context"""
        try:
            summary_prompt = f"""
            Create a brief summary of the context assembled for this query:
            
            Query: {query}
            Task Type: {task_type}
            
            Relevant Entities: {len(entities)} entities found
            Relevant Relationships: {len(relationships)} relationships found
            Relevant Document Chunks: {len(semantic_chunks)} chunks found
            
            Provide a 2-3 sentence summary of what context is available and how it relates to the query.
            """
            
            summary = await self.ai_service.generate_text(summary_prompt)
            return summary
            
        except Exception as e:
            logger.error(f"Error generating context summary: {str(e)}")
            return f"Context assembled with {len(entities)} entities, {len(relationships)} relationships, and {len(semantic_chunks)} document chunks."
    
    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract key terms from query for broader entity search"""
        # Simple extraction - in practice you might use NLP libraries
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'what', 'when', 'where', 'why', 'how', 'who', 'which', 'that', 'this', 'these', 'those'}
        
        words = query.lower().split()
        key_terms = [word for word in words if word not in common_words and len(word) > 2]
        
        return key_terms[:5]  # Return top 5 terms
    
    def _extract_document_ids(self, entities: List[Entity], relationships: List[Relationship], 
                             semantic_chunks: List[Dict[str, Any]]) -> List[str]:
        """Extract unique document IDs from context components"""
        document_ids = set()
        
        # From entities
        for entity in entities:
            document_ids.update(entity.source_documents)
        
        # From relationships
        for relationship in relationships:
            document_ids.update(relationship.source_documents)
        
        # From semantic chunks
        for chunk in semantic_chunks:
            if 'metadata' in chunk and 'document_id' in chunk['metadata']:
                document_ids.add(chunk['metadata']['document_id'])
        
        return list(document_ids)
    
    async def get_context_for_content_generation(self, content_type: str, topic: str, 
                                               target_audience: Optional[str] = None) -> KnowledgeContext:
        """Get specialized context for content generation tasks"""
        try:
            # Build query based on content type and topic
            query = f"{content_type} about {topic}"
            if target_audience:
                query += f" for {target_audience}"
            
            # Get base context
            context = await self.build_context(query, task_type="content_generation")
            
            # Add content-specific context
            content_prompt = f"""
            For creating {content_type} content about {topic}, what additional context would be most relevant?
            Consider brand voice, messaging guidelines, and content strategy.
            """
            
            # You could extend this to include brand guidelines, content templates, etc.
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting content generation context: {str(e)}")
            return KnowledgeContext()
    
    async def get_context_for_strategic_analysis(self, strategic_question: str) -> KnowledgeContext:
        """Get specialized context for strategic analysis tasks"""
        try:
            # Build comprehensive context for strategic analysis
            context = await self.build_context(
                strategic_question, 
                task_type="strategic_analysis",
                max_entities=20,  # More entities for strategic analysis
                max_chunks=10     # More chunks for comprehensive analysis
            )
            
            # Add strategic analysis specific context
            # This could include market data, competitive intelligence, etc.
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting strategic analysis context: {str(e)}")
            return KnowledgeContext()
    
    async def close(self):
        """Clean up resources"""
        self.knowledge_graph.close() 
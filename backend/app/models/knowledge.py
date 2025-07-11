from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum
from .base import BaseEntity

class EntityType(str, Enum):
    """Entity types in the knowledge graph"""
    COMPANY = "company"
    PERSON = "person"
    PRODUCT = "product"
    SERVICE = "service"
    LOCATION = "location"
    INDUSTRY = "industry"
    TECHNOLOGY = "technology"
    CONCEPT = "concept"
    EVENT = "event"
    ORGANIZATION = "organization"

class RelationshipType(str, Enum):
    """Relationship types in the knowledge graph"""
    COMPETES_WITH = "competes_with"
    PARTNERS_WITH = "partners_with"
    ACQUIRES = "acquires"
    INVESTS_IN = "invests_in"
    EMPLOYS = "employs"
    FOUNDED = "founded"
    LOCATED_IN = "located_in"
    OPERATES_IN = "operates_in"
    PROVIDES = "provides"
    USES = "uses"
    SIMILAR_TO = "similar_to"
    PARENT_OF = "parent_of"
    SUBSIDIARY_OF = "subsidiary_of"

class Entity(BaseEntity):
    """Entity model for knowledge graph"""
    name: str = Field(..., description="Entity name")
    entity_type: EntityType = Field(..., description="Entity type")
    description: Optional[str] = Field(default=None, description="Entity description")
    
    # Attributes
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Entity attributes")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence")
    
    # Source information
    source_documents: List[str] = Field(default_factory=list, description="Source document IDs")
    extraction_method: str = Field(default="llm", description="How entity was extracted")
    
    # Metadata
    aliases: List[str] = Field(default_factory=list, description="Alternative names")
    tags: List[str] = Field(default_factory=list, description="Entity tags")

class Relationship(BaseEntity):
    """Relationship model for knowledge graph"""
    source_entity_id: str = Field(..., description="Source entity ID")
    target_entity_id: str = Field(..., description="Target entity ID")
    relationship_type: RelationshipType = Field(..., description="Relationship type")
    
    # Relationship properties
    properties: Dict[str, Any] = Field(default_factory=dict, description="Relationship properties")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence")
    
    # Source information
    source_documents: List[str] = Field(default_factory=list, description="Source document IDs")
    extraction_method: str = Field(default="llm", description="How relationship was extracted")

class KnowledgeQuery(BaseModel):
    """Knowledge graph query model"""
    query_type: str = Field(..., description="Query type (entity, relationship, path, etc.)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")
    limit: int = Field(default=50, description="Maximum results")
    include_metadata: bool = Field(default=True, description="Include metadata in results")

class EntitySearchRequest(BaseModel):
    """Entity search request"""
    query: str = Field(..., description="Search query")
    entity_types: Optional[List[EntityType]] = Field(default=None, description="Filter by entity types")
    limit: int = Field(default=20, description="Maximum results")
    include_relationships: bool = Field(default=False, description="Include related entities")

class RelationshipSearchRequest(BaseModel):
    """Relationship search request"""
    source_entity_id: Optional[str] = Field(default=None, description="Source entity ID")
    target_entity_id: Optional[str] = Field(default=None, description="Target entity ID")
    relationship_types: Optional[List[RelationshipType]] = Field(default=None, description="Filter by relationship types")
    limit: int = Field(default=50, description="Maximum results")

class KnowledgeContext(BaseModel):
    """Knowledge context for AI generation"""
    entities: List[Entity] = Field(default_factory=list, description="Relevant entities")
    relationships: List[Relationship] = Field(default_factory=list, description="Relevant relationships")
    documents: List[str] = Field(default_factory=list, description="Relevant document IDs")
    semantic_chunks: List[Dict[str, Any]] = Field(default_factory=list, description="Semantic search results")
    context_summary: Optional[str] = Field(default=None, description="Context summary")
    
    class Config:
        json_encoders = {
            'datetime': lambda v: v.isoformat(),
            'UUID': lambda v: str(v)
        } 
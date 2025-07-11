from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.models.knowledge import Entity, Relationship, EntitySearchRequest, RelationshipSearchRequest
from app.models.base import BaseResponse, PaginatedResponse
from app.services.knowledge_graph import KnowledgeGraph

router = APIRouter()

# Initialize services
knowledge_graph = KnowledgeGraph()

@router.get("/entities", response_model=PaginatedResponse)
async def search_entities(
    query: str,
    entity_types: Optional[str] = None,
    limit: int = 20,
    page: int = 1
):
    """Search for entities in the knowledge graph"""
    try:
        # Parse entity types if provided
        entity_type_list = None
        if entity_types:
            entity_type_list = [t.strip() for t in entity_types.split(",")]
        
        entities = await knowledge_graph.search_entities(
            query=query,
            entity_types=entity_type_list,
            limit=limit
        )
        
        return PaginatedResponse(
            success=True,
            data=[entity.dict() for entity in entities],
            total=len(entities),
            page=page,
            size=limit,
            pages=1
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity search failed: {str(e)}")

@router.get("/entities/{entity_id}", response_model=BaseResponse)
async def get_entity(entity_id: str):
    """Get entity details and relationships"""
    try:
        # Get entity relationships
        relationships = await knowledge_graph.get_entity_relationships(entity_id)
        
        # This would typically fetch the entity from database
        # For now, return mock data
        entity_data = {
            "id": entity_id,
            "name": "Sample Entity",
            "entity_type": "company",
            "description": "Sample entity description",
            "relationships": relationships
        }
        
        return BaseResponse(
            success=True,
            data=entity_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get entity: {str(e)}")

@router.get("/relationships", response_model=BaseResponse)
async def search_relationships(
    source_entity_id: Optional[str] = None,
    target_entity_id: Optional[str] = None,
    relationship_types: Optional[str] = None,
    limit: int = 50
):
    """Search for relationships in the knowledge graph"""
    try:
        # Parse relationship types if provided
        rel_type_list = None
        if relationship_types:
            rel_type_list = [t.strip() for t in relationship_types.split(",")]
        
        relationships = await knowledge_graph.get_entity_relationships(
            source_entity_id or "",
            rel_type_list
        )
        
        return BaseResponse(
            success=True,
            data={"relationships": relationships}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Relationship search failed: {str(e)}")

@router.get("/paths", response_model=BaseResponse)
async def find_paths(
    source_entity_id: str,
    target_entity_id: str,
    max_length: int = 3
):
    """Find paths between two entities"""
    try:
        paths = await knowledge_graph.find_paths(
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            max_length=max_length
        )
        
        return BaseResponse(
            success=True,
            data={
                "paths": paths,
                "source_entity_id": source_entity_id,
                "target_entity_id": target_entity_id,
                "max_length": max_length
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Path finding failed: {str(e)}")

@router.get("/statistics", response_model=BaseResponse)
async def get_knowledge_statistics():
    """Get knowledge graph statistics"""
    try:
        stats = await knowledge_graph.get_graph_statistics()
        
        return BaseResponse(
            success=True,
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.post("/entities", response_model=BaseResponse)
async def create_entity(entity: Entity):
    """Create a new entity in the knowledge graph"""
    try:
        success = await knowledge_graph.create_entity(entity)
        
        if success:
            return BaseResponse(
                success=True,
                message="Entity created successfully",
                data={"entity_id": str(entity.id)}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create entity")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity creation failed: {str(e)}")

@router.post("/relationships", response_model=BaseResponse)
async def create_relationship(relationship: Relationship):
    """Create a new relationship in the knowledge graph"""
    try:
        success = await knowledge_graph.create_relationship(relationship)
        
        if success:
            return BaseResponse(
                success=True,
                message="Relationship created successfully",
                data={"relationship_id": str(relationship.id)}
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to create relationship")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Relationship creation failed: {str(e)}")

@router.delete("/entities/{entity_id}", response_model=BaseResponse)
async def delete_entity(entity_id: str):
    """Delete an entity from the knowledge graph"""
    try:
        success = await knowledge_graph.delete_entity(entity_id)
        
        if success:
            return BaseResponse(
                success=True,
                message="Entity deleted successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to delete entity")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity deletion failed: {str(e)}") 
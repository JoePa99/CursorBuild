from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from app.models.knowledge import Entity, Relationship, EntityType, RelationshipType
from app.core.config import settings

logger = logging.getLogger(__name__)

class KnowledgeGraph:
    """Knowledge graph service using Neo4j"""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        logger.info("Knowledge graph initialized successfully")
    
    def close(self):
        """Close the database connection"""
        self.driver.close()
    
    async def create_entity(self, entity: Entity) -> bool:
        """Create a new entity in the knowledge graph"""
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MERGE (e:Entity {id: $id})
                    SET e.name = $name,
                        e.entity_type = $entity_type,
                        e.description = $description,
                        e.attributes = $attributes,
                        e.confidence_score = $confidence_score,
                        e.source_documents = $source_documents,
                        e.extraction_method = $extraction_method,
                        e.aliases = $aliases,
                        e.tags = $tags,
                        e.created_at = $created_at,
                        e.updated_at = $updated_at
                    RETURN e
                """, {
                    'id': str(entity.id),
                    'name': entity.name,
                    'entity_type': entity.entity_type.value,
                    'description': entity.description,
                    'attributes': entity.attributes,
                    'confidence_score': entity.confidence_score,
                    'source_documents': entity.source_documents,
                    'extraction_method': entity.extraction_method,
                    'aliases': entity.aliases,
                    'tags': entity.tags,
                    'created_at': entity.created_at.isoformat(),
                    'updated_at': entity.updated_at.isoformat()
                })
                
                logger.info(f"Created entity: {entity.name}")
                return True
                
        except Exception as e:
            logger.error(f"Error creating entity: {str(e)}")
            return False
    
    async def create_relationship(self, relationship: Relationship) -> bool:
        """Create a new relationship in the knowledge graph"""
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (source:Entity {id: $source_id})
                    MATCH (target:Entity {id: $target_id})
                    MERGE (source)-[r:RELATES_TO]->(target)
                    SET r.relationship_type = $relationship_type,
                        r.properties = $properties,
                        r.confidence_score = $confidence_score,
                        r.source_documents = $source_documents,
                        r.extraction_method = $extraction_method,
                        r.created_at = $created_at,
                        r.updated_at = $updated_at
                    RETURN r
                """, {
                    'source_id': relationship.source_entity_id,
                    'target_id': relationship.target_entity_id,
                    'relationship_type': relationship.relationship_type.value,
                    'properties': relationship.properties,
                    'confidence_score': relationship.confidence_score,
                    'source_documents': relationship.source_documents,
                    'extraction_method': relationship.extraction_method,
                    'created_at': relationship.created_at.isoformat(),
                    'updated_at': relationship.updated_at.isoformat()
                })
                
                logger.info(f"Created relationship: {relationship.relationship_type}")
                return True
                
        except Exception as e:
            logger.error(f"Error creating relationship: {str(e)}")
            return False
    
    async def search_entities(self, query: str, entity_types: Optional[List[EntityType]] = None, 
                            limit: int = 20) -> List[Entity]:
        """Search for entities by name or description"""
        try:
            with self.driver.session() as session:
                # Build query with optional type filter
                cypher_query = """
                    MATCH (e:Entity)
                    WHERE toLower(e.name) CONTAINS toLower($query)
                       OR (e.description IS NOT NULL AND toLower(e.description) CONTAINS toLower($query))
                """
                
                if entity_types:
                    type_values = [t.value for t in entity_types]
                    cypher_query += " AND e.entity_type IN $entity_types"
                
                cypher_query += """
                    RETURN e
                    ORDER BY e.confidence_score DESC
                    LIMIT $limit
                """
                
                params = {
                    'query': query,
                    'limit': limit
                }
                
                if entity_types:
                    params['entity_types'] = type_values
                
                result = session.run(cypher_query, params)
                entities = []
                
                for record in result:
                    node = record['e']
                    entity = Entity(
                        id=node['id'],
                        name=node['name'],
                        entity_type=EntityType(node['entity_type']),
                        description=node.get('description'),
                        attributes=node.get('attributes', {}),
                        confidence_score=node.get('confidence_score', 1.0),
                        source_documents=node.get('source_documents', []),
                        extraction_method=node.get('extraction_method', 'llm'),
                        aliases=node.get('aliases', []),
                        tags=node.get('tags', [])
                    )
                    entities.append(entity)
                
                return entities
                
        except Exception as e:
            logger.error(f"Error searching entities: {str(e)}")
            return []
    
    async def get_entity_relationships(self, entity_id: str, 
                                     relationship_types: Optional[List[RelationshipType]] = None) -> List[Dict[str, Any]]:
        """Get relationships for a specific entity"""
        try:
            with self.driver.session() as session:
                cypher_query = """
                    MATCH (source:Entity {id: $entity_id})-[r:RELATES_TO]->(target:Entity)
                """
                
                if relationship_types:
                    type_values = [t.value for t in relationship_types]
                    cypher_query += " WHERE r.relationship_type IN $relationship_types"
                
                cypher_query += """
                    RETURN source, r, target
                    ORDER BY r.confidence_score DESC
                """
                
                params = {'entity_id': entity_id}
                if relationship_types:
                    params['relationship_types'] = type_values
                
                result = session.run(cypher_query, params)
                relationships = []
                
                for record in result:
                    rel_data = {
                        'source_entity': {
                            'id': record['source']['id'],
                            'name': record['source']['name'],
                            'entity_type': record['source']['entity_type']
                        },
                        'target_entity': {
                            'id': record['target']['id'],
                            'name': record['target']['name'],
                            'entity_type': record['target']['entity_type']
                        },
                        'relationship': {
                            'type': record['r']['relationship_type'],
                            'properties': record['r'].get('properties', {}),
                            'confidence_score': record['r'].get('confidence_score', 1.0)
                        }
                    }
                    relationships.append(rel_data)
                
                return relationships
                
        except Exception as e:
            logger.error(f"Error getting entity relationships: {str(e)}")
            return []
    
    async def find_paths(self, source_entity_id: str, target_entity_id: str, 
                        max_length: int = 3) -> List[List[Dict[str, Any]]]:
        """Find paths between two entities"""
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH path = (source:Entity {id: $source_id})-[*1..$max_length]-(target:Entity {id: $target_id})
                    RETURN path
                    LIMIT 10
                """, {
                    'source_id': source_entity_id,
                    'target_id': target_entity_id,
                    'max_length': max_length
                })
                
                paths = []
                for record in result:
                    path = record['path']
                    path_data = []
                    
                    for i, node in enumerate(path.nodes):
                        if i > 0:  # Add relationship
                            rel = path.relationships[i-1]
                            path_data.append({
                                'type': 'relationship',
                                'relationship_type': rel['relationship_type'],
                                'properties': rel.get('properties', {})
                            })
                        
                        path_data.append({
                            'type': 'entity',
                            'id': node['id'],
                            'name': node['name'],
                            'entity_type': node['entity_type']
                        })
                    
                    paths.append(path_data)
                
                return paths
                
        except Exception as e:
            logger.error(f"Error finding paths: {str(e)}")
            return []
    
    async def get_graph_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        try:
            with self.driver.session() as session:
                # Count entities
                entity_count = session.run("MATCH (e:Entity) RETURN count(e) as count").single()['count']
                
                # Count relationships
                rel_count = session.run("MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count").single()['count']
                
                # Count by entity type
                entity_types = session.run("""
                    MATCH (e:Entity)
                    RETURN e.entity_type as type, count(e) as count
                    ORDER BY count DESC
                """).data()
                
                # Count by relationship type
                rel_types = session.run("""
                    MATCH ()-[r:RELATES_TO]->()
                    RETURN r.relationship_type as type, count(r) as count
                    ORDER BY count DESC
                """).data()
                
                return {
                    'total_entities': entity_count,
                    'total_relationships': rel_count,
                    'entity_types': entity_types,
                    'relationship_types': rel_types
                }
                
        except Exception as e:
            logger.error(f"Error getting graph statistics: {str(e)}")
            return {
                'total_entities': 0,
                'total_relationships': 0,
                'entity_types': [],
                'relationship_types': []
            }
    
    async def delete_entity(self, entity_id: str) -> bool:
        """Delete an entity and its relationships"""
        try:
            with self.driver.session() as session:
                session.run("""
                    MATCH (e:Entity {id: $entity_id})
                    DETACH DELETE e
                """, {'entity_id': entity_id})
                
                logger.info(f"Deleted entity: {entity_id}")
                return True
                
        except Exception as e:
            logger.error(f"Error deleting entity: {str(e)}")
            return False 
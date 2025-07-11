import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import logging
import numpy as np
import hashlib

from app.models.document import DocumentChunk
from app.core.config import settings

logger = logging.getLogger(__name__)

class VectorStore:
    """Vector store service using ChromaDB for semantic search"""
    
    def __init__(self):
        # Use local ChromaDB client instead of HTTP client
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize simple embedding (placeholder for now)
        self.embedding_model = None
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="document_chunks",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info("Vector store initialized successfully")
    
    async def add_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """Add document chunks to vector store"""
        try:
            if not chunks:
                return True
            
            # Prepare data for ChromaDB
            ids = []
            texts = []
            metadatas = []
            
            for chunk in chunks:
                chunk_id = f"{chunk.document_id}_{chunk.chunk_index}"
                ids.append(chunk_id)
                texts.append(chunk.content)
                
                metadata = {
                    "document_id": str(chunk.document_id),
                    "chunk_index": chunk.chunk_index,
                    "start_position": chunk.start_position,
                    "end_position": chunk.end_position,
                    "created_at": chunk.created_at.isoformat(),
                    **chunk.metadata
                }
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(chunks)} chunks to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {str(e)}")
            return False
    
    async def search_similar(self, query: str, limit: int = 10, 
                           document_ids: Optional[List[str]] = None,
                           threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar document chunks"""
        try:
            # Prepare query filter
            where_filter = {}
            if document_ids:
                where_filter["document_id"] = {"$in": document_ids}
            
            # Search in collection
            results = self.collection.query(
                query_texts=[query],
                n_results=limit,
                where=where_filter if where_filter else None
            )
            
            # Process results
            similar_chunks = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # Convert distance to similarity score
                    similarity_score = 1 - distance
                    
                    if similarity_score >= threshold:
                        chunk_data = {
                            "content": doc,
                            "metadata": metadata,
                            "similarity_score": similarity_score,
                            "document_id": metadata.get("document_id"),
                            "chunk_index": metadata.get("chunk_index")
                        }
                        similar_chunks.append(chunk_data)
            
            # Sort by similarity score
            similar_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            logger.info(f"Found {len(similar_chunks)} similar chunks for query: {query}")
            return similar_chunks
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    async def get_chunk_embedding(self, text: str) -> List[float]:
        """Get embedding for a text chunk"""
        try:
            # Simple hash-based embedding for now
            # In production, use a proper embedding model
            hash_obj = hashlib.md5(text.encode())
            hash_bytes = hash_obj.digest()
            embedding = [float(b) / 255.0 for b in hash_bytes[:8]]  # Convert to 8-dim vector
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []
    
    async def update_chunk_embedding(self, chunk_id: str, text: str) -> bool:
        """Update embedding for a specific chunk"""
        try:
            embedding = await self.get_chunk_embedding(text)
            if embedding:
                # Note: ChromaDB doesn't support direct embedding updates
                # We would need to delete and re-add the chunk
                logger.warning("Embedding updates require chunk re-insertion")
                return False
            return False
        except Exception as e:
            logger.error(f"Error updating chunk embedding: {str(e)}")
            return False
    
    async def delete_document_chunks(self, document_id: str) -> bool:
        """Delete all chunks for a specific document"""
        try:
            # Delete chunks by document_id
            self.collection.delete(
                where={"document_id": document_id}
            )
            
            logger.info(f"Deleted chunks for document: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document chunks: {str(e)}")
            return False
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"total_chunks": 0, "collection_name": "unknown"}
    
    async def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Search with similarity scores"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                distances = results['distances'][0]
                metadatas = results['metadatas'][0]
                
                # Convert to (doc, score) tuples
                scored_docs = []
                for doc, distance, metadata in zip(documents, distances, metadatas):
                    score = 1 - distance  # Convert distance to similarity score
                    scored_docs.append((doc, score, metadata))
                
                return scored_docs
            
            return []
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return [] 
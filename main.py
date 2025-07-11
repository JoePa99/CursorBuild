#!/usr/bin/env python3
"""
Blueprint AI - Corporate Intelligence Platform
Root entry point for Railway deployment
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
import uuid
from typing import List, Optional
import google.generativeai as genai
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
import hashlib
import fitz  # PyMuPDF
from docx import Document
import tempfile
import shutil
from neo4j import GraphDatabase
import spacy
from collections import defaultdict

# Configure Google Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# Configure Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Initialize Neo4j driver
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

app = FastAPI(title="Blueprint AI - Corporate Intelligence Platform", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB for vector storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="company_knowledge",
    metadata={"description": "Company knowledge base and context"}
)

# Store company metadata
company_data = {
    "name": "",
    "industry": "",
    "documents": [],
    "context_summary": "",
    "business_processes": [],
    "key_metrics": []
}

class CompanySetup(BaseModel):
    name: str
    industry: str
    description: str
    key_processes: List[str]
    goals: List[str]

class ContextQuery(BaseModel):
    query: str
    context_type: str = "general"  # general, sales, support, process, etc.

class DocumentInfo(BaseModel):
    filename: str
    content_type: str
    size: int
    chunks: int

class KnowledgeGraphQuery(BaseModel):
    query: str
    depth: int = 2

@app.get("/")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Blueprint AI Corporate Intelligence Platform",
        "version": "2.0.0",
        "company_configured": bool(company_data["name"]),
        "documents_loaded": len(company_data["documents"])
    }

def create_knowledge_graph(tx, company_name, industry, processes, goals):
    """Create initial knowledge graph structure for company"""
    
    # Create Company node
    tx.run("""
        MERGE (c:Company {name: $name, industry: $industry})
        SET c.created_at = datetime()
        """, name=company_name, industry=industry)
    
    # Create Process nodes and relationships
    for process in processes:
        tx.run("""
            MERGE (p:Process {name: $process})
            MERGE (c:Company {name: $company})
            MERGE (c)-[:HAS_PROCESS]->(p)
            """, process=process, company=company_name)
    
    # Create Goal nodes and relationships
    for goal in goals:
        tx.run("""
            MERGE (g:Goal {description: $goal})
            MERGE (c:Company {name: $company})
            MERGE (c)-[:HAS_GOAL]->(g)
            """, goal=goal, company=company_name)

def extract_entities_and_relationships(text, document_id, document_type):
    """Extract entities and relationships from document text"""
    
    # Use Gemini to extract entities and relationships
    prompt = f"""
    Analyze this text and extract:
    1. Key entities (people, departments, products, concepts, locations)
    2. Relationships between entities
    3. Important concepts and their definitions
    
    Text: {text[:2000]}  # Limit for API
    
    Return as JSON:
    {{
        "entities": [
            {{"name": "entity_name", "type": "PERSON|DEPARTMENT|PRODUCT|CONCEPT|LOCATION", "description": "brief description"}}
        ],
        "relationships": [
            {{"from": "entity1", "to": "entity2", "type": "WORKS_IN|MANAGES|USES|LOCATED_IN|PART_OF", "description": "relationship description"}}
        ],
        "concepts": [
            {{"name": "concept_name", "definition": "definition", "importance": "HIGH|MEDIUM|LOW"}}
        ]
    }}
    """
    
    try:
        if GOOGLE_API_KEY:
            response = model.generate_content(prompt)
            result = json.loads(response.text)
            return result
    except:
        # Fallback: simple entity extraction
        return {
            "entities": [],
            "relationships": [],
            "concepts": []
        }

def add_document_to_knowledge_graph(tx, document_id, filename, document_type, entities, relationships, concepts, company_name):
    """Add document and its extracted knowledge to the graph"""
    
    # Create Document node
    tx.run("""
        MERGE (d:Document {id: $doc_id, filename: $filename, type: $doc_type})
        MERGE (c:Company {name: $company})
        MERGE (c)-[:HAS_DOCUMENT]->(d)
        """, doc_id=document_id, filename=filename, doc_type=document_type, company=company_name)
    
    # Create Entity nodes and relationships
    for entity in entities:
        tx.run("""
            MERGE (e:Entity {name: $name, type: $type})
            MERGE (d:Document {id: $doc_id})
            MERGE (d)-[:MENTIONS]->(e)
            SET e.description = $description
            """, name=entity["name"], type=entity["type"], doc_id=document_id, 
                 description=entity.get("description", ""))
    
    # Create Relationship nodes
    for rel in relationships:
        tx.run("""
            MERGE (e1:Entity {name: $from_entity})
            MERGE (e2:Entity {name: $to_entity})
            MERGE (e1)-[r:RELATES_TO {type: $rel_type}]->(e2)
            SET r.description = $description
            """, from_entity=rel["from"], to_entity=rel["to"], rel_type=rel["type"], 
                 description=rel.get("description", ""))
    
    # Create Concept nodes
    for concept in concepts:
        tx.run("""
            MERGE (c:Concept {name: $name})
            MERGE (d:Document {id: $doc_id})
            MERGE (d)-[:DEFINES]->(c)
            SET c.definition = $definition, c.importance = $importance
            """, name=concept["name"], doc_id=document_id, 
                 definition=concept["definition"], importance=concept["importance"])

def query_knowledge_graph(tx, query, depth=2):
    """Query the knowledge graph for relevant information"""
    
    # Cypher query to find relevant entities and relationships
    cypher_query = """
    MATCH (n)-[r*1..2]-(m)
    WHERE toLower(n.name) CONTAINS toLower($query) 
       OR toLower(m.name) CONTAINS toLower($query)
    RETURN n, r, m
    LIMIT 50
    """
    
    result = tx.run(cypher_query, query=query)
    return [record.data() for record in result]

@app.post("/setup-company")
async def setup_company(setup: CompanySetup):
    """Initialize company context and business profile"""
    global company_data
    
    company_data.update({
        "name": setup.name,
        "industry": setup.industry,
        "description": setup.description,
        "business_processes": setup.key_processes,
        "goals": setup.goals
    })
    
    # Create knowledge graph structure
    with neo4j_driver.session() as session:
        session.execute_write(create_knowledge_graph, 
                            setup.name, setup.industry, 
                            setup.key_processes, setup.goals)
    
    # Generate initial context summary
    context_prompt = f"""
    Company: {setup.name}
    Industry: {setup.industry}
    Description: {setup.description}
    Key Processes: {', '.join(setup.key_processes)}
    Goals: {', '.join(setup.goals)}
    
    Create a comprehensive business context summary that captures the essence of this company.
    Include typical challenges, opportunities, and business context for this type of organization.
    """
    
    if GOOGLE_API_KEY:
        response = model.generate_content(context_prompt)
        company_data["context_summary"] = response.text
    
    return {
        "status": "success",
        "message": f"Company {setup.name} configured successfully",
        "company_data": company_data
    }

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    description: str = Form("")
):
    """Upload and process company documents for context building"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Validate file type
    allowed_types = ['.pdf', '.docx', '.txt', '.md']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File type {file_ext} not supported")
    
    # Create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
    
    try:
        # Extract text based on file type
        text_content = ""
        if file_ext == '.pdf':
            doc = fitz.open(temp_path)
            text_content = ""
            for page in doc:
                text_content += page.get_text()
            doc.close()
        elif file_ext == '.docx':
            doc = Document(temp_path)
            text_content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:  # .txt or .md
            with open(temp_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        
        # Split into chunks for vector storage
        chunks = split_text_into_chunks(text_content, 1000)
        
        # Store in vector database
        document_id = str(uuid.uuid4())
        collection.add(
            documents=chunks,
            metadatas=[{
                "filename": file.filename,
                "document_type": document_type,
                "description": description,
                "chunk_index": i
            } for i in range(len(chunks))],
            ids=[f"{document_id}_{i}" for i in range(len(chunks))]
        )
        
        # Extract entities and relationships for knowledge graph
        extracted_knowledge = extract_entities_and_relationships(
            text_content, document_id, document_type
        )
        
        # Add to knowledge graph
        with neo4j_driver.session() as session:
            session.execute_write(add_document_to_knowledge_graph,
                                document_id, file.filename, document_type,
                                extracted_knowledge["entities"],
                                extracted_knowledge["relationships"],
                                extracted_knowledge["concepts"],
                                company_data["name"])
        
        # Update company data
        doc_info = DocumentInfo(
            filename=file.filename,
            content_type=document_type,
            size=len(text_content),
            chunks=len(chunks)
        )
        company_data["documents"].append(doc_info.dict())
        
        return {
            "status": "success",
            "message": f"Document {file.filename} processed successfully",
            "chunks_created": len(chunks),
            "entities_extracted": len(extracted_knowledge["entities"]),
            "relationships_found": len(extracted_knowledge["relationships"]),
            "document_info": doc_info.dict()
        }
        
    finally:
        os.unlink(temp_path)

@app.post("/query-context")
async def query_context(query: ContextQuery):
    """Query company knowledge with full context awareness"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Search relevant documents
    results = collection.query(
        query_texts=[query.query],
        n_results=5
    )
    
    # Query knowledge graph
    graph_results = []
    with neo4j_driver.session() as session:
        graph_results = session.execute_read(query_knowledge_graph, query.query, 2)
    
    # Build context from company data, relevant documents, and knowledge graph
    context = build_context(query.query, results, query.context_type, graph_results)
    
    # Generate AI response with full context
    if GOOGLE_API_KEY:
        response = generate_contextual_response(query.query, context, query.context_type)
    else:
        response = "AI service not configured"
    
    return {
        "query": query.query,
        "context_type": query.context_type,
        "response": response,
        "relevant_documents": results["metadatas"][0] if results["metadatas"] else [],
        "knowledge_graph_results": len(graph_results),
        "context_used": context["summary"]
    }

@app.post("/query-knowledge-graph")
async def query_knowledge_graph_endpoint(query: KnowledgeGraphQuery):
    """Query the knowledge graph directly"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    with neo4j_driver.session() as session:
        results = session.execute_read(query_knowledge_graph, query.query, query.depth)
    
    return {
        "query": query.query,
        "depth": query.depth,
        "results": results,
        "total_relationships": len(results)
    }

@app.get("/knowledge-graph-stats")
async def get_knowledge_graph_stats():
    """Get statistics about the knowledge graph"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    with neo4j_driver.session() as session:
        # Get node counts by type
        node_stats = session.run("""
            MATCH (n)
            RETURN labels(n)[0] as type, count(n) as count
            ORDER BY count DESC
        """).data()
        
        # Get relationship counts by type
        rel_stats = session.run("""
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            ORDER BY count DESC
        """).data()
        
        # Get graph density
        density = session.run("""
            MATCH (n)
            MATCH ()-[r]->()
            RETURN count(n) as nodes, count(r) as relationships
        """).single()
    
    return {
        "node_types": node_stats,
        "relationship_types": rel_stats,
        "total_nodes": density["nodes"] if density else 0,
        "total_relationships": density["relationships"] if density else 0
    }

@app.get("/company-context")
async def get_company_context():
    """Get current company context and knowledge base status"""
    return {
        "company": company_data,
        "knowledge_base": {
            "total_documents": len(company_data["documents"]),
            "total_chunks": sum(doc["chunks"] for doc in company_data["documents"]),
            "document_types": list(set(doc["content_type"] for doc in company_data["documents"]))
        }
    }

@app.post("/generate-business-content")
async def generate_business_content(
    content_type: str = Form(...),
    topic: str = Form(...),
    target_audience: str = Form(...),
    tone: str = Form("professional")
):
    """Generate business content using company context"""
    
    if not company_data["name"]:
        raise HTTPException(status_code=400, detail="Please setup company first")
    
    # Build business context
    business_context = f"""
    Company: {company_data['name']}
    Industry: {company_data['industry']}
    Context: {company_data['context_summary']}
    Processes: {', '.join(company_data['business_processes'])}
    Goals: {', '.join(company_data['goals'])}
    """
    
    # Generate content with company context
    prompt = f"""
    {business_context}
    
    Generate {content_type} about: {topic}
    Target Audience: {target_audience}
    Tone: {tone}
    
    Make this content highly relevant to {company_data['name']} and their specific business context.
    """
    
    if GOOGLE_API_KEY:
        response = model.generate_content(prompt)
        content = response.text
    else:
        content = "AI service not configured"
    
    return {
        "content_type": content_type,
        "topic": topic,
        "content": content,
        "context_used": business_context
    }

def split_text_into_chunks(text: str, chunk_size: int) -> List[str]:
    """Split text into overlapping chunks for better context"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size // 2):  # 50% overlap
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def build_context(query: str, search_results: dict, context_type: str, graph_results: List = None) -> dict:
    """Build comprehensive context from company data, search results, and knowledge graph"""
    
    # Extract relevant document content
    relevant_docs = []
    if search_results["documents"]:
        relevant_docs = search_results["documents"][0]
    
    # Process knowledge graph results
    graph_context = ""
    if graph_results:
        entities = set()
        relationships = set()
        for result in graph_results:
            if "n" in result:
                entities.add(result["n"].get("name", ""))
            if "m" in result:
                entities.add(result["m"].get("name", ""))
            if "r" in result:
                relationships.add(str(result["r"]))
        
        graph_context = f"""
        Knowledge Graph Context:
        Related Entities: {', '.join(list(entities)[:10])}
        Relationships: {len(relationships)} connections found
        """
    
    # Build context summary
    context_summary = f"""
    Company Context:
    - Name: {company_data['name']}
    - Industry: {company_data['industry']}
    - Business Context: {company_data['context_summary']}
    
    Query Context: {query}
    Context Type: {context_type}
    
    Relevant Company Knowledge:
    {chr(10).join(relevant_docs[:3]) if relevant_docs else 'No specific documents found'}
    
    {graph_context}
    """
    
    return {
        "summary": context_summary,
        "relevant_documents": relevant_docs,
        "knowledge_graph_results": len(graph_results) if graph_results else 0,
        "company_data": company_data
    }

def generate_contextual_response(query: str, context: dict, context_type: str) -> str:
    """Generate AI response with full company context"""
    
    prompt = f"""
    You are an AI assistant for {company_data['name']}, a {company_data['industry']} company.
    
    Company Context:
    {context['summary']}
    
    User Query: {query}
    
    Provide a comprehensive, contextually relevant response that:
    1. Uses specific knowledge about {company_data['name']}
    2. References relevant company processes and goals
    3. Leverages insights from the knowledge graph if available
    4. Provides actionable insights based on the company's context
    5. Maintains professional tone appropriate for {context_type} context
    
    Response:
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
# Blueprint: AI-Powered Corporate Intelligence & Content Generation Application

## Mission Statement
To create an application that transforms a company's unstructured and structured corporate knowledge into a dynamic, intelligent core, empowering teams to make smarter decisions, generate on-brand content, and execute their strategy with unprecedented speed and coherence.

## Architecture Overview

### 🏗️ System Architecture
- **Backend**: FastAPI (Python) - High-performance async API framework
- **Frontend**: React with TypeScript - Modern, responsive UI
- **Database**: 
  - Neo4j (Graph Database) - Entity relationships and structured knowledge
  - ChromaDB (Vector Database) - Semantic search and embeddings
- **AI Services**: Google Gemini API for LLM and image generation
- **File Processing**: Apache Tika, PyMuPDF for document extraction
- **Authentication**: JWT-based secure authentication

### 📁 Project Structure
```
blueprint-ai/
├── backend/                 # FastAPI backend services
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core configuration and utilities
│   │   ├── models/         # Data models and schemas
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI application entry point
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service calls
│   │   └── utils/          # Frontend utilities
│   ├── package.json        # Node.js dependencies
│   └── public/             # Static assets
├── docker-compose.yml      # Development environment setup
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- Neo4j Database
- Google Cloud Platform account (for Gemini API)

### Installation

1. **Clone and Setup**
```bash
git clone <repository-url>
cd blueprint-ai
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
npm install
```

4. **Environment Configuration**
```bash
# Copy and configure environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

5. **Start Development Environment**
```bash
docker-compose up -d
```

## 🧠 Core Features

### 1. Knowledge Core Architecture
- **Data Ingestion Pipeline**: Secure document upload and processing
- **Hybrid Knowledge Database**: Graph + Vector database integration
- **Entity & Relationship Extraction**: Automated knowledge graph building

### 2. AI Intelligence Layer
- **Context Engineering Service**: Dynamic context assembly
- **Multi-Modal Generation**: Text and image generation with brand consistency

### 3. Application Modules
- **Q&A Chat**: Intelligent corporate knowledge assistant
- **Content Studio**: Long-form content generation
- **Performance Grid**: Multi-variant ad asset creation
- **Sales Generator**: Personalized outreach automation
- **Customer Support**: Relationship management hub
- **Thought Partner**: Strategic planning and scenario modeling

## 🔧 Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

### Database Management
```bash
# Neo4j Browser: http://localhost:7474
# ChromaDB: http://localhost:8000
```

## 📊 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details. 
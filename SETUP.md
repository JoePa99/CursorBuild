# Blueprint AI - Setup Guide

## 🚀 Quick Start

This guide will help you set up the Blueprint AI Corporate Intelligence Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose** (v20.10+)
- **Python 3.9+** (for local development)
- **Node.js 18+** (for local development)
- **Git**

## 📋 Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd blueprint-ai
```

### 2. Environment Configuration

#### Backend Configuration

```bash
# Copy the example environment file
cp backend/env.example backend/.env

# Edit the environment file with your settings
nano backend/.env
```

**Required Environment Variables:**

```env
# Application Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database Settings
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# AI Services (Required)
GOOGLE_API_KEY=your-google-api-key-here

# Optional AI Services
OPENAI_API_KEY=your-openai-api-key-here
```

#### Frontend Configuration

```bash
# Create frontend environment file
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > frontend/.env
```

### 3. Start the Application

#### Option A: Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Option B: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Databases:**
```bash
# Start Neo4j
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.14.1

# Start ChromaDB
docker run -d \
  --name chromadb \
  -p 8001:8000 \
  chromadb/chroma:latest

# Start Redis
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

## 🌐 Access Points

Once the application is running, you can access:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **ChromaDB**: http://localhost:8001

## 🔧 Configuration Details

### AI Services Setup

#### Google Gemini API

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file:
   ```env
   GOOGLE_API_KEY=your-api-key-here
   ```

#### OpenAI API (Optional)

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add the key to your `.env` file:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

### Database Configuration

#### Neo4j

- **Default Credentials**: neo4j/password
- **Change Password**: Visit http://localhost:7474 and change the default password
- **Update .env**: Update `NEO4J_PASSWORD` in your `.env` file

#### ChromaDB

- **Default Configuration**: Runs on port 8001
- **Persistence**: Data is stored in Docker volumes
- **No Authentication**: Configured for development

## 📁 Project Structure

```
blueprint-ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # React frontend
│   ├── src/                # Source code
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Development environment
├── README.md               # Project overview
└── SETUP.md               # This file
```

## 🧪 Testing the Setup

### 1. Health Check

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "service": "blueprint-ai"}
```

### 2. Upload a Document

1. Open http://localhost:3000
2. Navigate to the Documents section
3. Upload a PDF or DOCX file
4. Check the processing status

### 3. Test Chat

1. Open the Q&A Chat module
2. Ask a question about your uploaded documents
3. Verify the AI response

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts

If you get port conflicts, check what's running on the required ports:

```bash
# Check ports in use
lsof -i :8000
lsof -i :3000
lsof -i :7474
```

#### 2. Database Connection Issues

```bash
# Check Neo4j status
docker-compose logs neo4j

# Check ChromaDB status
docker-compose logs chromadb
```

#### 3. AI Service Errors

- Verify your API keys are correct
- Check API quotas and limits
- Ensure internet connectivity

#### 4. File Upload Issues

```bash
# Check upload directory permissions
ls -la backend/uploads/

# Create directory if missing
mkdir -p backend/uploads
chmod 755 backend/uploads
```

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f
```

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables**: Use proper secrets management
2. **Database Security**: Configure authentication and encryption
3. **API Keys**: Use environment-specific keys
4. **SSL/TLS**: Configure HTTPS
5. **Monitoring**: Add logging and monitoring solutions
6. **Backup**: Configure database backups

## 📚 Next Steps

1. **Upload Documents**: Start by uploading your corporate documents
2. **Explore Modules**: Try each application module
3. **Customize**: Adapt the system to your specific needs
4. **Integrate**: Connect external data sources
5. **Scale**: Optimize for your usage patterns

## 🤝 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the API documentation at http://localhost:8000/docs
3. Check the logs for error messages
4. Create an issue in the project repository

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
# Blueprint AI Deployment Guide

This guide covers deploying both the backend and frontend of the Blueprint AI platform.

## Backend Deployment (Railway)

The backend is already deployed and running at: `https://cursorbuild-production.up.railway.app`

### Backend Features Available:
- ✅ Health check endpoint
- ✅ Content generation with Google Gemini AI
- ✅ Q&A functionality
- ✅ Sales content generation
- ✅ Document analysis (basic)

### Backend API Endpoints:
- `GET /` - Health check
- `POST /generate-content` - Generate general content
- `POST /ask-question` - Q&A functionality
- `POST /generate-sales-content` - Sales content generation
- `POST /analyze-document` - Document analysis

## Frontend Deployment (Vercel)

### Prerequisites:
1. GitHub account
2. Vercel account (free tier available)

### Steps to Deploy Frontend:

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add React frontend"
   git push origin main
   ```

2. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your GitHub repository
   - Set the following configuration:
     - **Framework Preset**: Create React App
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `build`
   - Click "Deploy"

3. **Environment Variables** (if needed):
   - The frontend is configured to connect to the Railway backend
   - No additional environment variables are required

### Frontend Features:
- 🎨 Modern, responsive UI with Tailwind CSS
- 📊 Dashboard with feature overview
- ✍️ Content Studio for AI content generation
- 💬 Interactive Q&A Chat
- 📈 Sales Generator with detailed forms
- 📄 Document Analysis (upload interface)

## Testing the Deployment

1. **Backend Test**:
   ```bash
   curl https://cursorbuild-production.up.railway.app/
   # Should return: {"status": "healthy", "message": "Blueprint AI API is running"}
   ```

2. **Frontend Test**:
   - Visit your Vercel URL
   - Navigate through all pages
   - Test the AI features by connecting to the backend

## Local Development

### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend:
```bash
cd frontend
npm install
npm start
```

## Troubleshooting

### Common Issues:

1. **CORS Errors**: The backend is configured to allow all origins for development
2. **API Connection**: Ensure the frontend is pointing to the correct Railway URL
3. **Build Failures**: Check that all dependencies are properly installed

### Support:
- Backend logs: Check Railway dashboard
- Frontend logs: Check Vercel dashboard
- Local development: Check terminal output

## Next Steps

After successful deployment:

1. **Add Authentication**: Implement user login/signup
2. **Database Integration**: Add persistent storage
3. **File Upload**: Enhance document analysis
4. **Advanced Features**: Add more AI capabilities
5. **Monitoring**: Add analytics and error tracking 
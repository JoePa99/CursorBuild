# Blueprint AI Frontend

A modern React frontend for the Blueprint AI Corporate Intelligence Platform.

## Features

- **Dashboard**: Overview of all AI features and quick access
- **Content Studio**: Generate compelling content with AI assistance
- **Q&A Chat**: Interactive AI-powered question answering
- **Sales Generator**: Create persuasive sales content
- **Document Analysis**: Upload and analyze documents with AI

## Tech Stack

- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Lucide React for icons
- React Hot Toast for notifications

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Building for Production

```bash
npm run build
```

## Deployment

This frontend is designed to be deployed on Vercel. The backend API is hosted on Railway.

### Environment Variables

The frontend connects to the backend API at `https://cursorbuild-production.up.railway.app`.

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── App.tsx        # Main app component
├── index.tsx      # App entry point
└── index.css      # Global styles
```

## API Endpoints

The frontend connects to these backend endpoints:

- `POST /generate-content` - Generate general content
- `POST /ask-question` - Q&A functionality
- `POST /generate-sales-content` - Sales content generation
- `POST /analyze-document` - Document analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request 
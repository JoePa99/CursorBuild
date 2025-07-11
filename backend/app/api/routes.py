from fastapi import APIRouter
from app.api.endpoints import documents, knowledge, chat, content, sales, support, thought_partner

# Main API router
api_router = APIRouter()

# Include all endpoint modules
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Graph"])
api_router.include_router(chat.router, prefix="/chat", tags=["Q&A Chat"])
api_router.include_router(content.router, prefix="/content", tags=["Content Studio"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales Generator"])
api_router.include_router(support.router, prefix="/support", tags=["Customer Support"])
api_router.include_router(thought_partner.router, prefix="/thought-partner", tags=["Thought Partner"]) 
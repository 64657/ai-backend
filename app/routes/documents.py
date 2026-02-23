from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

def get_document_service(db: AsyncSession = Depends(get_db)):
    repo = DocumentRepository(db)
    return DocumentService(repo)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    file_bytes = await file.read()

    return await service.upload(
        user_id=current_user.id,
        filename=file.filename,
        content=file_bytes
    )
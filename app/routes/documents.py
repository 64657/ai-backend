from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse
from app.utils.pdf_extractor import extract_text_from_pdf
from fastapi import HTTPException
from app.repositories.document_chunk_repository import DocumentChunkRepository

router = APIRouter(prefix="/documents", tags=["Documents"])

def get_document_service(db: AsyncSession = Depends(get_db)):
    repo = DocumentRepository(db)
    chunk_repo = DocumentChunkRepository(db)
    return DocumentService(repo, chunk_repo)

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

@router.get("/{doc_id}/text")
async def get_document_text(
    doc_id: int,
    current_user = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    document = await service.repo.get_by_id(doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Allowed")
    
    text = extract_text_from_pdf(document.content)

    return {
        "document_id": doc_id,
        "extracted_text": text
    }

@router.post("/{doc_id}/process")
async def process_document(
    doc_id: int,
    current_user = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    document = await service.repo.get_by_id(doc_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Allowed")

    result = await service.process_document(doc_id)

    return result

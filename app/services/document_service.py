from app.repositories.document_repository import DocumentRepository
from app.models.document import Document

class DocumentService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    async def upload(self,user_id: int, filename: str, content: bytes) -> Document:
        return await self.repo.create(
            user_id=user_id,
            filename=filename,
            content=content
        )
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_chunk import DocumentChunk
from sqlalchemy import select

class DocumentChunkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, document_id: int, content: str, embedding: list[float]):
        chunk = DocumentChunk(
            document_id=document_id,
            content=content,
            embedding=embedding
        )
        self.db.add(chunk)
        await self.db.commit()
        await self.db.refresh(chunk)
        return chunk

    async def get_by_document(self, document_id: int):
        result = await self.db.execute(
            select(DocumentChunk).where(
                DocumentChunk.document_id == document_id
            )
        )
        return result.scalars().all()
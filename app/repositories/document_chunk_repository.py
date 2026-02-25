from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_chunk import DocumentChunk

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
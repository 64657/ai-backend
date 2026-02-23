from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document

class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: int, filename: str, content: str):
        doc = Document(
            user_id=user_id,
            filename=filename,
            content=content
        )
        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc
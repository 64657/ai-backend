import asyncio
import sys

sys.path.append(".")


from app.db.session import engine
from app.models.user import Base
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


async def create_tables():
    async with engine.begin() as conn:
        # print("Cleaning up old tables...")
        # await conn.run_sync(Base.metadata.drop_all)

        print("Creating new tables (including 'bytea' columns)..")
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
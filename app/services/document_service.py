from app.repositories.document_repository import DocumentRepository
from app.models.document import Document
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.text_splitter import split_text
from app.utils.embedding import generate_embedding

class DocumentService:
    def __init__(self, repo: DocumentRepository, chunk_repo):
        self.repo = repo
        self.chunk_repo = chunk_repo

    async def upload(self,user_id: int, filename: str, content: bytes) -> Document:
        return await self.repo.create(
            user_id=user_id,
            filename=filename,
            content=content
        )

    async def process_document(self, doc_id:int):
        document = await self.repo.get_by_id(doc_id)

        if not document:
            return None

        text = extract_text_from_pdf(document.content)

        chunks = split_text(text)

        for chunk in chunks:
            embedding = generate_embedding(chunk)
            await self.chunk_repo.create(
                document_id=doc_id,
                content=chunk,
                embedding=embedding
            )

        return {"status": "processed", "chunks": len(chunks)}

        
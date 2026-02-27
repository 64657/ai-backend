from app.repositories.document_repository import DocumentRepository
from app.models.document import Document
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.text_splitter import split_text
from app.utils.embedding import generate_embedding
from app.utils.similarity import cosine_similarity
from app.utils.llm import generate_answer

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

    # async def ask(self, doc_id: int, question: str):
    #     chunks = await self.chunk_repo.get_by_document(doc_id)

    #     if not chunks:
    #         return {"error": "Document not processed"}

    #     question_embedding = generate_embedding(question)

    #     scored_chunks = []

    #     for chunk in chunks:
    #         score = cosine_similarity(
    #             question_embedding,
    #             chunk.embedding
    #         )
    #         scored_chunks.append((score, chunk.content))

    #     scored_chunks.sort(reverse=True, key=lambda x: x[0])

    #     top_chunks = scored_chunks[:3]

    #     return {
    #         "question": question,
    #         "top_matches": [
    #             {"score": float(score), "content": content}
    #             for score, content in top_chunks
    #         ]
    #     }

    from app.utils.llm import generate_answer

    async def ask(self, doc_id: int, question: str):
        question_embedding = generate_embedding(question)

        chunks = await self.chunk_repo.get_by_document(doc_id)

        if not chunks:
            return {"error": "Document not processed"}

        question_embedding = generate_embedding(question)

        scored_chunks = []

        for chunk in chunks:
            score = cosine_similarity(
                question_embedding,
                chunk.embedding
            )
            scored_chunks.append((score, chunk.content))

        scored_chunks.sort(reverse=True, key=lambda x: x[0])

        top_chunks = scored_chunks[:3]

        context = "\n\n".join([content for _, content in top_chunks])

        prompt = f"""
    You are an AI assistant answering questions from a document.

    Context:
    {context}

    Question:
    {question}

    Answer clearly and concisely based only on the context.
    """

        answer = await generate_answer(prompt)

        return {
            "question": question,
            "answer": answer
        }

        
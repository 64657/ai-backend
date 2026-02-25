from sqlalchemy import Column, Integer, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY
from app.models.user import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    content = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
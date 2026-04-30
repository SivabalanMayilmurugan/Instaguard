from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from database import Base


class PostResult(Base):
    __tablename__ = "post_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)

    post_index = Column(Integer, nullable=False)
    instagram_post_url = Column(String(512), nullable=True)
    image_url = Column(String(512), nullable=True)   # original CDN url (for display only, not stored)
    thumbnail_b64 = Column(Text, nullable=True)      # small base64 thumbnail stored in DB for display

    is_suspicious = Column(Boolean, nullable=False)
    confidence_score = Column(Float, nullable=False)   # 0.0 – 1.0
    scan_duration_ms = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    scan = relationship("Scan", back_populates="results")

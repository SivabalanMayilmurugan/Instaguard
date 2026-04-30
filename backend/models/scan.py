from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime, timezone
from database import Base


class ScanStatus(str, enum.Enum):
    PENDING = "pending"
    SCRAPING = "scraping"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instagram_username = Column(String(255), nullable=False, index=True)
    status = Column(SAEnum(ScanStatus), default=ScanStatus.PENDING, nullable=False)
    celery_task_id = Column(String(255), nullable=True)

    # FIX: added max_posts column — was missing, causing task to crash on scan.max_posts
    max_posts = Column(Integer, default=50, nullable=False)

    total_posts = Column(Integer, default=0)
    analyzed_posts = Column(Integer, default=0)   # images only (videos skipped)
    suspicious_count = Column(Integer, default=0)
    clean_count = Column(Integer, default=0)
    avg_scan_duration_ms = Column(Float, default=0.0)

    error_message = Column(String(1024), nullable=True)
      # Chain of Custody — SHA-256 of the canonical report payload
    # Set once when the scan completes and never mutated.
    report_hash = Column(String(64), nullable=True, index=True)
    # SHA-256 of the exported PDF bytes (set on first export)
    pdf_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="scans")
    results = relationship(
        "PostResult",
        back_populates="scan",
        cascade="all, delete-orphan",
        order_by="PostResult.post_index",
    )
   
    
  
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    goal = Column(String, nullable=True)
    scheduled_duration = Column(Integer, nullable=False)  # minutes
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(
        String,
        CheckConstraint("status IN ('scheduled','active','paused','completed','interrupted','abandoned','overdue')"),
        default="scheduled"
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    interruptions = relationship("Interruption", back_populates="session", cascade="all, delete-orphan")

    @property
    def pause_count(self):
        return len(self.interruptions)

    @property
    def last_interruption(self):
        if not self.interruptions:
            return None
        return max(self.interruptions, key=lambda x: x.pause_time)


class Interruption(Base):
    __tablename__ = "interruptions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    reason = Column(String, nullable=False)
    pause_time = Column(DateTime, default=datetime.utcnow)
    resume_time = Column(DateTime, nullable=True)

    session = relationship("Session", back_populates="interruptions")

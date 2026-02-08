from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    goal: Optional[str] = None
    duration_minutes: int = Field(..., gt=0, le=480)  # max 8 hours


class PauseRequest(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500)


class InterruptionResponse(BaseModel):
    id: int
    reason: str
    pause_time: datetime
    resume_time: Optional[datetime]

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    id: int
    title: str
    goal: Optional[str]
    scheduled_duration: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str
    created_at: datetime
    pause_count: int
    actual_duration_minutes: Optional[float]
    interruptions: List[InterruptionResponse] = []

    class Config:
        from_attributes = True


class SessionListItem(BaseModel):
    id: int
    title: str
    scheduled_duration: int
    status: str
    pause_count: int
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    actual_duration_minutes: Optional[float]

    class Config:
        from_attributes = True

from sqlalchemy.orm import Session as DbSession
from datetime import datetime
from typing import Optional

from models import Session, Interruption
from schemas import SessionCreate


def create_session(db: DbSession, data: SessionCreate) -> Session:
    session = Session(
        title=data.title,
        goal=data.goal,
        scheduled_duration=data.duration_minutes
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: DbSession, session_id: int) -> Optional[Session]:
    return db.query(Session).filter(Session.id == session_id).first()


def get_all_sessions(db: DbSession) -> list[Session]:
    return db.query(Session).order_by(Session.created_at.desc()).all()


def start_session(db: DbSession, session: Session) -> Session:
    if session.status != "scheduled":
        raise ValueError(f"Cannot start session in '{session.status}' state")
    
    session.status = "active"
    session.start_time = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


def pause_session(db: DbSession, session: Session, reason: str) -> Session:
    if session.status != "active":
        raise ValueError(f"Cannot pause session in '{session.status}' state")
    
    session.status = "paused"
    interruption = Interruption(session_id=session.id, reason=reason)
    db.add(interruption)
    db.commit()
    db.refresh(session)
    return session


def resume_session(db: DbSession, session: Session) -> Session:
    if session.status != "paused":
        raise ValueError(f"Cannot resume session in '{session.status}' state")
    
    session.status = "active"
    # mark the last interruption as resumed
    last_int = session.last_interruption
    if last_int:
        last_int.resume_time = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


def complete_session(db: DbSession, session: Session) -> Session:
    if session.status not in ("active", "paused"):
        raise ValueError(f"Cannot complete session in '{session.status}' state")
    
    session.end_time = datetime.utcnow()
    session.status = _calculate_final_status(session)
    db.commit()
    db.refresh(session)
    return session


def _calculate_final_status(session: Session) -> str:
    """
    Status rules:
    - 4+ pauses -> interrupted
    - Last pause never resumed -> abandoned
    - Actual time > scheduled + 10% -> overdue
    - Otherwise -> completed
    """
    pause_count = session.pause_count
    
    # check if abandoned (paused and never resumed)
    if session.status == "paused":
        last_int = session.last_interruption
        if last_int and last_int.resume_time is None:
            return "abandoned"
    
    # too many interruptions
    if pause_count >= 4:
        return "interrupted"
    
    # check for overdue
    if session.start_time and session.end_time:
        actual_minutes = calc_actual_duration(session)
        threshold = session.scheduled_duration * 1.1
        if actual_minutes > threshold:
            return "overdue"
    
    return "completed"


def calc_actual_duration(session: Session) -> float:
    """Calculate actual working time, excluding pause durations."""
    if not session.start_time:
        return 0.0
    
    end = session.end_time or datetime.utcnow()
    total_seconds = (end - session.start_time).total_seconds()
    
    # subtract pause durations
    for interruption in session.interruptions:
        resume = interruption.resume_time or end
        pause_seconds = (resume - interruption.pause_time).total_seconds()
        total_seconds -= pause_seconds
    
    return max(total_seconds / 60, 0)


def session_to_response(session: Session) -> dict:
    """Convert session to response dict with computed fields."""
    return {
        "id": session.id,
        "title": session.title,
        "goal": session.goal,
        "scheduled_duration": session.scheduled_duration,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "status": session.status,
        "created_at": session.created_at,
        "pause_count": session.pause_count,
        "actual_duration_minutes": calc_actual_duration(session) if session.start_time else None,
        "interruptions": [
            {
                "id": i.id,
                "reason": i.reason,
                "pause_time": i.pause_time,
                "resume_time": i.resume_time
            }
            for i in session.interruptions
        ]
    }


def session_to_list_item(session: Session) -> dict:
    return {
        "id": session.id,
        "title": session.title,
        "scheduled_duration": session.scheduled_duration,
        "status": session.status,
        "pause_count": session.pause_count,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "actual_duration_minutes": calc_actual_duration(session) if session.start_time else None
    }

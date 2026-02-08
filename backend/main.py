from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DbSession

from database import engine, get_db, Base
from schemas import SessionCreate, PauseRequest, SessionResponse, SessionListItem
import crud

# create tables if they don't exist (for development)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Deep Work Session Tracker",
    version="1.0.0",
    description="Track and manage deep work sessions with interruption logging"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sessions/", response_model=SessionResponse)
def create_session(data: SessionCreate, db: DbSession = Depends(get_db)):
    session = crud.create_session(db, data)
    return crud.session_to_response(session)


@app.get("/sessions/history", response_model=list[SessionListItem])
def get_history(db: DbSession = Depends(get_db)):
    sessions = crud.get_all_sessions(db)
    return [crud.session_to_list_item(s) for s in sessions]


@app.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: DbSession = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return crud.session_to_response(session)


@app.patch("/sessions/{session_id}/start", response_model=SessionResponse)
def start_session(session_id: int, db: DbSession = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        session = crud.start_session(db, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return crud.session_to_response(session)


@app.patch("/sessions/{session_id}/pause", response_model=SessionResponse)
def pause_session(session_id: int, data: PauseRequest, db: DbSession = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        session = crud.pause_session(db, session, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return crud.session_to_response(session)


@app.patch("/sessions/{session_id}/resume", response_model=SessionResponse)
def resume_session(session_id: int, db: DbSession = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        session = crud.resume_session(db, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return crud.session_to_response(session)


@app.patch("/sessions/{session_id}/complete", response_model=SessionResponse)
def complete_session(session_id: int, db: DbSession = Depends(get_db)):
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    try:
        session = crud.complete_session(db, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return crud.session_to_response(session)

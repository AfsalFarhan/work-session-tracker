import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import Session, Interruption


# test db setup
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestSessionCreation:
    def test_create_session(self):
        resp = client.post("/sessions/", json={
            "title": "Deep work",
            "goal": "Finish feature",
            "duration_minutes": 45
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Deep work"
        assert data["status"] == "scheduled"
        assert data["pause_count"] == 0

    def test_create_session_without_goal(self):
        resp = client.post("/sessions/", json={
            "title": "Quick task",
            "duration_minutes": 25
        })
        assert resp.status_code == 200
        assert resp.json()["goal"] is None


class TestStateTransitions:
    def test_start_session(self):
        # create then start
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": 30})
        sid = resp.json()["id"]
        
        resp = client.patch(f"/sessions/{sid}/start")
        assert resp.status_code == 200
        assert resp.json()["status"] == "active"
        assert resp.json()["start_time"] is not None

    def test_cannot_start_twice(self):
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": 30})
        sid = resp.json()["id"]
        
        client.patch(f"/sessions/{sid}/start")
        resp = client.patch(f"/sessions/{sid}/start")
        assert resp.status_code == 400
        assert "Cannot start session" in resp.json()["detail"]

    def test_pause_requires_active(self):
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": 30})
        sid = resp.json()["id"]
        
        # try to pause without starting
        resp = client.patch(f"/sessions/{sid}/pause", json={"reason": "break"})
        assert resp.status_code == 400

    def test_pause_requires_reason(self):
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": 30})
        sid = resp.json()["id"]
        client.patch(f"/sessions/{sid}/start")
        
        resp = client.patch(f"/sessions/{sid}/pause", json={})
        assert resp.status_code == 422  # validation error

    def test_resume_requires_paused(self):
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": 30})
        sid = resp.json()["id"]
        client.patch(f"/sessions/{sid}/start")
        
        resp = client.patch(f"/sessions/{sid}/resume")
        assert resp.status_code == 400

    def test_full_workflow(self):
        # create -> start -> pause -> resume -> complete
        resp = client.post("/sessions/", json={"title": "Full workflow", "duration_minutes": 30})
        sid = resp.json()["id"]
        
        client.patch(f"/sessions/{sid}/start")
        client.patch(f"/sessions/{sid}/pause", json={"reason": "coffee"})
        client.patch(f"/sessions/{sid}/resume")
        resp = client.patch(f"/sessions/{sid}/complete")
        
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"
        assert resp.json()["pause_count"] == 1


class TestStatusCalculation:
    def _create_and_start(self, duration=30):
        resp = client.post("/sessions/", json={"title": "Test", "duration_minutes": duration})
        sid = resp.json()["id"]
        client.patch(f"/sessions/{sid}/start")
        return sid

    def test_interrupted_after_four_pauses(self):
        sid = self._create_and_start()
        
        for i in range(4):
            client.patch(f"/sessions/{sid}/pause", json={"reason": f"pause {i+1}"})
            client.patch(f"/sessions/{sid}/resume")
        
        resp = client.patch(f"/sessions/{sid}/complete")
        assert resp.json()["status"] == "interrupted"
        assert resp.json()["pause_count"] == 4

    def test_abandoned_when_not_resumed(self):
        sid = self._create_and_start()
        client.patch(f"/sessions/{sid}/pause", json={"reason": "got distracted"})
        # complete while paused, never resumed
        resp = client.patch(f"/sessions/{sid}/complete")
        assert resp.json()["status"] == "abandoned"

    def test_overdue_detection(self):
        # this is tricky to test without mocking time
        # we'll test the logic via direct db manipulation
        db = TestSession()
        
        session = Session(
            title="Overdue test",
            scheduled_duration=10,  # 10 minutes
            status="active",
            start_time=datetime.utcnow() - timedelta(minutes=15)  # 15 min ago (>10% over)
        )
        db.add(session)
        db.commit()
        
        resp = client.patch(f"/sessions/{session.id}/complete")
        assert resp.json()["status"] == "overdue"
        db.close()

    def test_normal_completion(self):
        db = TestSession()
        
        session = Session(
            title="Normal test",
            scheduled_duration=30,
            status="active",
            start_time=datetime.utcnow() - timedelta(minutes=25)  # within time
        )
        db.add(session)
        db.commit()
        
        resp = client.patch(f"/sessions/{session.id}/complete")
        assert resp.json()["status"] == "completed"
        db.close()


class TestHistory:
    def test_get_history(self):
        # create a few sessions
        client.post("/sessions/", json={"title": "Session 1", "duration_minutes": 30})
        client.post("/sessions/", json={"title": "Session 2", "duration_minutes": 45})
        
        resp = client.get("/sessions/history")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_history_ordering(self):
        client.post("/sessions/", json={"title": "First", "duration_minutes": 30})
        client.post("/sessions/", json={"title": "Second", "duration_minutes": 30})
        
        resp = client.get("/sessions/history")
        # should be newest first
        assert resp.json()[0]["title"] == "Second"

import { useState, useEffect, useCallback } from 'react';
import SessionForm from './components/SessionForm';
import SessionControl from './components/SessionControl';
import SessionHistory from './components/SessionHistory';
import {
    createSession,
    getHistory,
    getSession,
    startSession,
    pauseSession,
    resumeSession,
    completeSession
} from './api';

export default function App() {
    const [sessions, setSessions] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchHistory = useCallback(async () => {
        try {
            const { data } = await getHistory();
            setSessions(data);

            // find any active/paused/scheduled session
            const current = data.find(s => ['active', 'paused', 'scheduled'].includes(s.status));
            if (current) {
                const { data: full } = await getSession(current.id);
                setActiveSession(full);
            } else {
                setActiveSession(null);
            }
            setError(null);
        } catch (err) {
            setError('Failed to load sessions. Is the backend running?');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchHistory();
    }, [fetchHistory]);

    const handleCreate = async (data) => {
        try {
            const { data: session } = await createSession(data);
            setActiveSession(session);
            await fetchHistory();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create session');
        }
    };

    const handleStart = async () => {
        try {
            const { data } = await startSession(activeSession.id);
            setActiveSession(data);
            await fetchHistory();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to start session');
        }
    };

    const handlePause = async (reason) => {
        try {
            const { data } = await pauseSession(activeSession.id, reason);
            setActiveSession(data);
            await fetchHistory();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to pause session');
        }
    };

    const handleResume = async () => {
        try {
            const { data } = await resumeSession(activeSession.id);
            setActiveSession(data);
            await fetchHistory();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to resume session');
        }
    };

    const handleComplete = async () => {
        try {
            await completeSession(activeSession.id);
            setActiveSession(null);
            await fetchHistory();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to complete session');
        }
    };

    const handleSelectSession = async (session) => {
        try {
            const { data } = await getSession(session.id);
            setActiveSession(data);
        } catch (err) {
            setError('Failed to load session');
        }
    };

    if (loading) {
        return <div className="app loading">Loading...</div>;
    }

    return (
        <div className="app">
            <header>
                <h1>Deep Work Tracker</h1>
                <p className="tagline">Focus. Track. Improve.</p>
            </header>

            {error && (
                <div className="error-banner">
                    {error}
                    <button onClick={() => setError(null)}>×</button>
                </div>
            )}

            <main>
                <div className="left-panel">
                    <SessionForm
                        onSubmit={handleCreate}
                        disabled={activeSession && ['active', 'paused'].includes(activeSession.status)}
                    />
                    <SessionControl
                        session={activeSession}
                        onStart={handleStart}
                        onPause={handlePause}
                        onResume={handleResume}
                        onComplete={handleComplete}
                    />
                </div>
                <div className="right-panel">
                    <SessionHistory
                        sessions={sessions}
                        onSelectSession={handleSelectSession}
                    />
                </div>
            </main>
        </div>
    );
}

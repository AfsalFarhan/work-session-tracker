import { useState, useEffect, useRef } from 'react';

export default function SessionControl({ session, onStart, onPause, onResume, onComplete }) {
    const [pauseReason, setPauseReason] = useState('');
    const [showPauseInput, setShowPauseInput] = useState(false);
    const [elapsed, setElapsed] = useState(0);
    const timerRef = useRef(null);

    useEffect(() => {
        if (session?.status === 'active' && session?.start_time) {
            const startTime = new Date(session.start_time).getTime();

            const tick = () => {
                const now = Date.now();
                setElapsed(Math.floor((now - startTime) / 1000));
            };

            tick();
            timerRef.current = setInterval(tick, 1000);

            return () => clearInterval(timerRef.current);
        } else {
            clearInterval(timerRef.current);
        }
    }, [session?.status, session?.start_time]);

    if (!session) {
        return (
            <div className="session-control empty">
                <p>No active session. Schedule one to get started.</p>
            </div>
        );
    }

    const formatTime = (secs) => {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    };

    const handlePauseClick = () => {
        setShowPauseInput(true);
    };

    const handlePauseSubmit = () => {
        if (pauseReason.trim()) {
            onPause(pauseReason.trim());
            setPauseReason('');
            setShowPauseInput(false);
        }
    };

    const remaining = Math.max(0, session.scheduled_duration * 60 - elapsed);
    const isOvertime = remaining === 0 && session.status === 'active';

    return (
        <div className={`session-control ${session.status}`}>
            <div className="session-info">
                <h2>{session.title}</h2>
                {session.goal && <p className="goal">{session.goal}</p>}
                <span className={`status-badge ${session.status}`}>{session.status}</span>
            </div>

            {session.status === 'active' && (
                <div className={`timer ${isOvertime ? 'overtime' : ''}`}>
                    <span className="timer-label">{isOvertime ? 'Overtime' : 'Remaining'}</span>
                    <span className="timer-value">
                        {isOvertime ? `+${formatTime(elapsed - session.scheduled_duration * 60)}` : formatTime(remaining)}
                    </span>
                </div>
            )}

            <div className="controls">
                {session.status === 'scheduled' && (
                    <button className="btn-start" onClick={onStart}>Start Session</button>
                )}

                {session.status === 'active' && !showPauseInput && (
                    <>
                        <button className="btn-pause" onClick={handlePauseClick}>Pause</button>
                        <button className="btn-complete" onClick={onComplete}>Complete</button>
                    </>
                )}

                {session.status === 'active' && showPauseInput && (
                    <div className="pause-input">
                        <input
                            type="text"
                            value={pauseReason}
                            onChange={(e) => setPauseReason(e.target.value)}
                            placeholder="Why are you pausing?"
                            autoFocus
                            onKeyDown={(e) => e.key === 'Enter' && handlePauseSubmit()}
                        />
                        <button onClick={handlePauseSubmit} disabled={!pauseReason.trim()}>Confirm Pause</button>
                        <button className="btn-cancel" onClick={() => setShowPauseInput(false)}>Cancel</button>
                    </div>
                )}

                {session.status === 'paused' && (
                    <>
                        <button className="btn-resume" onClick={onResume}>Resume</button>
                        <button className="btn-complete" onClick={onComplete}>Complete Anyway</button>
                    </>
                )}
            </div>

            {session.pause_count > 0 && (
                <div className="pause-count">
                    Paused {session.pause_count} time{session.pause_count > 1 ? 's' : ''}
                    {session.pause_count >= 4 && <span className="warning"> (will be marked interrupted)</span>}
                </div>
            )}
        </div>
    );
}

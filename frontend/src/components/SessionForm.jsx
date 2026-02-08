import { useState } from 'react';

export default function SessionForm({ onSubmit, disabled }) {
    const [title, setTitle] = useState('');
    const [goal, setGoal] = useState('');
    const [duration, setDuration] = useState(25);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!title.trim()) return;

        onSubmit({
            title: title.trim(),
            goal: goal.trim() || null,
            duration_minutes: duration
        });

        setTitle('');
        setGoal('');
        setDuration(25);
    };

    return (
        <form onSubmit={handleSubmit} className="session-form">
            <h2>Schedule Session</h2>
            <div className="form-group">
                <label htmlFor="title">What are you working on?</label>
                <input
                    id="title"
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g., API refactoring"
                    required
                    disabled={disabled}
                />
            </div>
            <div className="form-group">
                <label htmlFor="goal">Goal (optional)</label>
                <input
                    id="goal"
                    type="text"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="e.g., Complete endpoints for user auth"
                    disabled={disabled}
                />
            </div>
            <div className="form-group">
                <label htmlFor="duration">Duration (minutes)</label>
                <select
                    id="duration"
                    value={duration}
                    onChange={(e) => setDuration(Number(e.target.value))}
                    disabled={disabled}
                >
                    <option value={15}>15 min</option>
                    <option value={25}>25 min (Pomodoro)</option>
                    <option value={45}>45 min</option>
                    <option value={60}>1 hour</option>
                    <option value={90}>1.5 hours</option>
                    <option value={120}>2 hours</option>
                </select>
            </div>
            <button type="submit" disabled={disabled || !title.trim()}>
                Schedule Session
            </button>
        </form>
    );
}

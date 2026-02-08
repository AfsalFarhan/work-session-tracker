const STATUS_LABELS = {
    scheduled: 'Scheduled',
    active: 'Active',
    paused: 'Paused',
    completed: 'Completed',
    interrupted: 'Interrupted',
    abandoned: 'Abandoned',
    overdue: 'Overdue'
};

export default function SessionHistory({ sessions, onSelectSession }) {
    const formatDuration = (mins) => {
        if (mins < 60) return `${Math.round(mins)}m`;
        const h = Math.floor(mins / 60);
        const m = Math.round(mins % 60);
        return m > 0 ? `${h}h ${m}m` : `${h}h`;
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return '-';
        const d = new Date(dateStr);
        const now = new Date();
        const diff = now - d;

        if (diff < 86400000) { // today
            return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else if (diff < 172800000) { // yesterday
            return 'Yesterday';
        }
        return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
    };

    if (sessions.length === 0) {
        return (
            <div className="session-history empty">
                <p>No sessions yet. Create your first deep work session!</p>
            </div>
        );
    }

    return (
        <div className="session-history">
            <h2>Session History</h2>
            <table>
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Duration</th>
                        <th>Actual</th>
                        <th>Status</th>
                        <th>Pauses</th>
                        <th>When</th>
                    </tr>
                </thead>
                <tbody>
                    {sessions.map(s => (
                        <tr
                            key={s.id}
                            className={`status-${s.status}`}
                            onClick={() => ['scheduled', 'active', 'paused'].includes(s.status) && onSelectSession(s)}
                            style={{ cursor: ['scheduled', 'active', 'paused'].includes(s.status) ? 'pointer' : 'default' }}
                        >
                            <td className="title">{s.title}</td>
                            <td>{formatDuration(s.scheduled_duration)}</td>
                            <td>{s.actual_duration_minutes ? formatDuration(s.actual_duration_minutes) : '-'}</td>
                            <td>
                                <span className={`status-badge ${s.status}`}>
                                    {STATUS_LABELS[s.status] || s.status}
                                </span>
                            </td>
                            <td>{s.pause_count}</td>
                            <td>{formatDate(s.start_time || s.created_at)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

-- Seed data for Deep Work Session Tracker
-- Run this after migrations to populate test data

-- Completed session (normal)
INSERT INTO sessions (title, goal, scheduled_duration, start_time, end_time, status, created_at)
VALUES ('API Design Review', 'Review and finalize REST API endpoints', 45, 
        datetime('now', '-3 days', '-50 minutes'), datetime('now', '-3 days'), 'completed',
        datetime('now', '-3 days', '-1 hour'));

-- Completed session with one pause
INSERT INTO sessions (id, title, goal, scheduled_duration, start_time, end_time, status, created_at)
VALUES (2, 'Database Schema Planning', 'Design normalized schema for user data', 60,
        datetime('now', '-2 days', '-70 minutes'), datetime('now', '-2 days'), 'completed',
        datetime('now', '-2 days', '-2 hours'));

INSERT INTO interruptions (session_id, reason, pause_time, resume_time)
VALUES (2, 'Quick standup meeting', datetime('now', '-2 days', '-40 minutes'), datetime('now', '-2 days', '-35 minutes'));

-- Interrupted session (4+ pauses)
INSERT INTO sessions (id, title, goal, scheduled_duration, start_time, end_time, status, created_at)
VALUES (3, 'Frontend Component Refactor', 'Refactor form components to use hooks', 90,
        datetime('now', '-1 day', '-100 minutes'), datetime('now', '-1 day'), 'interrupted',
        datetime('now', '-1 day', '-2 hours'));

INSERT INTO interruptions (session_id, reason, pause_time, resume_time) VALUES 
(3, 'Slack notification', datetime('now', '-1 day', '-90 minutes'), datetime('now', '-1 day', '-88 minutes')),
(3, 'Coffee break', datetime('now', '-1 day', '-70 minutes'), datetime('now', '-1 day', '-60 minutes')),
(3, 'Phone call', datetime('now', '-1 day', '-45 minutes'), datetime('now', '-1 day', '-40 minutes')),
(3, 'Email notification', datetime('now', '-1 day', '-20 minutes'), datetime('now', '-1 day', '-18 minutes'));

-- Overdue session (took >10% longer)
INSERT INTO sessions (id, title, goal, scheduled_duration, start_time, end_time, status, created_at)
VALUES (4, 'Code Review', 'Review PR #234', 30,
        datetime('now', '-12 hours', '-45 minutes'), datetime('now', '-12 hours'), 'overdue',
        datetime('now', '-12 hours', '-1 hour'));

-- Abandoned session (paused and never resumed)
INSERT INTO sessions (id, title, goal, scheduled_duration, start_time, end_time, status, created_at)
VALUES (5, 'Documentation Writing', 'Write API docs for auth endpoints', 60,
        datetime('now', '-6 hours', '-30 minutes'), datetime('now', '-6 hours'), 'abandoned',
        datetime('now', '-6 hours', '-1 hour'));

INSERT INTO interruptions (session_id, reason, pause_time, resume_time)
VALUES (5, 'Lunch break - got sidetracked', datetime('now', '-6 hours', '-20 minutes'), NULL);

-- Scheduled session (not started yet)
INSERT INTO sessions (title, goal, scheduled_duration, status, created_at)
VALUES ('Unit Test Coverage', 'Improve test coverage for auth module', 45, 'scheduled', datetime('now', '-1 hour'));

-- Active session 
INSERT INTO sessions (title, goal, scheduled_duration, start_time, status, created_at)
VALUES ('Bug Investigation', 'Debug memory leak in worker process', 60, datetime('now', '-15 minutes'), 'active', datetime('now', '-20 minutes'));

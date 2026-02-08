"""Initial migration - sessions and interruptions tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-15
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('goal', sa.String(), nullable=True),
        sa.Column('scheduled_duration', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), server_default='scheduled'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.CheckConstraint(
            "status IN ('scheduled','active','paused','completed','interrupted','abandoned','overdue')",
            name='valid_status'
        )
    )

    op.create_table(
        'interruptions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('pause_time', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('resume_time', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_interruptions_session_id', 'interruptions', ['session_id'])


def downgrade() -> None:
    op.drop_table('interruptions')
    op.drop_table('sessions')

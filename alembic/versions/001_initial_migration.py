"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-01-14 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite doesn't support ENUMs, so we'll use String with constraints

    # Create students table
    op.create_table('students',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('telegram_user_id', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('course_program_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_telegram_user_id'), 'students', ['telegram_user_id'], unique=True)

    # Create course_programs table
    op.create_table('course_programs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_programs_id'), 'course_programs', ['id'], unique=False)

    # Create streams table
    op.create_table('streams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_streams_id'), 'streams', ['id'], unique=False)

    # Create modules table
    op.create_table('modules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('order_num', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_modules_id'), 'modules', ['id'], unique=False)

    # Create lessons table
    op.create_table('lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('module_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('order_num', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)

    # Create course_materials table
    op.create_table('course_materials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('material_type', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_materials_id'), 'course_materials', ['id'], unique=False)

    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('telegram_message_id', sa.Integer(), nullable=True),
        sa.Column('chat_id', sa.Integer(), nullable=True),
        sa.Column('sender_type', sa.String(length=20), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)

    # Create bot_responses table
    op.create_table('bot_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('text_content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_responses_id'), 'bot_responses', ['id'], unique=False)

    # Create assignments table
    op.create_table('assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('is_intermediate_attestation', sa.Boolean(), nullable=True),
        sa.Column('is_final_attestation', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignments_id'), 'assignments', ['id'], unique=False)

    # Create schedule table
    op.create_table('schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False),
        sa.Column('lesson_type', sa.String(length=20), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_id'), 'schedule', ['id'], unique=False)

    # Create prompts table
    op.create_table('prompts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('prompt_text', sa.Text(), nullable=False),
        sa.Column('prompt_type', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prompts_id'), 'prompts', ['id'], unique=False)

    # Create students_streams association table
    op.create_table('students_streams',
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('stream_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('student_id', 'stream_id')
    )

    # Add foreign key constraints
    op.create_foreign_key(None, 'students', 'course_programs', ['course_program_id'], ['id'])
    op.create_foreign_key(None, 'streams', 'course_programs', ['program_id'], ['id'])
    op.create_foreign_key(None, 'modules', 'course_programs', ['program_id'], ['id'])
    op.create_foreign_key(None, 'lessons', 'modules', ['module_id'], ['id'])
    op.create_foreign_key(None, 'course_materials', 'lessons', ['lesson_id'], ['id'])
    op.create_foreign_key(None, 'bot_responses', 'messages', ['message_id'], ['id'])
    op.create_foreign_key(None, 'assignments', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'assignments', 'lessons', ['lesson_id'], ['id'])
    op.create_foreign_key(None, 'schedule', 'streams', ['stream_id'], ['id'])
    op.create_foreign_key(None, 'schedule', 'lessons', ['lesson_id'], ['id'])
    op.create_foreign_key(None, 'students_streams', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'students_streams', 'streams', ['stream_id'], ['id'])


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint(None, 'students_streams', type_='foreignkey')
    op.drop_constraint(None, 'students_streams', type_='foreignkey')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'assignments', type_='foreignkey')
    op.drop_constraint(None, 'assignments', type_='foreignkey')
    op.drop_constraint(None, 'bot_responses', type_='foreignkey')
    op.drop_constraint(None, 'course_materials', type_='foreignkey')
    op.drop_constraint(None, 'lessons', type_='foreignkey')
    op.drop_constraint(None, 'modules', type_='foreignkey')
    op.drop_constraint(None, 'streams', type_='foreignkey')
    op.drop_constraint(None, 'students', type_='foreignkey')

    # Drop tables
    op.drop_table('students_streams')
    op.drop_table('prompts')
    op.drop_table('schedule')
    op.drop_table('assignments')
    op.drop_table('bot_responses')
    op.drop_table('messages')
    op.drop_table('course_materials')
    op.drop_table('lessons')
    op.drop_table('modules')
    op.drop_table('streams')
    op.drop_table('course_programs')
    op.drop_table('students')

    # SQLite doesn't have ENUMs to drop

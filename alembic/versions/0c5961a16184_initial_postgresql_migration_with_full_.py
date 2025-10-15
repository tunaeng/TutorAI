"""Initial PostgreSQL migration with full schema

Revision ID: 0c5961a16184
Revises: 
Create Date: 2025-10-15 18:07:19.153010

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0c5961a16184'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types
    materialcategory = postgresql.ENUM('lecture', 'assignment', 'methodical', name='materialcategory')
    materialcategory.create(op.get_bind())
    
    sendertype = postgresql.ENUM('user', 'bot', name='sendertype')
    sendertype.create(op.get_bind())
    
    assignmentstatus = postgresql.ENUM('pending', 'submitted', 'checked', 'completed', name='assignmentstatus')
    assignmentstatus.create(op.get_bind())
    
    meetingtype = postgresql.ENUM('lecture', 'practice', 'independent', name='meetingtype')
    meetingtype.create(op.get_bind())

    # Create students table
    op.create_table('students',
        sa.Column('student_id', sa.BigInteger(), nullable=False),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('telegram_user_id', sa.BigInteger(), nullable=True),
        sa.Column('telegram_username', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('course_program_id', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('student_id'),
        sa.CheckConstraint("phone ~ '^\\+7\\d{10}$'", name='check_phone_format')
    )
    op.create_index(op.f('ix_students_student_id'), 'students', ['student_id'], unique=False)
    op.create_index('idx_students_phone', 'students', ['phone'], unique=False)
    op.create_index('idx_students_telegram_user_id', 'students', ['telegram_user_id'], unique=False)

    # Create course_programs table
    op.create_table('course_programs',
        sa.Column('program_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('total_hours', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('program_id')
    )
    op.create_index(op.f('ix_course_programs_program_id'), 'course_programs', ['program_id'], unique=False)

    # Create streams table
    op.create_table('streams',
        sa.Column('stream_id', sa.BigInteger(), nullable=False),
        sa.Column('program_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('stream_id')
    )
    op.create_index(op.f('ix_streams_stream_id'), 'streams', ['stream_id'], unique=False)
    op.create_index('idx_modules_program_id', 'streams', ['program_id'], unique=False)

    # Create modules table
    op.create_table('modules',
        sa.Column('module_id', sa.BigInteger(), nullable=False),
        sa.Column('program_id', sa.BigInteger(), nullable=False),
        sa.Column('order_num', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_hours', sa.Integer(), nullable=False),
        sa.Column('lecture_hours', sa.Integer(), nullable=True),
        sa.Column('practice_hours', sa.Integer(), nullable=True),
        sa.Column('independent_hours', sa.Integer(), nullable=True),
        sa.Column('is_intermediate_attestation', sa.Boolean(), nullable=True),
        sa.Column('is_final_attestation', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('module_id')
    )
    op.create_index(op.f('ix_modules_module_id'), 'modules', ['module_id'], unique=False)
    op.create_index('idx_modules_program_id', 'modules', ['program_id'], unique=False)

    # Create lessons table
    op.create_table('lessons',
        sa.Column('lesson_id', sa.BigInteger(), nullable=False),
        sa.Column('module_id', sa.BigInteger(), nullable=False),
        sa.Column('order_num', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_hours', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('lesson_id')
    )
    op.create_index(op.f('ix_lessons_lesson_id'), 'lessons', ['lesson_id'], unique=False)
    op.create_index('idx_lessons_module_id', 'lessons', ['module_id'], unique=False)

    # Create course_materials table
    op.create_table('course_materials',
        sa.Column('material_id', sa.BigInteger(), nullable=False),
        sa.Column('lesson_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('material_type', sa.String(length=50), nullable=True),
        sa.Column('material_category', materialcategory, nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('material_id')
    )
    op.create_index(op.f('ix_course_materials_material_id'), 'course_materials', ['material_id'], unique=False)
    op.create_index('idx_course_materials_lesson_id', 'course_materials', ['lesson_id'], unique=False)

    # Create messages table
    op.create_table('messages',
        sa.Column('message_id', sa.BigInteger(), nullable=False),
        sa.Column('telegram_message_id', sa.BigInteger(), nullable=True),
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('sender_type', sendertype, nullable=False),
        sa.Column('sender_id', sa.BigInteger(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('attachment_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('message_id')
    )
    op.create_index(op.f('ix_messages_message_id'), 'messages', ['message_id'], unique=False)
    op.create_index('idx_messages_chat_id', 'messages', ['chat_id'], unique=False)
    op.create_index('idx_messages_telegram_message_id', 'messages', ['telegram_message_id'], unique=False)

    # Create bot_responses table
    op.create_table('bot_responses',
        sa.Column('response_id', sa.BigInteger(), nullable=False),
        sa.Column('message_id', sa.BigInteger(), nullable=False),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('attachment_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('response_id')
    )
    op.create_index(op.f('ix_bot_responses_response_id'), 'bot_responses', ['response_id'], unique=False)

    # Create meetings table
    op.create_table('meetings',
        sa.Column('meeting_id', sa.BigInteger(), nullable=False),
        sa.Column('stream_id', sa.BigInteger(), nullable=False),
        sa.Column('lesson_id', sa.BigInteger(), nullable=False),
        sa.Column('meeting_type', meetingtype, nullable=False),
        sa.Column('meeting_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('meeting_id')
    )
    op.create_index(op.f('ix_meetings_meeting_id'), 'meetings', ['meeting_id'], unique=False)
    op.create_index('idx_meetings_stream_id', 'meetings', ['stream_id'], unique=False)
    op.create_index('idx_meetings_date', 'meetings', ['meeting_date'], unique=False)

    # Create schedule table
    op.create_table('schedule',
        sa.Column('schedule_id', sa.BigInteger(), nullable=False),
        sa.Column('stream_id', sa.BigInteger(), nullable=False),
        sa.Column('lesson_id', sa.BigInteger(), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('schedule_id')
    )
    op.create_index(op.f('ix_schedule_schedule_id'), 'schedule', ['schedule_id'], unique=False)
    op.create_index('idx_schedule_stream_id', 'schedule', ['stream_id'], unique=False)

    # Create assignments table
    op.create_table('assignments',
        sa.Column('assignment_id', sa.BigInteger(), nullable=False),
        sa.Column('student_id', sa.BigInteger(), nullable=False),
        sa.Column('lesson_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', assignmentstatus, nullable=False),
        sa.Column('deadline', sa.Date(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('checked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('assignment_id')
    )
    op.create_index(op.f('ix_assignments_assignment_id'), 'assignments', ['assignment_id'], unique=False)
    op.create_index('idx_assignments_student_id', 'assignments', ['student_id'], unique=False)
    op.create_index('idx_assignments_lesson_id', 'assignments', ['lesson_id'], unique=False)

    # Create prompts table
    op.create_table('prompts',
        sa.Column('prompt_id', sa.BigInteger(), nullable=False),
        sa.Column('prompt_type', sa.String(length=50), nullable=False),
        sa.Column('prompt_text', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('prompt_id')
    )
    op.create_index(op.f('ix_prompts_prompt_id'), 'prompts', ['prompt_id'], unique=False)
    op.create_index('idx_prompts_type_active', 'prompts', ['prompt_type', 'is_active'], unique=False)

    # Create faq_responses table
    op.create_table('faq_responses',
        sa.Column('faq_id', sa.BigInteger(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('keywords', sa.Text(), nullable=True),
        sa.Column('question', sa.Text(), nullable=True),
        sa.Column('answer_text', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('faq_id')
    )
    op.create_index(op.f('ix_faq_responses_faq_id'), 'faq_responses', ['faq_id'], unique=False)

    # Create students_streams association table
    op.create_table('students_streams',
        sa.Column('student_id', sa.BigInteger(), nullable=False),
        sa.Column('stream_id', sa.BigInteger(), nullable=False),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('student_id', 'stream_id')
    )

    # Add foreign key constraints
    op.create_foreign_key('fk_students_course_program', 'students', 'course_programs', ['course_program_id'], ['program_id'])
    op.create_foreign_key(None, 'streams', 'course_programs', ['program_id'], ['program_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'modules', 'course_programs', ['program_id'], ['program_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'lessons', 'modules', ['module_id'], ['module_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'course_materials', 'lessons', ['lesson_id'], ['lesson_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'bot_responses', 'messages', ['message_id'], ['message_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'meetings', 'streams', ['stream_id'], ['stream_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'meetings', 'lessons', ['lesson_id'], ['lesson_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'schedule', 'streams', ['stream_id'], ['stream_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'schedule', 'lessons', ['lesson_id'], ['lesson_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'assignments', 'students', ['student_id'], ['student_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'assignments', 'lessons', ['lesson_id'], ['lesson_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'students_streams', 'students', ['student_id'], ['student_id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'students_streams', 'streams', ['stream_id'], ['stream_id'], ondelete='CASCADE')

    # Create triggers for auto-updating updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    op.execute("""
        CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_prompts_updated_at BEFORE UPDATE ON prompts 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_prompts_updated_at ON prompts;")
    op.execute("DROP TRIGGER IF EXISTS update_students_updated_at ON students;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
    
    # Drop foreign key constraints
    op.drop_constraint(None, 'students_streams', type_='foreignkey')
    op.drop_constraint(None, 'students_streams', type_='foreignkey')
    op.drop_constraint(None, 'assignments', type_='foreignkey')
    op.drop_constraint(None, 'assignments', type_='foreignkey')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'meetings', type_='foreignkey')
    op.drop_constraint(None, 'meetings', type_='foreignkey')
    op.drop_constraint(None, 'bot_responses', type_='foreignkey')
    op.drop_constraint(None, 'course_materials', type_='foreignkey')
    op.drop_constraint(None, 'lessons', type_='foreignkey')
    op.drop_constraint(None, 'modules', type_='foreignkey')
    op.drop_constraint(None, 'streams', type_='foreignkey')
    op.drop_constraint('fk_students_course_program', 'students', type_='foreignkey')

    # Drop tables
    op.drop_table('students_streams')
    op.drop_table('faq_responses')
    op.drop_table('prompts')
    op.drop_table('assignments')
    op.drop_table('schedule')
    op.drop_table('meetings')
    op.drop_table('bot_responses')
    op.drop_table('messages')
    op.drop_table('course_materials')
    op.drop_table('lessons')
    op.drop_table('modules')
    op.drop_table('streams')
    op.drop_table('course_programs')
    op.drop_table('students')

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS meetingtype;")
    op.execute("DROP TYPE IF EXISTS assignmentstatus;")
    op.execute("DROP TYPE IF EXISTS sendertype;")
    op.execute("DROP TYPE IF EXISTS materialcategory;")
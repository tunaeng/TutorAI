"""
SQLAlchemy models matching the TutorAI PostgreSQL schema.
"""

from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from sqlalchemy import (
    BigInteger, String, Text, Boolean, DateTime, Date, Integer,
    ForeignKey, UniqueConstraint, Index, LargeBinary, Numeric, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, deferred
from sqlalchemy.sql import func
from app.core.database import Base


# 1. PROGRAMS
class Program(Base):
    __tablename__ = "programs"
    
    program_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students: Mapped[List["Student"]] = relationship("Student", back_populates="program")
    modules: Mapped[List["CourseModule"]] = relationship("CourseModule", back_populates="program")
    materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="program")
    
    def __str__(self):
        return self.name


# 2. STUDENTS
class Student(Base):
    __tablename__ = "students"
    
    student_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    program_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('programs.program_id', ondelete='CASCADE'), nullable=False)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    telegram_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    max_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    status: Mapped[str] = mapped_column(String(50), server_default='active')
    flow_mode: Mapped[str] = mapped_column(String(50), server_default='tutor')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", back_populates="students")
    progress: Mapped[List["StudentModuleProgress"]] = relationship("StudentModuleProgress", back_populates="student", cascade="all, delete-orphan")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="student", cascade="all, delete-orphan")
    rate_limits: Mapped[List["RateLimit"]] = relationship("RateLimit", back_populates="student", cascade="all, delete-orphan")
    schedule_items: Mapped[List["ScheduleItem"]] = relationship("ScheduleItem", back_populates="student", cascade="all, delete-orphan")
    test_results: Mapped[List["TestResult"]] = relationship("TestResult", back_populates="student", cascade="all, delete-orphan")
    feedbacks: Mapped[List["Feedback"]] = relationship("Feedback", back_populates="student", cascade="all, delete-orphan")
    registration: Mapped[Optional["RegistrationProgress"]] = relationship(
        "RegistrationProgress", back_populates="student", uselist=False, cascade="all, delete-orphan"
    )
    consultant_requests: Mapped[List["ConsultantRequest"]] = relationship(
        "ConsultantRequest", back_populates="student", cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index('idx_students_telegram_user_id', 'telegram_user_id'),
        Index('idx_students_max_user_id', 'max_user_id'),
        Index('idx_students_phone', 'phone'),
        Index('idx_students_program_id', 'program_id'),
    )
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# 3. COURSE MODULES
class CourseModule(Base):
    __tablename__ = "course_modules"
    
    module_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    program_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('programs.program_id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    total_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    lecture_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    practice_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    self_study_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", back_populates="modules", lazy='selectin')
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="module", cascade="all, delete-orphan")
    materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="module", cascade="all, delete-orphan")
    progress: Mapped[List["StudentModuleProgress"]] = relationship("StudentModuleProgress", back_populates="module", cascade="all, delete-orphan")
    tests: Mapped[List["AttestationTest"]] = relationship("AttestationTest", back_populates="module", cascade="all, delete-orphan")
    
    def __str__(self):
        return self.name


# 4. TOPICS
class Topic(Base):
    __tablename__ = "topics"
    
    topic_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    lecture_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    practice_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    self_study_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_intermediate_assessment: Mapped[bool] = mapped_column(Boolean, server_default='false')
    is_final_assessment: Mapped[bool] = mapped_column(Boolean, server_default='false')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="topics", lazy='selectin')
    materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="topic", cascade="all, delete-orphan")
    
    def __str__(self):
        return self.name


# 5. COURSE MATERIALS
class CourseMaterial(Base):
    __tablename__ = "course_materials"
    
    material_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    program_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('programs.program_id', ondelete='CASCADE'), nullable=False)
    module_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=True)
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('topics.topic_id', ondelete='CASCADE'), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    external_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_data: Mapped[Optional[bytes]] = deferred(mapped_column(LargeBinary, nullable=True))
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    file_mimetype: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    material_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    order_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, server_default='false')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", back_populates="materials", lazy='selectin')
    module: Mapped[Optional["CourseModule"]] = relationship("CourseModule", back_populates="materials", lazy='selectin')
    topic: Mapped[Optional["Topic"]] = relationship("Topic", back_populates="materials", lazy='selectin')
    
    def __str__(self):
        return self.title


# 6. STUDENT MODULE PROGRESS
class StudentModuleProgress(Base):
    __tablename__ = "student_module_progress"
    
    progress_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    module_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=False)
    status: Mapped[str] = mapped_column(String(50), server_default='not_started')
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    topics_completed: Mapped[int] = mapped_column(Integer, server_default='0')
    total_topics: Mapped[int] = mapped_column(Integer, server_default='0')
    progress_percentage: Mapped[float] = mapped_column(Numeric(5, 2), server_default='0.0')
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="progress")
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="progress")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'module_id'),
    )
    
    def __str__(self):
        return f"Progress ID: {self.progress_id} (Module: {self.module_id})"


# 7. MESSAGES
class Message(Base):
    __tablename__ = "messages"
    
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    processing_ms: Mapped[Optional[int]] = mapped_column(Integer, server_default='0')
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    message_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="messages")
    
    def __str__(self):
        return f"{self.sender_type}: {self.text_content[:30]}..."


# 8. RATE LIMITS
class RateLimit(Base):
    __tablename__ = "rate_limits"
    
    limit_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    limit_date: Mapped[date] = mapped_column(Date, nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, server_default='0')
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="rate_limits")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'limit_date'),
    )

    def __str__(self):
        return f"Limit for Student ID: {self.student_id} on {self.limit_date}"


# 9. SCHEDULE ITEMS
class ScheduleItem(Base):
    __tablename__ = "schedule_items"
    
    schedule_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    event_name: Mapped[str] = mapped_column(String(255), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="schedule_items")
    
    def __str__(self):
        return f"{self.event_name} ({self.event_date})"


# 10. ATTESTATION TESTS
class AttestationTest(Base):
    __tablename__ = "attestation_tests"
    
    test_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    passing_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_attempts: Mapped[int] = mapped_column(Integer, server_default='3')
    time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default='true')
    external_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="tests", lazy='selectin')
    results: Mapped[List["TestResult"]] = relationship("TestResult", back_populates="test", cascade="all, delete-orphan")
    
    def __str__(self):
        return self.title


# 11. TEST RESULTS
class TestResult(Base):
    __tablename__ = "test_results"
    
    result_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('attestation_tests.test_id', ondelete='CASCADE'), nullable=False)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="test_results")
    test: Mapped["AttestationTest"] = relationship("AttestationTest", back_populates="results")
    
    def __str__(self):
        return f"Test Result ID: {self.result_id} (Score: {self.score})"


# 12. FEEDBACK
class Feedback(Base):
    __tablename__ = "feedback"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=True)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Relationships
    student: Mapped[Optional["Student"]] = relationship("Student", back_populates="feedbacks")
    
    def __str__(self):
        return f"Feedback ID: {self.id} (Rating: {self.rating})"


# 13. REGISTRATION PROGRESS
class RegistrationProgress(Base):
    __tablename__ = "registration_progress"

    registration_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False, unique=True
    )
    current_stage: Mapped[int] = mapped_column(Integer, nullable=False, server_default='1')
    age_50_plus: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    need_help: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    registration_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    waiting_consultant_question: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="registration", lazy='selectin')
    consultant_requests: Mapped[List["ConsultantRequest"]] = relationship(
        "ConsultantRequest", back_populates="registration"
    )

    __table_args__ = (
        Index('idx_registration_progress_student_id', 'student_id'),
    )

    def __str__(self):
        return f"Регистрация #{self.registration_id} (этап {self.current_stage})"


# 14. CONSULTANT REQUESTS
class ConsultantRequest(Base):
    __tablename__ = "consultant_requests"

    request_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    registration_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey('registration_progress.registration_id', ondelete='SET NULL'), nullable=True
    )
    employee_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    request_type: Mapped[str] = mapped_column(String(20), nullable=False)
    stage_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_time_slot: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='new')
    operator_reply_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    operator_result_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_channel: Mapped[str] = mapped_column(String(20), nullable=False, server_default='max')
    source_message_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    operator_message_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    taken_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    student: Mapped["Student"] = relationship("Student", back_populates="consultant_requests", lazy='selectin')
    registration: Mapped[Optional["RegistrationProgress"]] = relationship(
        "RegistrationProgress", back_populates="consultant_requests", lazy='selectin'
    )

    __table_args__ = (
        CheckConstraint(
            "request_type IN ('chat_question', 'call_request')",
            name='consultant_requests_type_chk',
        ),
        CheckConstraint(
            'stage_number BETWEEN 1 AND 7',
            name='consultant_requests_stage_chk',
        ),
        CheckConstraint(
            "status IN ('new', 'in_progress', 'answered', 'closed', 'cancelled')",
            name='consultant_requests_status_chk',
        ),
        CheckConstraint(
            "call_time_slot IS NULL OR call_time_slot IN ('9-13', '13-17', '17-19')",
            name='consultant_requests_slot_chk',
        ),
        Index('idx_consultant_requests_student_id', 'student_id'),
        Index('idx_consultant_requests_status_created_at', 'status', 'created_at'),
        Index('idx_consultant_requests_employee_status', 'employee_id', 'status'),
        Index('idx_consultant_requests_registration_id', 'registration_id'),
    )

    def __str__(self):
        return f"Заявка #{self.request_id} ({self.request_type}, {self.status})"


# 15. REGISTRY CURRENT
class RegistryCurrent(Base):
    __tablename__ = "registry_current"

    row_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    app_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    row_key: Mapped[Optional[UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    site: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    registered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    program_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    training_period: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    person_id_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    provider_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employer_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    first_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status_history_terminal_done: Mapped[bool] = mapped_column(Boolean, server_default='false')

    __table_args__ = (
        Index('idx_registry_current_phone', 'phone'),
        Index('idx_registry_current_status', 'status'),
        Index('idx_registry_current_updated_at', 'updated_at'),
        Index('idx_registry_current_row_key', 'row_key'),
    )

    def __str__(self):
        return self.full_name or self.app_number or f"Реестр #{self.row_id}"

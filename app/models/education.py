"""
SQLAlchemy models matching the TutorAI PostgreSQL schema (actual DB tables).
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    BigInteger, String, Text, Boolean, DateTime, Date, Integer,
    ForeignKey, UniqueConstraint, Index, LargeBinary, Numeric, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column, deferred
from sqlalchemy.sql import func
from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    student_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    telegram_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    max_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=True)
    status: Mapped[str] = mapped_column(String(50), server_default='active')
    flow_mode: Mapped[str] = mapped_column(String(50), server_default='tutor')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    program_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    progress: Mapped[List["StudentModuleProgress"]] = relationship(
        "StudentModuleProgress", back_populates="student", cascade="all, delete-orphan"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="student", cascade="all, delete-orphan"
    )
    rate_limits: Mapped[List["RateLimit"]] = relationship(
        "RateLimit", back_populates="student", cascade="all, delete-orphan"
    )
    test_results: Mapped[List["TestResult"]] = relationship(
        "TestResult", back_populates="student", cascade="all, delete-orphan"
    )
    feedbacks: Mapped[List["Feedback"]] = relationship(
        "Feedback", back_populates="student", cascade="all, delete-orphan"
    )
    registration: Mapped[Optional["RegistrationProgress"]] = relationship(
        "RegistrationProgress", back_populates="student", uselist=False, cascade="all, delete-orphan"
    )
    consultant_requests: Mapped[List["ConsultantRequest"]] = relationship(
        "ConsultantRequest", back_populates="student", cascade="all, delete-orphan"
    )
    scenario_notifications: Mapped[List["ScenarioNotification"]] = relationship(
        "ScenarioNotification", back_populates="student", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_students_telegram_user_id', 'telegram_user_id'),
        Index('idx_students_max_user_id', 'max_user_id'),
        Index('idx_students_phone', 'phone'),
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class CourseMaterial(Base):
    __tablename__ = "course_materials"

    material_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    program_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    module_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
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

    def __str__(self):
        return self.title


class StudentModuleProgress(Base):
    __tablename__ = "student_module_progress"

    progress_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    status: Mapped[str] = mapped_column(String(50), server_default='not_started')
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    topics_completed: Mapped[int] = mapped_column(Integer, server_default='0')
    total_topics: Mapped[int] = mapped_column(Integer, server_default='0')
    progress_percentage: Mapped[float] = mapped_column(Numeric(5, 2), server_default='0.0')

    student: Mapped["Student"] = relationship("Student", back_populates="progress")

    __table_args__ = (
        UniqueConstraint('student_id', 'module_id'),
    )

    def __str__(self):
        return f"Прогресс #{self.progress_id} (модуль {self.module_id})"


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    processing_ms: Mapped[Optional[int]] = mapped_column(Integer, server_default='0')
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    message_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="messages")

    def __str__(self):
        return f"{self.sender_type}: {self.text_content[:30]}..."


class RateLimit(Base):
    __tablename__ = "rate_limits"

    limit_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    limit_date: Mapped[date] = mapped_column(Date, nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, server_default='0')

    student: Mapped["Student"] = relationship("Student", back_populates="rate_limits")

    __table_args__ = (
        UniqueConstraint('student_id', 'limit_date'),
    )

    def __str__(self):
        return f"Лимит студента {self.student_id} на {self.limit_date}"


class AttestationTest(Base):
    __tablename__ = "attestation_tests"

    test_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    passing_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_attempts: Mapped[int] = mapped_column(Integer, server_default='3')
    time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default='true')
    external_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    results: Mapped[List["TestResult"]] = relationship(
        "TestResult", back_populates="test", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.title


class TestResult(Base):
    __tablename__ = "test_results"

    result_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    test_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('attestation_tests.test_id', ondelete='CASCADE'), nullable=False
    )
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped["Student"] = relationship("Student", back_populates="test_results")
    test: Mapped["AttestationTest"] = relationship("AttestationTest", back_populates="results")

    def __str__(self):
        return f"Результат #{self.result_id} (балл: {self.score})"


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=True
    )
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    max_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    student: Mapped[Optional["Student"]] = relationship("Student", back_populates="feedbacks")

    def __str__(self):
        return f"Отзыв #{self.id} (оценка: {self.rating})"


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

    __table_args__ = (
        Index('idx_registration_progress_student_id', 'student_id'),
    )

    def __str__(self):
        return f"Регистрация #{self.registration_id} (этап {self.current_stage})"


class ConsultantRequest(Base):
    __tablename__ = "consultant_requests"

    request_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False
    )
    request_type: Mapped[str] = mapped_column(Text, nullable=False)
    stage_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_time_slot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default='new')
    employee_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    operator_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    operator_reply_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    closed_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    taken_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    replied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reply_sent_to_user: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    student: Mapped["Student"] = relationship("Student", back_populates="consultant_requests", lazy='selectin')

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
        CheckConstraint(
            """(
                (request_type = 'chat_question' AND question_text IS NOT NULL AND call_time_slot IS NULL)
                OR
                (request_type = 'call_request' AND call_time_slot IS NOT NULL)
            )""",
            name='consultant_requests_payload_chk',
        ),
        Index('idx_consultant_requests_student_id', 'student_id'),
        Index('idx_consultant_requests_status_created_at', 'status', 'created_at'),
        Index('idx_consultant_requests_employee_status', 'employee_id', 'status'),
    )

    def __str__(self):
        return f"Заявка #{self.request_id} ({self.request_type}, {self.status})"


class ScenarioNotification(Base):
    __tablename__ = "scenario_notifications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    history_line_row_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    app_number: Mapped[str] = mapped_column(Text, nullable=False)
    student_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=True
    )
    scenario_type: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped[Optional["Student"]] = relationship(
        "Student", back_populates="scenario_notifications", lazy='selectin'
    )

    def __str__(self):
        return f"Уведомление #{self.id} ({self.scenario_type})"

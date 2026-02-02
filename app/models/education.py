"""
SQLAlchemy models matching existing Supabase schema
"""

from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, BigInteger, String, Text, Boolean, DateTime, Date, Integer,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
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
    status: Mapped[str] = mapped_column(String(50), server_default='active')
    auth_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deauth_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", back_populates="students")
    progress: Mapped[List["StudentModuleProgress"]] = relationship("StudentModuleProgress", back_populates="student")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="student")
    rate_limits: Mapped[List["RateLimit"]] = relationship("RateLimit", back_populates="student")
    schedule_items: Mapped[List["ScheduleItem"]] = relationship("ScheduleItem", back_populates="student")
    test_results: Mapped[List["TestResult"]] = relationship("TestResult", back_populates="student")
    
    __table_args__ = (
        Index('idx_students_telegram_user_id', 'telegram_user_id'),
        Index('idx_students_phone', 'phone'),
        Index('idx_students_program_id', 'program_id'),
    )


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
    program: Mapped["Program"] = relationship("Program", back_populates="modules")
    topics: Mapped[List["Topic"]] = relationship("Topic", back_populates="module")
    materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="module")
    progress: Mapped[List["StudentModuleProgress"]] = relationship("StudentModuleProgress", back_populates="module")
    tests: Mapped[List["AttestationTest"]] = relationship("AttestationTest", back_populates="module")
    
    __table_args__ = (
        Index('idx_modules_program_id', 'program_id'),
    )


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
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="topics")
    materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="topic")
    
    __table_args__ = (
        Index('idx_topics_module_id', 'module_id'),
    )


# 5. COURSE MATERIALS
class CourseMaterial(Base):
    __tablename__ = "course_materials"
    
    material_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    program_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('programs.program_id', ondelete='CASCADE'), nullable=False)
    module_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('course_modules.module_id', ondelete='CASCADE'), nullable=True)
    topic_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('topics.topic_id', ondelete='CASCADE'), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    material_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    order_index: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, server_default='false')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", back_populates="materials")
    module: Mapped[Optional["CourseModule"]] = relationship("CourseModule", back_populates="materials")
    topic: Mapped[Optional["Topic"]] = relationship("Topic", back_populates="materials")
    
    __table_args__ = (
        Index('idx_course_materials_program_id', 'program_id'),
        Index('idx_course_materials_topic_id', 'topic_id'),
    )


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
    progress_percentage: Mapped[int] = mapped_column(Integer, server_default='0')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="progress")
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="progress")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'module_id'),
        Index('idx_student_progress_student_id', 'student_id'),
        Index('idx_student_progress_module_id', 'module_id'),
    )


# 7. MESSAGES
class Message(Base):
    __tablename__ = "messages"
    
    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)
    role: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    processing_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="messages")
    
    __table_args__ = (
        Index('idx_messages_student_id', 'student_id'),
        Index('idx_messages_created_at', 'created_at'),
    )


# 8. RATE LIMITS
class RateLimit(Base):
    __tablename__ = "rate_limits"
    
    limit_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    limit_date: Mapped[date] = mapped_column(Date, nullable=False)
    request_count: Mapped[int] = mapped_column(Integer, server_default='0')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="rate_limits")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'limit_date'),
        Index('idx_rate_limits_student_id_date', 'student_id', 'limit_date'),
    )


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
    
    __table_args__ = (
        Index('idx_schedule_items_student_id', 'student_id'),
        Index('idx_schedule_items_event_date', 'event_date'),
    )


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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    module: Mapped["CourseModule"] = relationship("CourseModule", back_populates="tests")
    results: Mapped[List["TestResult"]] = relationship("TestResult", back_populates="test")
    
    __table_args__ = (
        Index('idx_attestation_tests_module_id', 'module_id'),
    )


# 11. TEST RESULTS
class TestResult(Base):
    __tablename__ = "test_results"
    
    result_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    student_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)
    test_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('attestation_tests.test_id', ondelete='CASCADE'), nullable=False)
    attempt_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    percentage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    time_spent_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="test_results")
    test: Mapped["AttestationTest"] = relationship("AttestationTest", back_populates="results")
    
    __table_args__ = (
        Index('idx_test_results_student_id', 'student_id'),
        Index('idx_test_results_test_id', 'test_id'),
    )
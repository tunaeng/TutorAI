"""
SQLAlchemy models for education platform
All models as Python classes - no manual SQL as required by team lead
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    ForeignKey, Table, Enum as SQLEnum, Time, Date
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base
import enum


# Enums
class MaterialType(str, enum.Enum):
    LECTURE = "lecture"  # Лекционные материалы
    ASSIGNMENT = "assignment"  # Задания
    METHODICAL = "methodical"  # Методические материалы


class SenderType(str, enum.Enum):
    STUDENT = "student"
    BOT = "bot"


class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    GRADED = "graded"


class LessonType(str, enum.Enum):
    LECTURE = "lecture"  # Лекционная работа
    PRACTICAL = "practical"  # Практическая работа
    INDEPENDENT = "independent"  # Самостоятельная работа


class PromptType(str, enum.Enum):
    FAQ = "faq"
    MATERIALS = "materials"


# Association table for many-to-many relationship
students_streams = Table(
    'students_streams',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('stream_id', Integer, ForeignKey('streams.id'), primary_key=True)
)


class Student(Base):
    """Students table"""
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    telegram_user_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    course_program_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('course_programs.id'), nullable=True)
    
    # Relationships
    course_program: Mapped[Optional["CourseProgram"]] = relationship("CourseProgram", back_populates="students")
    streams: Mapped[List["Stream"]] = relationship("Stream", secondary=students_streams, back_populates="students")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="student")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="student")


class CourseProgram(Base):
    """Educational programs table"""
    __tablename__ = "course_programs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    students: Mapped[List["Student"]] = relationship("Student", back_populates="course_program")
    streams: Mapped[List["Stream"]] = relationship("Stream", back_populates="program")
    modules: Mapped[List["Module"]] = relationship("Module", back_populates="program")


class Stream(Base):
    """Learning streams table"""
    __tablename__ = "streams"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey('course_programs.id'), nullable=False)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    program: Mapped["CourseProgram"] = relationship("CourseProgram", back_populates="streams")
    students: Mapped[List["Student"]] = relationship("Student", secondary=students_streams, back_populates="streams")
    schedule: Mapped[List["Schedule"]] = relationship("Schedule", back_populates="stream")


class Module(Base):
    """Course modules (sections) table"""
    __tablename__ = "modules"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    program_id: Mapped[int] = mapped_column(Integer, ForeignKey('course_programs.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Duration in hours
    
    # Relationships
    program: Mapped["CourseProgram"] = relationship("CourseProgram", back_populates="modules")
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="module")


class Lesson(Base):
    """Lessons (topics) within modules table"""
    __tablename__ = "lessons"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey('modules.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_num: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    module: Mapped["Module"] = relationship("Module", back_populates="lessons")
    course_materials: Mapped[List["CourseMaterial"]] = relationship("CourseMaterial", back_populates="lesson")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="lesson")
    schedule: Mapped[List["Schedule"]] = relationship("Schedule", back_populates="lesson")


class CourseMaterial(Base):
    """Course materials table - 3 required types"""
    __tablename__ = "course_materials"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey('lessons.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    material_type: Mapped[MaterialType] = mapped_column(SQLEnum(MaterialType), nullable=False)
    
    # Relationships
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="course_materials")


class Message(Base):
    """Messages from students table (renamed from message_logs)"""
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telegram_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    chat_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sender_type: Mapped[SenderType] = mapped_column(SQLEnum(SenderType), nullable=False)
    sender_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    student: Mapped[Optional["Student"]] = relationship("Student", back_populates="messages")
    bot_responses: Mapped[List["BotResponse"]] = relationship("BotResponse", back_populates="message")


class BotResponse(Base):
    """Bot responses table (separate entity)"""
    __tablename__ = "bot_responses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey('messages.id'), nullable=False)
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    message: Mapped["Message"] = relationship("Message", back_populates="bot_responses")


class Assignment(Base):
    """Student assignments table"""
    __tablename__ = "assignments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'), nullable=False)
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey('lessons.id'), nullable=False)
    status: Mapped[AssignmentStatus] = mapped_column(SQLEnum(AssignmentStatus), default=AssignmentStatus.PENDING)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_intermediate_attestation: Mapped[bool] = mapped_column(Boolean, default=False)
    is_final_attestation: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="assignments")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="assignments")


class Schedule(Base):
    """Schedule table with different lesson types"""
    __tablename__ = "schedule"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    stream_id: Mapped[int] = mapped_column(Integer, ForeignKey('streams.id'), nullable=False)
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey('lessons.id'), nullable=False)
    scheduled_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    lesson_type: Mapped[LessonType] = mapped_column(SQLEnum(LessonType), nullable=False)
    start_time: Mapped[Optional[datetime]] = mapped_column(Time, nullable=True)  # Only for lecture/practical
    end_time: Mapped[Optional[datetime]] = mapped_column(Time, nullable=True)    # Only for lecture/practical
    
    # Relationships
    stream: Mapped["Stream"] = relationship("Stream", back_populates="schedule")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="schedule")


class Prompt(Base):
    """AI prompts storage table"""
    __tablename__ = "prompts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_type: Mapped[PromptType] = mapped_column(SQLEnum(PromptType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

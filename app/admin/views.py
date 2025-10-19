from sqladmin import Admin, ModelView
from app.core.database import engine
from app.models.education import (
    Student, CourseProgram, Stream, Module, Lesson,
    CourseMaterial, Schedule, Assignment, Message, BotResponse
)

class StudentAdmin(ModelView, model=Student):
    name = "Студент"
    name_plural = "Студенты"
    column_list = [Student.student_id, Student.name, Student.phone, Student.is_active]

class CourseProgramAdmin(ModelView, model=CourseProgram):
    name = "Программа курса"
    name_plural = "Программы курсов"
    column_list = [CourseProgram.program_id, CourseProgram.name, CourseProgram.total_hours]

class StreamAdmin(ModelView, model=Stream):
    name = "Поток"
    name_plural = "Потоки"
    column_list = [Stream.stream_id, Stream.name, Stream.start_date, Stream.end_date]

class ModuleAdmin(ModelView, model=Module):
    name = "Модуль"
    name_plural = "Модули"
    column_list = [Module.module_id, Module.name, Module.order_num]

class LessonAdmin(ModelView, model=Lesson):
    name = "Урок"
    name_plural = "Уроки"
    column_list = [Lesson.lesson_id, Lesson.name, Lesson.module_id]

class CourseMaterialAdmin(ModelView, model=CourseMaterial):
    name = "Материал курса"
    name_plural = "Материалы курса"
    column_list = [CourseMaterial.material_id, CourseMaterial.title, CourseMaterial.material_type]

class ScheduleAdmin(ModelView, model=Schedule):
    name = "Расписание"
    name_plural = "Расписания"
    column_list = [Schedule.schedule_id, Schedule.scheduled_date, Schedule.lesson_id]

class AssignmentAdmin(ModelView, model=Assignment):
    name = "Задание"
    name_plural = "Задания"
    column_list = [Assignment.assignment_id, Assignment.student_id, Assignment.status]

class MessageAdmin(ModelView, model=Message):
    name = "Сообщение"
    name_plural = "Сообщения"
    column_list = [Message.message_id, Message.sender_type, Message.created_at]
    can_create = False
    can_edit = False

class BotResponseAdmin(ModelView, model=BotResponse):
    name = "Ответ бота"
    name_plural = "Ответы бота"
    column_list = [BotResponse.response_id, BotResponse.text_content, BotResponse.created_at]
    can_create = False
    can_edit = False

def setup_admin(app):
    admin = Admin(app, engine, title="AI Tutor Admin")
    
    # Регистрация моделей
    admin.add_view(StudentAdmin)
    admin.add_view(CourseProgramAdmin)
    admin.add_view(StreamAdmin)
    admin.add_view(ModuleAdmin)
    admin.add_view(LessonAdmin)
    admin.add_view(CourseMaterialAdmin)
    admin.add_view(ScheduleAdmin)
    admin.add_view(AssignmentAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(BotResponseAdmin)
    
    return admin

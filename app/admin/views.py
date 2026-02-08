import hashlib
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from app.core.config import settings
from starlette.responses import HTMLResponse
from app.core.database import engine
from app.models.education import (
    Student, Program, CourseModule, Topic, CourseMaterial,
    StudentModuleProgress, Message, RateLimit, ScheduleItem,
    AttestationTest, TestResult, Feedback
)

class StudentAdmin(ModelView, model=Student):
    name = "Студент"
    name_plural = "Студенты"
    icon = "fa-solid fa-user"
    can_export = True
    
    column_list = [Student.student_id, Student.last_name, Student.first_name, Student.phone, Student.status]
    column_details_list = [Student.student_id, Student.last_name, Student.first_name, Student.patronymic, Student.phone, Student.telegram_user_id, Student.status, Student.created_at]
    
    column_searchable_list = [Student.student_id, Student.last_name, Student.first_name, Student.phone, Student.telegram_user_id]
    column_filters = [Student.status, Student.program_id]
    
    column_labels = {
        Student.student_id: "ID",
        Student.first_name: "Имя",
        Student.last_name: "Фамилия",
        Student.patronymic: "Отчество",
        Student.phone: "Телефон",
        Student.telegram_user_id: "Telegram ID",
        Student.telegram_chat_id: "Chat ID",
        Student.status: "Статус",
        Student.created_at: "Создан"
    }
    
    form_columns = [Student.first_name, Student.last_name, Student.patronymic, Student.phone, Student.program_id, Student.telegram_user_id, Student.telegram_chat_id, Student.status]

class ProgramAdmin(ModelView, model=Program):
    name = "Программа"
    name_plural = "Программы"
    icon = "fa-solid fa-graduation-cap"
    can_export = True
    
    column_list = [Program.program_id, Program.name, Program.total_hours]
    column_labels = {
        Program.program_id: "ID",
        Program.name: "Название",
        Program.description: "Описание",
        Program.total_hours: "Часов",
        Program.created_at: "Создана"
    }
    form_excluded_columns = [Program.students, Program.modules, Program.materials]

class CourseModuleAdmin(ModelView, model=CourseModule):
    name = "Модуль"
    name_plural = "Модули"
    icon = "fa-solid fa-book"
    can_export = True
    
    column_list = [CourseModule.module_id, CourseModule.name, CourseModule.order_index, CourseModule.total_hours]
    column_labels = {
        CourseModule.module_id: "ID",
        CourseModule.name: "Название",
        CourseModule.description: "Описание",
        CourseModule.order_index: "Порядок",
        CourseModule.total_hours: "Всего часов",
        CourseModule.lecture_hours: "Лекции",
        CourseModule.practice_hours: "Практика",
        CourseModule.self_study_hours: "Самостоятельно"
    }
    form_excluded_columns = [CourseModule.topics, CourseModule.materials, CourseModule.tests, CourseModule.progress]

class TopicAdmin(ModelView, model=Topic):
    name = "Тема"
    name_plural = "Темы"
    icon = "fa-solid fa-chalkboard-teacher"
    can_export = True
    
    column_list = [Topic.topic_id, Topic.name, Topic.order_index]
    column_labels = {
        Topic.topic_id: "ID",
        Topic.name: "Название",
        Topic.description: "Описание",
        Topic.order_index: "Порядок",
        Topic.lecture_hours: "Лекции",
        Topic.practice_hours: "Практика",
        Topic.self_study_hours: "Самостоятельно",
        Topic.is_intermediate_assessment: "Промежуточная аттестация",
        Topic.is_final_assessment: "Финальная аттестация"
    }

class CourseMaterialAdmin(ModelView, model=CourseMaterial):
    name = "Материал"
    name_plural = "Материалы"
    icon = "fa-solid fa-file-alt"
    can_export = True
    
    column_list = [CourseMaterial.material_id, CourseMaterial.title, CourseMaterial.material_type, CourseMaterial.is_public]
    column_labels = {
        CourseMaterial.material_id: "ID",
        CourseMaterial.title: "Название",
        CourseMaterial.content: "Содержимое",
        CourseMaterial.file_size: "Размер файла",
        CourseMaterial.file_mimetype: "Тип файла",
        CourseMaterial.material_type: "Тип",
        CourseMaterial.order_index: "Порядок",
        CourseMaterial.is_public: "Публичный"
    }
    form_excluded_columns = [CourseMaterial.file_data]

class StudentModuleProgressAdmin(ModelView, model=StudentModuleProgress):
    name = "Прогресс"
    name_plural = "Прогресс студентов"
    icon = "fa-solid fa-chart-line"
    can_export = True
    
    column_list = [StudentModuleProgress.progress_id, StudentModuleProgress.student_id, StudentModuleProgress.module_id, StudentModuleProgress.status, StudentModuleProgress.progress_percentage]
    column_labels = {
        StudentModuleProgress.progress_id: "ID",
        StudentModuleProgress.status: "Статус",
        StudentModuleProgress.started_at: "Начало",
        StudentModuleProgress.completed_at: "Завершено",
        StudentModuleProgress.topics_completed: "Тем завершено",
        StudentModuleProgress.total_topics: "Всего тем",
        StudentModuleProgress.progress_percentage: "Прогресс %"
    }

class MessageAdmin(ModelView, model=Message):
    name = "Сообщение"
    name_plural = "Сообщения"
    icon = "fa-solid fa-comment"
    can_create = False
    can_edit = False
    
    column_list = [Message.message_id, Message.sender_type, Message.role, Message.text_content, Message.created_at]
    column_labels = {
        Message.message_id: "ID",
        Message.sender_type: "Тип отправителя",
        Message.role: "Роль",
        Message.text_content: "Текст",
        Message.created_at: "Создано"
    }

class RateLimitAdmin(ModelView, model=RateLimit):
    name = "Лимит"
    name_plural = "Лимиты запросов"
    icon = "fa-solid fa-stopwatch"
    
    column_list = [RateLimit.limit_id, RateLimit.student_id, RateLimit.limit_date, RateLimit.request_count]
    column_labels = {
        RateLimit.limit_id: "ID",
        RateLimit.limit_date: "Дата",
        RateLimit.request_count: "Количество запросов"
    }

class ScheduleItemAdmin(ModelView, model=ScheduleItem):
    name = "Расписание"
    name_plural = "Расписание"
    icon = "fa-solid fa-calendar"
    
    column_list = [ScheduleItem.schedule_id, ScheduleItem.student_id, ScheduleItem.event_name, ScheduleItem.event_date]
    column_labels = {
        ScheduleItem.schedule_id: "ID",
        ScheduleItem.student_id: "Студент ID",
        ScheduleItem.event_name: "Название",
        ScheduleItem.event_date: "Дата",
        ScheduleItem.event_type: "Тип"
    }

class AttestationTestAdmin(ModelView, model=AttestationTest):
    name = "Тест"
    name_plural = "Тесты"
    icon = "fa-solid fa-clipboard-check"
    
    column_list = [AttestationTest.test_id, AttestationTest.title, AttestationTest.passing_score]
    column_labels = {
        AttestationTest.test_id: "ID",
        AttestationTest.title: "Название",
        AttestationTest.passing_score: "Проходной балл"
    }

class TestResultAdmin(ModelView, model=TestResult):
    name = "Результат теста"
    name_plural = "Результаты тестов"
    icon = "fa-solid fa-poll"
    
    column_list = [TestResult.result_id, TestResult.student_id, TestResult.test_id, TestResult.score, TestResult.passed]
    column_labels = {
        TestResult.result_id: "ID",
        TestResult.score: "Балл",
        TestResult.passed: "Сдан",
        TestResult.created_at: "Завершено"
    }

class FeedbackAdmin(ModelView, model=Feedback):
    name = "Отзыв"
    name_plural = "Отзывы"
    icon = "fa-solid fa-star"
    
    column_list = [Feedback.id, Feedback.student_id, Feedback.rating, Feedback.created_at]
    column_labels = {
        Feedback.id: "ID",
        Feedback.rating: "Оценка",
        Feedback.comment: "Комментарий",
        Feedback.created_at: "Создан"
    }

class AdminAuth(AuthenticationBackend):
    async def login(self, request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request) -> bool:
        return bool(request.session.get("authenticated"))

def setup_admin(app):
    auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(app, engine, title="TutorAI Admin", authentication_backend=auth_backend)
    admin.add_view(StudentAdmin)
    admin.add_view(ProgramAdmin)
    admin.add_view(CourseModuleAdmin)
    admin.add_view(TopicAdmin)
    admin.add_view(CourseMaterialAdmin)
    admin.add_view(StudentModuleProgressAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(RateLimitAdmin)
    admin.add_view(ScheduleItemAdmin)
    admin.add_view(AttestationTestAdmin)
    admin.add_view(TestResultAdmin)
    admin.add_view(FeedbackAdmin)
    return admin

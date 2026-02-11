from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from app.core.config import settings
from starlette.requests import Request
from wtforms import FileField, BooleanField
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
    column_list = [
        Student.student_id, 
        Student.last_name, 
        Student.first_name, 
        Student.patronymic, 
        Student.phone, 
        Student.telegram_user_id, 
        Student.created_at
    ]
    column_labels = {
        Student.student_id: "ID",
        Student.first_name: "Имя",
        Student.last_name: "Фамилия",
        Student.patronymic: "Отчество",
        Student.phone: "Телефон",
        Student.status: "Статус",
        Student.program: "Программа",
        Student.telegram_user_id: "Telegram ID",
        Student.telegram_chat_id: "Chat ID",
        Student.created_at: "Дата регистрации"
    }
    column_searchable_list = [
        Student.last_name,
        Student.first_name,
        Student.phone,
        Student.telegram_user_id
    ]
    column_sortable_list = [
        Student.student_id,
        Student.last_name,
        Student.first_name,
        Student.patronymic,
        Student.phone,
        Student.telegram_user_id,
        Student.created_at
    ]
    form_columns = [
        Student.last_name, 
        Student.first_name, 
        Student.patronymic, 
        Student.phone, 
        Student.program, 
        Student.status, 
        Student.telegram_user_id, 
        Student.telegram_chat_id
    ]


class ProgramAdmin(ModelView, model=Program):
    name = "Программа"
    name_plural = "Программы"
    icon = "fa-solid fa-graduation-cap"
    can_export = True
    column_list = [Program.program_id, Program.name, Program.total_hours, Program.created_at]
    column_labels = {
        Program.program_id: "ID",
        Program.name: "Название",
        Program.description: "Описание",
        Program.total_hours: "Всего часов",
        Program.created_at: "Дата создания"
    }
    column_sortable_list = [
        Program.program_id,
        Program.name,
        Program.total_hours,
        Program.created_at
    ]


class CourseModuleAdmin(ModelView, model=CourseModule):
    name = "Модуль"
    name_plural = "Модули"
    icon = "fa-solid fa-book"
    can_export = True
    column_list = [
        CourseModule.module_id, 
        CourseModule.name, 
        CourseModule.program, 
        CourseModule.order_index,
        CourseModule.total_hours
    ]
    column_labels = {
        CourseModule.module_id: "ID",
        CourseModule.name: "Название",
        CourseModule.program: "Программа",
        CourseModule.description: "Описание",
        CourseModule.order_index: "Порядок",
        CourseModule.total_hours: "Часов (всего)",
        CourseModule.lecture_hours: "Лекции",
        CourseModule.practice_hours: "Практика",
        CourseModule.self_study_hours: "Самост. работа"
    }
    column_sortable_list = [
        CourseModule.module_id,
        CourseModule.name,
        CourseModule.program,
        CourseModule.order_index,
        CourseModule.total_hours
    ]
    column_searchable_list = [CourseModule.name]

class TopicAdmin(ModelView, model=Topic):
    name = "Тема"
    name_plural = "Темы"
    icon = "fa-solid fa-chalkboard-teacher"
    can_export = True
    column_list = [
        Topic.topic_id, 
        Topic.name, 
        Topic.module, 
        Topic.order_index,
        Topic.is_intermediate_assessment,
        Topic.is_final_assessment
    ]
    column_labels = {
        Topic.topic_id: "ID",
        Topic.name: "Название",
        Topic.module: "Модуль",
        Topic.description: "Описание",
        Topic.order_index: "Порядок",
        Topic.lecture_hours: "Лекции",
        Topic.practice_hours: "Практика",
        Topic.self_study_hours: "Самост. работа",
        Topic.is_intermediate_assessment: "Пром. аттестация",
        Topic.is_final_assessment: "Итоговая аттестация"
    }
    column_sortable_list = [
        Topic.topic_id,
        Topic.name,
        Topic.module,
        Topic.order_index,
        Topic.is_intermediate_assessment,
        Topic.is_final_assessment
    ]
    column_searchable_list = [Topic.name]

class CourseMaterialAdmin(ModelView, model=CourseMaterial):
    name = "Материал"
    name_plural = "Материалы"
    icon = "fa-solid fa-file-alt"
    can_export = True
    column_list = [
        CourseMaterial.material_id, 
        CourseMaterial.title, 
        CourseMaterial.material_type, 
        CourseMaterial.external_url, 
        CourseMaterial.is_public
    ]
    column_labels = {
        CourseMaterial.material_id: "ID",
        CourseMaterial.program: "Программа",
        CourseMaterial.module: "Модуль",
        CourseMaterial.topic: "Тема",
        CourseMaterial.title: "Название",
        CourseMaterial.external_url: "Ссылка (URL)",
        CourseMaterial.content: "Текст материала",
        CourseMaterial.material_type: "Тип",
        CourseMaterial.order_index: "Порядок",
        CourseMaterial.is_public: "Опубликовано",
        CourseMaterial.file_size: "Размер файла",
        CourseMaterial.file_mimetype: "Тип файла (MIME)",
        "upload": "Загрузить файл напрямую"
    }
    column_sortable_list = [
        CourseMaterial.material_id,
        CourseMaterial.title,
        CourseMaterial.material_type,
        CourseMaterial.is_public
    ]
    column_searchable_list = [CourseMaterial.title]
    form_columns = [
        CourseMaterial.program, 
        CourseMaterial.module, 
        CourseMaterial.topic, 
        CourseMaterial.title, 
        CourseMaterial.external_url, 
        CourseMaterial.content, 
        "upload",
        CourseMaterial.material_type, 
        CourseMaterial.order_index, 
        CourseMaterial.is_public
    ]
    form_extra_fields = {
        "upload": FileField("Загрузить файл вручную (PDF/и др.)")
    }

    async def on_model_change(self, data, model, is_created, request: Request):
        form = await request.form()
        file_obj = form.get("upload")
        if file_obj and hasattr(file_obj, "filename") and file_obj.filename:
            content = await file_obj.read()
            model.file_data = content
            model.file_size = len(content)
            model.file_mimetype = file_obj.content_type

class ScheduleItemAdmin(ModelView, model=ScheduleItem):
    name = "Занятие"
    name_plural = "Расписание"
    icon = "fa-solid fa-calendar-day"
    column_list = [
        ScheduleItem.schedule_id, 
        ScheduleItem.student, 
        ScheduleItem.event_name, 
        ScheduleItem.event_date,
        ScheduleItem.event_type
    ]
    column_labels = {
        ScheduleItem.schedule_id: "ID",
        ScheduleItem.student: "Студент",
        ScheduleItem.event_name: "Событие",
        ScheduleItem.event_date: "Дата и время",
        ScheduleItem.event_type: "Тип",
        ScheduleItem.description: "Описание/Адрес"
    }
    column_sortable_list = [
        ScheduleItem.schedule_id,
        ScheduleItem.student,
        ScheduleItem.event_name,
        ScheduleItem.event_date,
        ScheduleItem.event_type
    ]
    column_searchable_list = [ScheduleItem.event_name]

class AttestationTestAdmin(ModelView, model=AttestationTest):
    name = "Тест"
    name_plural = "Тесты"
    icon = "fa-solid fa-vial"
    column_list = [
        AttestationTest.test_id, 
        AttestationTest.title, 
        AttestationTest.module, 
        AttestationTest.passing_score,
        AttestationTest.is_active,
        AttestationTest.external_url
    ]
    column_labels = {
        AttestationTest.test_id: "ID",
        AttestationTest.title: "Название",
        AttestationTest.module: "Модуль",
        AttestationTest.description: "Описание",
        AttestationTest.passing_score: "Проходной балл",
        AttestationTest.max_attempts: "Попыток",
        AttestationTest.time_limit_minutes: "Лимит (мин)",
        AttestationTest.is_active: "Активен",
        AttestationTest.external_url: "Внешняя ссылка"
    }
    column_sortable_list = [
        AttestationTest.test_id,
        AttestationTest.title,
        AttestationTest.module,
        AttestationTest.passing_score,
        AttestationTest.is_active
    ]
    column_searchable_list = [AttestationTest.title]

class StudentModuleProgressAdmin(ModelView, model=StudentModuleProgress):
    name = "Прогресс"
    name_plural = "Прогресс студентов"
    icon = "fa-solid fa-chart-line"
    column_list = [
        StudentModuleProgress.progress_id, 
        StudentModuleProgress.student, 
        StudentModuleProgress.module, 
        StudentModuleProgress.status, 
        StudentModuleProgress.progress_percentage
    ]
    column_labels = {
        StudentModuleProgress.progress_id: "ID",
        StudentModuleProgress.student: "Студент",
        StudentModuleProgress.module: "Модуль",
        StudentModuleProgress.status: "Статус",
        StudentModuleProgress.started_at: "Начало",
        StudentModuleProgress.completed_at: "Завершено",
        StudentModuleProgress.topics_completed: "Тем завершено",
        StudentModuleProgress.total_topics: "Всего тем",
        StudentModuleProgress.progress_percentage: "Прогресс %"
    }
    column_sortable_list = [
        StudentModuleProgress.progress_id,
        StudentModuleProgress.student,
        StudentModuleProgress.module,
        StudentModuleProgress.status,
        StudentModuleProgress.progress_percentage
    ]

class MessageAdmin(ModelView, model=Message):
    name = "Сообщение"
    name_plural = "История чатов"
    icon = "fa-solid fa-comment-dots"
    can_create = False
    column_list = [
        Message.message_id, 
        Message.student, 
        Message.sender_type, 
        Message.role, 
        Message.created_at,
        Message.text_content
    ]
    column_labels = {
        Message.message_id: "ID",
        Message.student: "Студент",
        Message.sender_type: "Отправитель",
        Message.role: "Роль",
        Message.text_content: "Текст сообщения",
        Message.created_at: "Дата"
    }
    column_sortable_list = [
        Message.message_id,
        Message.student,
        Message.sender_type,
        Message.role,
        Message.created_at
    ]
    column_searchable_list = [Message.text_content]

class RateLimitAdmin(ModelView, model=RateLimit):
    name = "Лимит"
    name_plural = "Лимиты GPT"
    icon = "fa-solid fa-stopwatch"
    column_list = [RateLimit.limit_id, RateLimit.student, RateLimit.limit_date, RateLimit.request_count]
    column_labels = {
        RateLimit.limit_id: "ID",
        RateLimit.student: "Студент",
        RateLimit.limit_date: "Дата",
        RateLimit.request_count: "Запросы"
    }
    column_sortable_list = [
        RateLimit.limit_id,
        RateLimit.student,
        RateLimit.limit_date,
        RateLimit.request_count
    ]

class TestResultAdmin(ModelView, model=TestResult):
    name = "Результат"
    name_plural = "Результаты тестов"
    icon = "fa-solid fa-poll"
    column_list = [
        TestResult.result_id, 
        TestResult.student, 
        TestResult.test, 
        TestResult.score, 
        TestResult.passed
    ]
    column_labels = {
        TestResult.result_id: "ID",
        TestResult.student: "Студент",
        TestResult.test: "Тест",
        TestResult.score: "Балл",
        TestResult.passed: "Сдан",
        TestResult.created_at: "Дата"
    }
    column_sortable_list = [
        TestResult.result_id,
        TestResult.student,
        TestResult.test,
        TestResult.score,
        TestResult.passed,
        TestResult.created_at
    ]

class FeedbackAdmin(ModelView, model=Feedback):
    name = "Отзыв"
    name_plural = "Отзывы"
    icon = "fa-solid fa-star"
    column_list = [
        Feedback.id, 
        Feedback.student, 
        Feedback.rating, 
        Feedback.message_id,
        Feedback.created_at
    ]
    column_labels = {
        Feedback.id: "ID",
        Feedback.student: "Студент",
        Feedback.rating: "Оценка",
        Feedback.message_id: "ID сообщения",
        Feedback.comment: "Комментарий",
        Feedback.created_at: "Дата"
    }
    column_sortable_list = [
        Feedback.id,
        Feedback.student,
        Feedback.rating,
        Feedback.created_at
    ]
    column_searchable_list = [Feedback.comment]

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("authenticated"))

def setup_admin(app):
    auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    admin = Admin(app, engine, title="TutorAI Admin", authentication_backend=auth_backend)
    admin.add_view(StudentAdmin)
    admin.add_view(ProgramAdmin)
    admin.add_view(CourseModuleAdmin)
    admin.add_view(TopicAdmin)
    admin.add_view(CourseMaterialAdmin)
    admin.add_view(ScheduleItemAdmin)
    admin.add_view(AttestationTestAdmin)
    admin.add_view(StudentModuleProgressAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(RateLimitAdmin)
    admin.add_view(TestResultAdmin)
    admin.add_view(FeedbackAdmin)
    return admin

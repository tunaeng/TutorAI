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
    column_sortable_list = [Student.student_id, Student.last_name, Student.first_name, Student.phone, Student.status, Student.created_at]
    
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
    column_searchable_list = [Program.name]
    column_sortable_list = [Program.program_id, Program.name, Program.total_hours]
    
    column_labels = {
        Program.program_id: "ID",
        Program.name: "Название",
        Program.description: "Описание",
        Program.total_hours: "Часов",
        Program.created_at: "Создана"
    }



class CourseModuleAdmin(ModelView, model=CourseModule):
    name = "Модуль"
    name_plural = "Модули"
    icon = "fa-solid fa-book"
    can_export = True
    
    column_list = [CourseModule.module_id, CourseModule.name, CourseModule.order_index, CourseModule.total_hours]
    column_searchable_list = [CourseModule.name]
    column_filters = [CourseModule.program_id]
    column_sortable_list = [CourseModule.module_id, CourseModule.name, CourseModule.order_index, CourseModule.total_hours]
    
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




class TopicAdmin(ModelView, model=Topic):
    name = "Тема"
    name_plural = "Темы"
    icon = "fa-solid fa-chalkboard-teacher"
    can_export = True
    
    column_list = [Topic.topic_id, Topic.name, Topic.order_index]
    column_searchable_list = [Topic.name]
    column_filters = [Topic.module_id]
    column_sortable_list = [Topic.topic_id, Topic.name, Topic.order_index]
    
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
    column_searchable_list = [CourseMaterial.title, CourseMaterial.material_type]
    column_filters = [CourseMaterial.material_type, CourseMaterial.is_public]
    column_sortable_list = [CourseMaterial.material_id, CourseMaterial.title, CourseMaterial.material_type]
    
    column_labels = {
        CourseMaterial.material_id: "ID",
        CourseMaterial.title: "Название",
        CourseMaterial.content: "Содержимое",
        CourseMaterial.file_url: "Ссылка на файл",
        CourseMaterial.material_type: "Тип",
        CourseMaterial.order_index: "Порядок",
        CourseMaterial.is_public: "Публичный"
    }
    
    form_widget_args = {
        "file_url": {"placeholder": "Введите URL файла из Supabase Storage"}
    }



class StudentModuleProgressAdmin(ModelView, model=StudentModuleProgress):
    name = "Прогресс"
    name_plural = "Прогресс студентов"
    icon = "fa-solid fa-chart-line"
    can_export = True
    
    column_list = [StudentModuleProgress.progress_id, StudentModuleProgress.student_id, StudentModuleProgress.module_id, StudentModuleProgress.status, StudentModuleProgress.progress_percentage]
    column_searchable_list = [StudentModuleProgress.student_id, StudentModuleProgress.status]
    column_sortable_list = [StudentModuleProgress.progress_id, StudentModuleProgress.student_id, StudentModuleProgress.module_id, StudentModuleProgress.status, StudentModuleProgress.progress_percentage]
    
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
    can_export = True
    
    column_list = [Message.message_id, Message.sender_type, Message.role, Message.telegram_user_id, Message.text_content, Message.created_at]
    column_searchable_list = [Message.message_id, Message.text_content, Message.telegram_user_id]
    column_filters = [Message.student_id, Message.sender_type, Message.role, Message.created_at]
    column_sortable_list = [Message.message_id, Message.sender_type, Message.role, Message.telegram_user_id, Message.text_content, Message.created_at]
    
    column_labels = {
        Message.message_id: "ID",
        Message.sender_type: "Тип отправителя",
        Message.role: "Роль",
        Message.telegram_user_id: "Telegram User ID",
        Message.text_content: "Текст",
        Message.message_type: "Тип сообщения",
        Message.processing_ms: "Время обработки (мс)",
        Message.created_at: "Создано"
    }


class RateLimitAdmin(ModelView, model=RateLimit):
    name = "Лимит"
    name_plural = "Лимиты запросов"
    icon = "fa-solid fa-stopwatch"
    can_export = True
    
    column_list = [RateLimit.limit_id, RateLimit.student_id, RateLimit.limit_date, RateLimit.request_count]
    column_searchable_list = [RateLimit.student_id, RateLimit.limit_date]
    column_sortable_list = [RateLimit.limit_id, RateLimit.student_id, RateLimit.limit_date, RateLimit.request_count]
    
    column_labels = {
        RateLimit.limit_id: "ID",
        RateLimit.limit_date: "Дата",
        RateLimit.request_count: "Количество запросов"
    }


class ScheduleItemAdmin(ModelView, model=ScheduleItem):
    name = "Расписание"
    name_plural = "Расписание"
    icon = "fa-solid fa-calendar"
    can_export = True
    
    column_list = [ScheduleItem.schedule_id, ScheduleItem.event_name, ScheduleItem.event_date, ScheduleItem.event_type]
    column_searchable_list = [ScheduleItem.event_name, ScheduleItem.event_type]
    column_sortable_list = [ScheduleItem.schedule_id, ScheduleItem.event_name, ScheduleItem.event_date, ScheduleItem.event_type]
    
    column_labels = {
        ScheduleItem.schedule_id: "ID",
        ScheduleItem.event_name: "Название",
        ScheduleItem.event_date: "Дата",
        ScheduleItem.event_type: "Тип",
        ScheduleItem.description: "Описание"
    }


class AttestationTestAdmin(ModelView, model=AttestationTest):
    name = "Тест"
    name_plural = "Тесты"
    icon = "fa-solid fa-clipboard-check"
    can_export = True
    
    column_list = [AttestationTest.test_id, AttestationTest.title, AttestationTest.passing_score, AttestationTest.is_active]
    column_searchable_list = [AttestationTest.title]
    column_sortable_list = [AttestationTest.test_id, AttestationTest.title, AttestationTest.passing_score, AttestationTest.is_active]
    
    column_labels = {
        AttestationTest.test_id: "ID",
        AttestationTest.title: "Название",
        AttestationTest.description: "Описание",
        AttestationTest.passing_score: "Проходной балл",
        AttestationTest.max_attempts: "Макс. попыток",
        AttestationTest.time_limit_minutes: "Время (мин)",
        AttestationTest.is_active: "Активен"
    }



class TestResultAdmin(ModelView, model=TestResult):
    name = "Результат теста"
    name_plural = "Результаты тестов"
    icon = "fa-solid fa-poll"
    can_export = True
    
    column_list = [TestResult.result_id, TestResult.student_id, TestResult.test_id, TestResult.score, TestResult.passed]
    column_searchable_list = [TestResult.student_id, TestResult.test_id]
    column_sortable_list = [TestResult.result_id, TestResult.student_id, TestResult.test_id, TestResult.score, TestResult.passed, TestResult.completed_at]
    
    column_labels = {
        TestResult.result_id: "ID",
        TestResult.attempt_number: "Попытка",
        TestResult.score: "Балл",
        TestResult.percentage: "Процент",
        TestResult.passed: "Сдан",
        TestResult.completed_at: "Завершено",
        TestResult.time_spent_minutes: "Время (мин)"
    }



class FeedbackAdmin(ModelView, model=Feedback):
    name = "Отзыв"
    name_plural = "Отзывы"
    icon = "fa-solid fa-star"
    can_export = True
    
    column_list = [Feedback.id, Feedback.student_id, Feedback.rating, Feedback.created_at]
    column_searchable_list = [Feedback.comment, Feedback.student_id]
    column_filters = [Feedback.rating, Feedback.student_id]
    column_sortable_list = [Feedback.id, Feedback.student_id, Feedback.rating, Feedback.created_at]
    
    column_labels = {
        Feedback.id: "ID",
        Feedback.rating: "Оценка",
        Feedback.comment: "Комментарий",
        Feedback.created_at: "Создан",
        Feedback.telegram_user_id: "Telegram ID",
        Feedback.message_id: "Message ID"
    }


class AdminAuth(AuthenticationBackend):
    async def login(self, request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Базовая валидация типов
        if not (isinstance(username, str) and isinstance(password, str)):
            return False

        # Сначала проверяем логин
        if username != settings.ADMIN_USERNAME:
            return False

        # Если в настройках задан хэш пароля — используем только его
        if settings.ADMIN_PASSWORD_HASH:
            password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if password_hash == settings.ADMIN_PASSWORD_HASH:
                request.session.update({"authenticated": True})
                return True
            return False

        # Fallback: если хэш не задан, используем старый вариант с открытым паролем
        if password == settings.ADMIN_PASSWORD:
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
    
    # Регистрация моделей
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

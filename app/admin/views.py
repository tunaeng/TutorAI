import csv
from datetime import datetime, timezone

import sqladmin.helpers
import sqladmin.models
from sqladmin.helpers import _PseudoBuffer

def patched_stream_to_csv(callback):
    # Используем ; как разделитель для Excel и добавляем BOM для корректной кодировки
    writer = csv.writer(_PseudoBuffer(), delimiter=';')
    async def new_callback(w):
        yield "\ufeff"
        async for item in callback(w):
            yield item
    return new_callback(writer)

sqladmin.helpers.stream_to_csv = patched_stream_to_csv
sqladmin.models.stream_to_csv = patched_stream_to_csv

from sqladmin import Admin, ModelView, action
from sqladmin.authentication import AuthenticationBackend
from app.core.config import settings
from starlette.requests import Request
from starlette.responses import RedirectResponse
from wtforms import FileField, SelectField
from app.core.database import engine
from app.models.education import (
    Student, CourseMaterial,
    StudentModuleProgress, Message, RateLimit,
    AttestationTest, TestResult, Feedback,
    RegistrationProgress, ConsultantRequest,
)

REQUEST_TYPE_LABELS = {
    "chat_question": "Вопрос в чате",
    "call_request": "Заявка на звонок",
}
STATUS_LABELS = {
    "new": "Новая",
    "in_progress": "В работе",
    "answered": "Отвечена",
    "closed": "Закрыта",
    "cancelled": "Отменена",
}
CALL_SLOT_LABELS = {
    "9-13": "9–13",
    "13-17": "13–17",
    "17-19": "17–19",
}

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
        Student.max_user_id,
        Student.created_at
    ]
    column_labels = {
        Student.student_id: "ID",
        Student.first_name: "Имя",
        Student.last_name: "Фамилия",
        Student.patronymic: "Отчество",
        Student.phone: "Телефон",
        Student.status: "Статус",
        Student.flow_mode: "Режим (tutor / registration)",
        Student.program_id: "ID программы",
        Student.telegram_user_id: "Telegram ID",
        Student.telegram_chat_id: "Telegram Chat ID",
        Student.max_user_id: "Max ID",
        Student.max_chat_id: "Max Chat ID",
        Student.created_at: "Дата регистрации"
    }
    column_searchable_list = [
        Student.last_name,
        Student.first_name,
        Student.phone,
        Student.telegram_user_id,
        Student.max_user_id
    ]
    column_sortable_list = [
        Student.student_id,
        Student.last_name,
        Student.first_name,
        Student.patronymic,
        Student.phone,
        Student.telegram_user_id,
        Student.max_user_id,
        Student.created_at
    ]
    form_columns = [
        Student.last_name, 
        Student.first_name, 
        Student.patronymic, 
        Student.phone, 
        Student.program_id,
        Student.status,
        Student.flow_mode,
        Student.telegram_user_id, 
        Student.telegram_chat_id,
        Student.max_user_id,
        Student.max_chat_id
    ]


class CourseMaterialAdmin(ModelView, model=CourseMaterial):
    name = "Материал"
    name_plural = "Материалы"
    icon = "fa-solid fa-file-alt"
    can_export = True
    column_list = [
        CourseMaterial.material_id,
        CourseMaterial.title,
        CourseMaterial.program_id,
        CourseMaterial.module_id,
        CourseMaterial.material_type,
        CourseMaterial.is_public,
    ]
    column_labels = {
        CourseMaterial.material_id: "ID",
        CourseMaterial.program_id: "ID программы",
        CourseMaterial.module_id: "ID модуля",
        CourseMaterial.topic_id: "ID темы",
        CourseMaterial.title: "Название",
        CourseMaterial.external_url: "Ссылка (URL)",
        CourseMaterial.content: "Текст материала",
        CourseMaterial.description: "Описание",
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
        CourseMaterial.program_id,
        CourseMaterial.module_id,
        CourseMaterial.topic_id,
        CourseMaterial.title,
        CourseMaterial.external_url,
        CourseMaterial.content,
        CourseMaterial.description,
        "upload",
        CourseMaterial.material_type,
        CourseMaterial.order_index,
        CourseMaterial.is_public,
    ]
    form_extra_fields = {
        "upload": FileField("Загрузить файл вручную (PDF/и др.)")
    }

    async def on_model_change(self, data, model, is_created, request: Request):
        form = await request.form()
        file_obj = form.get("upload")
        # Проверяем, что объект файла существует и имеет имя (т.е. файл был выбран)
        if file_obj and hasattr(file_obj, "filename") and file_obj.filename:
            try:
                content = await file_obj.read()
                if content:
                    model.file_data = content
                    model.file_size = len(content)
                    model.file_mimetype = file_obj.content_type
            except Exception:
                pass

class AttestationTestAdmin(ModelView, model=AttestationTest):
    name = "Тест"
    name_plural = "Тесты"
    icon = "fa-solid fa-vial"
    can_export = True
    column_list = [
        AttestationTest.test_id,
        AttestationTest.title,
        AttestationTest.module_id,
        AttestationTest.passing_score,
        AttestationTest.is_active,
        AttestationTest.external_url,
    ]
    column_labels = {
        AttestationTest.test_id: "ID",
        AttestationTest.title: "Название",
        AttestationTest.module_id: "ID модуля",
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
        AttestationTest.module_id,
        AttestationTest.passing_score,
        AttestationTest.is_active
    ]
    column_searchable_list = [AttestationTest.title]

class StudentModuleProgressAdmin(ModelView, model=StudentModuleProgress):
    name = "Прогресс"
    name_plural = "Прогресс студентов"
    icon = "fa-solid fa-chart-line"
    can_export = True
    column_list = [
        StudentModuleProgress.progress_id,
        StudentModuleProgress.student,
        StudentModuleProgress.module_id,
        StudentModuleProgress.status,
        StudentModuleProgress.progress_percentage,
    ]
    column_labels = {
        StudentModuleProgress.progress_id: "ID",
        StudentModuleProgress.student: "Студент",
        StudentModuleProgress.module_id: "ID модуля",
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
        StudentModuleProgress.module_id,
        StudentModuleProgress.status,
        StudentModuleProgress.progress_percentage
    ]

class MessageAdmin(ModelView, model=Message):
    name = "Сообщение"
    name_plural = "История чатов"
    icon = "fa-solid fa-comment-dots"
    can_create = False
    can_export = True
    column_list = [
        Message.message_id, 
        Message.student, 
        Message.sender_type, 
        Message.role, 
        Message.created_at,
        Message.max_user_id,
        Message.text_content
    ]
    column_labels = {
        Message.message_id: "ID",
        Message.student: "Студент",
        Message.sender_type: "Отправитель",
        Message.role: "Роль",
        Message.text_content: "Текст сообщения",
        Message.processing_ms: "Время обработки (мс)",
        Message.telegram_user_id: "Telegram ID",
        Message.max_user_id: "Max ID",
        Message.message_type: "Тип сообщения",
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
    can_export = True
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
    can_export = True
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
    can_export = True
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
        Feedback.telegram_user_id: "Telegram ID",
        Feedback.max_user_id: "Max ID",
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


class RegistrationProgressAdmin(ModelView, model=RegistrationProgress):
    name = "Регистрация"
    name_plural = "Регистрация (воронка)"
    icon = "fa-solid fa-clipboard-list"
    can_export = True
    column_list = [
        RegistrationProgress.registration_id,
        RegistrationProgress.student,
        RegistrationProgress.current_stage,
        RegistrationProgress.registration_completed,
        RegistrationProgress.need_help,
        RegistrationProgress.waiting_consultant_question,
        RegistrationProgress.updated_at,
    ]
    column_labels = {
        RegistrationProgress.registration_id: "ID",
        RegistrationProgress.student: "Студент",
        RegistrationProgress.current_stage: "Текущий этап",
        RegistrationProgress.age_50_plus: "Ответ: 50+",
        RegistrationProgress.need_help: "Нужна помощь",
        RegistrationProgress.registration_completed: "Регистрация завершена",
        RegistrationProgress.waiting_consultant_question: "Ожидает вопрос консультанта",
        RegistrationProgress.created_at: "Создано",
        RegistrationProgress.updated_at: "Обновлено",
    }
    column_sortable_list = [
        RegistrationProgress.registration_id,
        RegistrationProgress.student,
        RegistrationProgress.current_stage,
        RegistrationProgress.registration_completed,
        RegistrationProgress.updated_at,
    ]
    column_searchable_list = [RegistrationProgress.age_50_plus]
    form_columns = [
        RegistrationProgress.student,
        RegistrationProgress.current_stage,
        RegistrationProgress.age_50_plus,
        RegistrationProgress.need_help,
        RegistrationProgress.registration_completed,
        RegistrationProgress.waiting_consultant_question,
    ]
    form_ajax_refs = {
        "student": {
            "fields": ("last_name", "first_name", "phone"),
            "order_by": "last_name",
        }
    }


class ConsultantRequestAdmin(ModelView, model=ConsultantRequest):
    name = "Заявка консультанта"
    name_plural = "Заявки консультанта"
    icon = "fa-solid fa-headset"
    can_export = True
    list_template = "consultant_request_list.html"
    column_list = [
        ConsultantRequest.request_id,
        ConsultantRequest.student,
        "student.phone",
        ConsultantRequest.request_type,
        ConsultantRequest.stage_number,
        ConsultantRequest.status,
        ConsultantRequest.operator_name,
        ConsultantRequest.reply_sent_to_user,
        ConsultantRequest.created_at,
    ]
    column_labels = {
        ConsultantRequest.request_id: "ID",
        ConsultantRequest.student: "Студент",
        "student.phone": "Телефон",
        ConsultantRequest.employee_id: "ID сотрудника",
        ConsultantRequest.request_type: "Тип заявки",
        ConsultantRequest.stage_number: "Этап (1–7)",
        ConsultantRequest.question_text: "Текст вопроса",
        ConsultantRequest.call_time_slot: "Слот звонка",
        ConsultantRequest.call_scheduled_at: "Запланированный звонок",
        ConsultantRequest.status: "Статус",
        ConsultantRequest.operator_name: "Имя оператора",
        ConsultantRequest.operator_reply_text: "Ответ оператора",
        ConsultantRequest.closed_reason: "Причина закрытия",
        ConsultantRequest.created_at: "Создано",
        ConsultantRequest.taken_at: "Взято в работу",
        ConsultantRequest.replied_at: "Отвечено",
        ConsultantRequest.reply_sent_to_user: "Ответ отправлен пользователю",
        ConsultantRequest.closed_at: "Закрыто",
    }
    column_sortable_list = [
        ConsultantRequest.request_id,
        ConsultantRequest.student,
        ConsultantRequest.status,
        ConsultantRequest.created_at,
    ]
    column_searchable_list = [
        ConsultantRequest.question_text,
        ConsultantRequest.operator_reply_text,
        ConsultantRequest.operator_name,
        ConsultantRequest.closed_reason,
    ]
    form_columns = [
        ConsultantRequest.student,
        ConsultantRequest.employee_id,
        ConsultantRequest.request_type,
        ConsultantRequest.stage_number,
        ConsultantRequest.question_text,
        ConsultantRequest.call_time_slot,
        ConsultantRequest.call_scheduled_at,
        ConsultantRequest.status,
        ConsultantRequest.operator_name,
        ConsultantRequest.operator_reply_text,
        ConsultantRequest.closed_reason,
        ConsultantRequest.taken_at,
        ConsultantRequest.replied_at,
        ConsultantRequest.closed_at,
    ]
    form_ajax_refs = {
        "student": {
            "fields": ("last_name", "first_name", "phone"),
            "order_by": "last_name",
        },
    }
    form_overrides = {
        "request_type": SelectField,
        "status": SelectField,
        "call_time_slot": SelectField,
    }
    form_args = {
        "request_type": {
            "choices": [(value, label) for value, label in REQUEST_TYPE_LABELS.items()],
            "coerce": str,
        },
        "status": {
            "choices": [(value, label) for value, label in STATUS_LABELS.items()],
            "coerce": str,
        },
        "call_time_slot": {
            "choices": [("", "—")] + [(value, label) for value, label in CALL_SLOT_LABELS.items()],
            "coerce": str,
        },
    }
    form_widget_args = {
        "call_scheduled_at": {"readonly": True},
    }
    column_formatters = {
        ConsultantRequest.request_type: lambda m, a: REQUEST_TYPE_LABELS.get(m.request_type, m.request_type),
        ConsultantRequest.status: lambda m, a: STATUS_LABELS.get(m.status, m.status),
        ConsultantRequest.call_time_slot: lambda m, a: CALL_SLOT_LABELS.get(m.call_time_slot, m.call_time_slot or "—"),
        ConsultantRequest.reply_sent_to_user: lambda m, a: "Да" if m.reply_sent_to_user else ("Нет" if m.reply_sent_to_user is not None else "—"),
    }

    async def on_model_change(self, data, model, is_created, request: Request):
        if not is_created:
            data["call_scheduled_at"] = model.call_scheduled_at

        if not model.call_time_slot:
            model.call_time_slot = None

        if model.request_type == "chat_question":
            if not model.question_text:
                raise ValueError("Для типа «Вопрос в чате» нужно заполнить текст вопроса.")
            model.call_time_slot = None
        elif model.request_type == "call_request":
            if not model.call_time_slot:
                raise ValueError("Для типа «Заявка на звонок» нужно выбрать слот звонка.")
        else:
            raise ValueError(
                "Недопустимый тип заявки. Выберите «Вопрос в чате» или «Заявка на звонок»."
            )

    @action(
        name="close_requests",
        label="Закрыть выбранные",
        confirmation_message="Закрыть выбранные заявки?",
        add_in_detail=True,
        add_in_list=True,
    )
    async def close_requests(self, request: Request):
        pks = [pk for pk in request.query_params.get("pks", "").split(",") if pk]
        if pks:
            now = datetime.now(timezone.utc)
            async with self.session_maker() as session:
                for pk in pks:
                    stmt = self._stmt_by_identifier(pk)
                    result = await session.execute(stmt)
                    model = result.scalars().first()
                    if model and model.status not in ("closed", "cancelled"):
                        model.status = "closed"
                        if not model.closed_at:
                            model.closed_at = now
                await session.commit()

        referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        return RedirectResponse(request.url_for("admin:list", identity=self.identity))


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
    admin = Admin(
        app,
        engine,
        title="TutorAI Admin",
        authentication_backend=auth_backend,
        templates_dir="app/templates",
    )
    admin.add_view(StudentAdmin)
    admin.add_view(RegistrationProgressAdmin)
    admin.add_view(ConsultantRequestAdmin)
    admin.add_view(CourseMaterialAdmin)
    admin.add_view(AttestationTestAdmin)
    admin.add_view(StudentModuleProgressAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(RateLimitAdmin)
    admin.add_view(TestResultAdmin)
    admin.add_view(FeedbackAdmin)
    return admin

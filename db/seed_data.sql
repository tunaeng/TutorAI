-- Test data for AI Tutor Backend
-- This file contains sample data for testing and development

-- Insert test course programs
INSERT INTO course_programs (name, description, total_hours) VALUES
('Python для начинающих', 'Базовый курс Python программирования', 120),
('Веб-разработка на Django', 'Полный курс создания веб-приложений', 200),
('Анализ данных с Pandas', 'Курс по анализу данных в Python', 80)
ON CONFLICT DO NOTHING;

-- Insert test students
INSERT INTO students (phone, name, telegram_user_id, telegram_username, course_program_id, is_active) VALUES
('+79991234567', 'Иван Тестов', 123456789, 'ivan_test', 1, true),
('+79991234568', 'Мария Студентова', 123456790, 'maria_student', 1, true),
('+79991234569', 'Алексей Программист', 123456791, 'alex_dev', 2, true),
('+79991234570', 'Елена Аналитик', 123456792, 'elena_analyst', 3, true)
ON CONFLICT (phone) DO NOTHING;

-- Insert test streams
INSERT INTO streams (program_id, name, start_date, end_date, description) VALUES
(1, 'Python Stream 2024-01', '2024-01-15', '2024-06-15', 'Основной поток Python курса'),
(1, 'Python Stream 2024-02', '2024-07-01', '2024-12-01', 'Второй поток Python курса'),
(2, 'Django Stream 2024', '2024-02-01', '2024-08-01', 'Поток веб-разработки'),
(3, 'Data Analysis Stream 2024', '2024-03-01', '2024-06-01', 'Поток анализа данных')
ON CONFLICT DO NOTHING;

-- Insert students into streams
INSERT INTO students_streams (student_id, stream_id, enrolled_at) VALUES
(1, 1, '2024-01-10 10:00:00+03'),
(2, 1, '2024-01-12 14:30:00+03'),
(3, 3, '2024-01-25 09:15:00+03'),
(4, 4, '2024-02-20 16:45:00+03')
ON CONFLICT DO NOTHING;

-- Insert test modules
INSERT INTO modules (program_id, order_num, name, description, duration_hours, lecture_hours, practice_hours, independent_hours, is_intermediate_attestation, is_final_attestation) VALUES
(1, 1, 'Основы Python', 'Введение в Python программирование', 20, 10, 8, 2, false, false),
(1, 2, 'Структуры данных', 'Списки, словари, кортежи', 25, 12, 10, 3, true, false),
(1, 3, 'Функции и модули', 'Создание функций и работа с модулями', 30, 15, 12, 3, false, true),
(2, 1, 'Основы Django', 'Введение в Django фреймворк', 40, 20, 15, 5, false, false),
(2, 2, 'Модели и базы данных', 'Django ORM и работа с БД', 35, 18, 14, 3, true, false),
(3, 1, 'Pandas основы', 'Введение в библиотеку Pandas', 20, 10, 8, 2, false, false),
(3, 2, 'Анализ данных', 'Визуализация и статистика', 25, 12, 10, 3, false, true)
ON CONFLICT DO NOTHING;

-- Insert test lessons
INSERT INTO lessons (module_id, order_num, name, description, duration_hours) VALUES
(1, 1, 'Переменные и типы данных', 'Изучение основных типов данных Python', 2),
(1, 2, 'Условные операторы', 'if, elif, else конструкции', 2),
(1, 3, 'Циклы', 'for и while циклы', 3),
(2, 1, 'Списки', 'Работа со списками в Python', 3),
(2, 2, 'Словари', 'Создание и использование словарей', 3),
(2, 3, 'Кортежи и множества', 'Неизменяемые структуры данных', 2),
(3, 1, 'Создание функций', 'def, параметры, возврат значений', 4),
(3, 2, 'Лямбда функции', 'Анонимные функции', 2),
(4, 1, 'Установка Django', 'Создание проекта и приложения', 3),
(4, 2, 'URL маршрутизация', 'Настройка URL patterns', 3),
(5, 1, 'Django модели', 'Создание моделей данных', 4),
(5, 2, 'Миграции', 'Создание и применение миграций', 3),
(6, 1, 'DataFrame основы', 'Создание и работа с DataFrame', 3),
(6, 2, 'Индексация и фильтрация', 'Выборка данных', 3),
(7, 1, 'Визуализация с Matplotlib', 'Построение графиков', 4),
(7, 2, 'Статистический анализ', 'Описательная статистика', 3)
ON CONFLICT DO NOTHING;

-- Insert test course materials
INSERT INTO course_materials (lesson_id, title, content, file_path, material_type, material_category, is_public) VALUES
(1, 'Типы данных Python', 'Подробное описание основных типов данных', '/materials/python_types.pdf', 'PDF', 'lecture', true),
(1, 'Практическое задание', 'Создайте переменные разных типов', '/materials/assignment_1.py', 'PYTHON', 'assignment', false),
(2, 'Условные операторы', 'Лекция по условным конструкциям', '/materials/conditions.pdf', 'PDF', 'lecture', true),
(3, 'Циклы в Python', 'Видеоурок по циклам', '/materials/loops.mp4', 'VIDEO', 'lecture', true),
(4, 'Работа со списками', 'Практическое руководство', '/materials/lists_guide.pdf', 'PDF', 'methodical', true),
(5, 'Словари и их применение', 'Интерактивный урок', '/materials/dicts.html', 'HTML', 'lecture', true),
(7, 'Функции в Python', 'Подробная лекция', '/materials/functions.pdf', 'PDF', 'lecture', true),
(7, 'Создание функций', 'Практическое задание', '/materials/functions_task.py', 'PYTHON', 'assignment', false),
(9, 'Django Quick Start', 'Быстрый старт с Django', '/materials/django_start.pdf', 'PDF', 'lecture', true),
(11, 'Django модели', 'Создание моделей данных', '/materials/django_models.pdf', 'PDF', 'lecture', true),
(13, 'Pandas DataFrame', 'Основы работы с DataFrame', '/materials/pandas_df.pdf', 'PDF', 'lecture', true),
(15, 'Визуализация данных', 'Matplotlib и Seaborn', '/materials/visualization.pdf', 'PDF', 'lecture', true)
ON CONFLICT DO NOTHING;

-- Insert test messages
INSERT INTO messages (telegram_message_id, chat_id, sender_type, sender_id, text_content, created_at) VALUES
(1001, 123456789, 'user', 1, 'Привет! Как дела с курсом?', '2024-01-20 10:30:00+03'),
(1002, 123456789, 'bot', NULL, 'Привет! Курс идет отлично. Как дела с домашним заданием?', '2024-01-20 10:30:15+03'),
(1003, 123456790, 'user', 2, 'Не понимаю задачу с циклами', '2024-01-22 14:20:00+03'),
(1004, 123456790, 'bot', NULL, 'Давайте разберем задачу пошагово. Какой именно цикл вызывает сложности?', '2024-01-22 14:20:30+03'),
(1005, 123456791, 'user', 3, 'Когда будет следующая лекция по Django?', '2024-01-25 09:15:00+03'),
(1006, 123456792, 'user', 4, 'Спасибо за материал по Pandas!', '2024-01-28 16:45:00+03')
ON CONFLICT (telegram_message_id) DO NOTHING;

-- Insert test bot responses
INSERT INTO bot_responses (message_id, text_content, created_at) VALUES
(2, 'Привет! Курс идет отлично. Как дела с домашним заданием?', '2024-01-20 10:30:15+03'),
(4, 'Давайте разберем задачу пошагово. Какой именно цикл вызывает сложности?', '2024-01-22 14:20:30+03')
ON CONFLICT DO NOTHING;

-- Insert test meetings
INSERT INTO meetings (stream_id, lesson_id, meeting_type, meeting_date, start_time, end_time, description) VALUES
(1, 1, 'lecture', '2024-01-15', '10:00:00', '12:00:00', 'Вводная лекция по Python'),
(1, 2, 'practice', '2024-01-17', '14:00:00', '16:00:00', 'Практическое занятие по условным операторам'),
(1, 3, 'lecture', '2024-01-20', '10:00:00', '13:00:00', 'Лекция по циклам'),
(1, 4, 'independent', '2024-01-22', NULL, NULL, 'Самостоятельная работа со списками'),
(3, 9, 'lecture', '2024-02-05', '10:00:00', '13:00:00', 'Введение в Django'),
(3, 10, 'practice', '2024-02-07', '14:00:00', '17:00:00', 'Практика с URL маршрутизацией'),
(4, 13, 'lecture', '2024-03-05', '10:00:00', '13:00:00', 'Основы Pandas DataFrame'),
(4, 15, 'practice', '2024-03-12', '14:00:00', '17:00:00', 'Практика визуализации данных')
ON CONFLICT DO NOTHING;

-- Insert test schedule
INSERT INTO schedule (stream_id, lesson_id, scheduled_date, is_completed) VALUES
(1, 1, '2024-01-15', true),
(1, 2, '2024-01-17', true),
(1, 3, '2024-01-20', true),
(1, 4, '2024-01-22', false),
(1, 5, '2024-01-24', false),
(1, 6, '2024-01-27', false),
(3, 9, '2024-02-05', true),
(3, 10, '2024-02-07', true),
(3, 11, '2024-02-10', false),
(4, 13, '2024-03-05', true),
(4, 14, '2024-03-08', false),
(4, 15, '2024-03-12', false)
ON CONFLICT DO NOTHING;

-- Insert test assignments
INSERT INTO assignments (student_id, lesson_id, name, description, status, deadline, submitted_at, checked_at, feedback, grade) VALUES
(1, 1, 'Переменные и типы', 'Создайте переменные всех основных типов данных', 'completed', '2024-01-18', '2024-01-17 18:30:00+03', '2024-01-18 10:15:00+03', 'Отличная работа! Все типы данных использованы правильно.', 5),
(1, 2, 'Условные операторы', 'Напишите программу с использованием if-elif-else', 'completed', '2024-01-20', '2024-01-19 20:45:00+03', '2024-01-20 09:30:00+03', 'Хорошо, но можно улучшить читаемость кода.', 4),
(2, 1, 'Переменные и типы', 'Создайте переменные всех основных типов данных', 'submitted', '2024-01-18', '2024-01-18 23:59:00+03', NULL, NULL, NULL),
(2, 2, 'Условные операторы', 'Напишите программу с использованием if-elif-else', 'pending', '2024-01-20', NULL, NULL, NULL, NULL),
(3, 9, 'Django проект', 'Создайте базовый Django проект', 'completed', '2024-02-08', '2024-02-07 19:20:00+03', '2024-02-08 11:00:00+03', 'Проект создан корректно, структура правильная.', 5),
(4, 13, 'Pandas анализ', 'Проанализируйте предоставленный датасет', 'submitted', '2024-03-10', '2024-03-09 22:15:00+03', NULL, NULL, NULL)
ON CONFLICT DO NOTHING;

-- Insert test prompts
INSERT INTO prompts (prompt_type, prompt_text, description, version, is_active) VALUES
('question_classifier', 'Classify this question about Python programming into one of these categories: syntax, data_structures, functions, modules, errors, general. Question: {question}', 'Default question classifier for Python questions', 1, true),
('faq_response', 'Answer this frequently asked question about Python: {question}. Provide a clear, concise answer with examples if needed.', 'FAQ response generator for Python questions', 1, true),
('material_response', 'Based on the course material about {topic}, provide a detailed explanation and examples. Material: {material_content}', 'Material-based response generator', 1, true),
('question_classifier', 'Classify this question about Django web development into: models, views, templates, urls, deployment, general. Question: {question}', 'Question classifier for Django questions', 1, true),
('faq_response', 'Answer this Django-related question: {question}. Include code examples and best practices.', 'FAQ response generator for Django questions', 1, true)
ON CONFLICT DO NOTHING;

-- Insert test FAQ responses
INSERT INTO faq_responses (category, keywords, question, answer_text, is_active) VALUES
('python', 'переменные, типы, int, str, float', 'Что такое переменная в Python?', 'Переменная в Python - это именованная область памяти для хранения данных. Python автоматически определяет тип переменной на основе присвоенного значения.', true),
('python', 'список, list, append, remove', 'Как добавить элемент в список?', 'Для добавления элемента в список используйте метод append(): my_list.append(element). Для вставки в определенную позицию - insert(index, element).', true),
('python', 'цикл, for, while, break, continue', 'В чем разница между for и while циклами?', 'for используется для итерации по последовательности (список, строка, range), while - для повторения блока кода пока условие истинно. for обычно используется когда известно количество итераций.', true),
('django', 'модель, model, поле, field', 'Как создать модель в Django?', 'Создайте класс, наследующийся от models.Model, и определите поля как атрибуты класса. Например: class User(models.Model): name = models.CharField(max_length=100)', true),
('django', 'миграция, migration, makemigrations, migrate', 'Что такое миграции в Django?', 'Миграции - это файлы, которые описывают изменения в структуре базы данных. makemigrations создает миграции, migrate применяет их к базе данных.', true),
('pandas', 'dataframe, df, создание, создание', 'Как создать DataFrame в Pandas?', 'DataFrame можно создать из словаря: df = pd.DataFrame({"col1": [1,2,3], "col2": ["a","b","c"]}) или из CSV файла: df = pd.read_csv("file.csv")', true),
('pandas', 'фильтрация, filter, loc, iloc', 'Как отфильтровать данные в DataFrame?', 'Используйте boolean indexing: df[df["column"] > value] или методы loc/iloc: df.loc[df["column"] > value, ["col1", "col2"]]', true)
ON CONFLICT DO NOTHING;

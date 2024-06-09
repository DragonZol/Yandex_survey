# Система голосового анкетирования на платформе Яндекс.Диалоги

## ![2024-06-09_14-27-50](https://github.com/DragonZol/Yandex_survey/assets/116492948/3d6bc18e-5b47-4535-b508-b57884d155d0)

Этот проект реализует систему голосового анкетирования с использованием платформы Яндекс.Диалоги. Основная функциональность включает управление состояниями, обработку намерений пользователя и динамическое формирование вопросов в зависимости от ответов пользователя.

## Возможности

- **Управление состояниями**: Плавный переход между состояниями анкеты на основе ответов пользователя и заданных условий.
- **Обработка намерений пользователя**: Поддержка различных намерений пользователя, таких как остановка или пропуск вопросов.
- **Динамическое формирование вопросов**: Определение следующего вопроса на основе текущего состояния и предыдущих ответов пользователя.
- **Конфигурируемые вопросы**: Поддержка различных типов вопросов и ожиданий намерений для широкого спектра анкет.
- **Генерация вопросов из БД**: Автоматическая генерация структуры анкеты на основе данных из внешней базы данных.

## Функции

### Основные функции

- `make_response(text, buttons=None, state=None)`: Формирует ответ для платформы Яндекс.Диалоги.
- `get_intents(event)`: Извлекает намерения пользователя из события.
- `is_new_session(event)`: Проверяет, является ли сессия новой.
- `is_not_new(state)`: Проверяет, есть ли текущее состояние.
- `get_state(event)`: Извлекает текущее состояние из события.

### Функции для работы с вопросами и состояниями

- `get_current_state(state)`: Получает текущее состояние экрана.
- `get_next_state(cur_state)`: Определяет следующее состояние на основе текущего.
- `compare(actual, expected, operator)`: Сравнивает фактическое и ожидаемое значения по заданному оператору.
- `get_conditional_next_state(cur_state, state)`: Определяет следующее состояние на основе условий.
- `get_question_type(cur_state)`: Возвращает тип текущего вопроса.
- `get_expected_intent(cur_state)`: Возвращает ожидаемое намерение для текущего вопроса.
- `get_slots_to_fill(cur_state)`: Возвращает слоты, которые необходимо заполнить для текущего вопроса.
- `get_possible_values(cur_state)`: Возвращает возможные значения для слотов текущего вопроса.

### Функции для обработки ответов пользователя

- `if_stop(intents)`: Проверяет, содержит ли намерения пользователя команду остановки.
- `if_skip(intents)`: Проверяет, содержит ли намерения пользователя команду пропуска.
- `if_was_next(cur_state, intents)`: Проверяет, соответствует ли намерение пользователя ожидаемому.
- `get_value(cur_state, intents)`: Извлекает значение ответа из намерений пользователя.
- `get_question_text(cur_state, state)`: Формирует текст вопроса для текущего состояния.

### Инициализация и форматирование

- `initialize_state()`: Инициализирует состояние анкеты.
- `format_answers(state)`: Форматирует ответы пользователя для сохранения.

### Основные функции для работы с анкетой

- `first_question(state)`: Инициализирует первый вопрос анкеты.
- `ask_question(state, event)`: Задает следующий вопрос в анкете.

### Функция обработки событий

- `handler(event, context)`: Основная функция-обработчик для Яндекс.Диалогов, управляющая состояниями и обработкой ответов.

### Генерация вопросов из базы данных

- `load_questions_from_url(url)`: Загружает вопросы из внешней базы данных по указанному URL.
- `load_next_states_from_url(url1, url2)`: Загружает следующую структуру состояний из внешней базы данных по указанным URL.

# Руководство пользователя

## Пользователи системы

- **Респондент**: пользователь, который проходит анкетирование с помощью голосового помощника. Данный пользователь не является основным в контексте разработки системы.
- **Разработчик голосового помощника**: основной пользователь, который использует инструментальное средство для создания спецификации голосового помощника для анкетирования на платформе Яндекс.Диалогов с использованием языка программирования Python.

## 1. Руководство пользователя респондента

1. **Требования**: Для использования нашего навыка необходимо иметь учетную запись в Яндексе и установленный Яндекс.Браузер с голосовым помощником Алисой.
2. **Иконка Алисы**: Если вышеуказанные условия выполнены, то с левой стороны окна браузера будет отображаться фиолетовый значок Алисы.
3. **Запуск навыка**: Нажмите на значок Алисы. После этого вы можете либо произнести вслух, либо ввести в диалоговое окно фразу: "Запусти навык Анкета Опрос".
   
   ![image](https://github.com/DragonZol/Yandex_survey/assets/116492948/74fe8451-b1a7-4829-9022-73d125cf841a)
   
4. **Начало опроса**: После запуска навыка начнется процесс опроса.

   ![image](https://github.com/DragonZol/Yandex_survey/assets/116492948/3c91d16f-8c9e-4e2e-8d38-e665fb4f73e3)
   
5. **Ответы на вопросы**: Для ответов на заданные вопросы вы можете использовать либо ввод с клавиатуры в поле для ввода, либо голосовой ввод, произнося ответы вслух.
6. **Типы вопросов**:
    - **Открытые вопросы**: Ответы на эти вопросы принимаются по определенному критерию, но не ограничиваются строгими шаблонами. Примеры: ФИО, рост, вес, возраст и т.д. При ответе на открытые вопросы старайтесь давать лаконичные и точные ответы, избегая лишнего контекста.
    - **Закрытые вопросы**: Ответы на эти вопросы предопределены, и вам нужно выбрать один из предложенных вариантов. Пример: "Где вы проживаете? С родителями, снимаете квартиру или в общежитии?".
7. **Пропуск и завершение опроса**: В любой момент опроса вы можете пропустить текущий вопрос или досрочно завершить анкетирование. Для этого просто скажите или напишите в диалоговое окно команду, например: "Пропустить вопрос" или "Закончить анкетирование".
8. **Переспрос вопроса**: Если система не может найти необходимый ответ в вашем сообщении, она переспросит вопрос еще раз и попросит ответить более точно. Важные вопросы, которые нельзя пропустить, будут повторены.
9. **Точность ответов**: Будьте внимательны при прослушивании или прочтении вопросов и старайтесь давать четкие и релевантные ответы. Это поможет системе правильно интерпретировать вашу информацию.
10. **Завершение анкетирования**: После завершения анкетирования система поблагодарит вас за участие, и ваши ответы будут сохранены для дальнейшей обработки.

## 2. Руководство разработчика голосового помощника

Для использования разработанного инструментального средства разработчику голосового помощника необходимо выполнить следующую последовательность действий:

1. **Создание анкеты**: Создайте анкету для опроса респондентов на платформе создания ВА.
2. **Регистрация в системе Яндекс.Диалогов**: Зарегистрируйтесь в системе Яндекс.Диалогов.
3. **Выгрузка интервью**: Выгрузите нужное интервью, в результате чего будет сгенерирован код для голосового помощника.
4. **Создание облачной функции**: Создайте облачную функцию на платформе Яндекса, перепишите сгенерированный код и настройте точки доступа.
5. **Настройка интерфейса**: Настройте спецификации разговорного интерфейса для голосового помощника.
6. **Выгрузка кода**: Выгрузите код спецификации.
7. **Ввод информации**: Введите сгенерированную информацию в соответствующие поля системы Яндекса.

---

Для получения дополнительной информации и подробной документации, пожалуйста, ознакомьтесь с исходным кодом и комментариями в скриптах.

import json
import requests
from upload import upload_json_to_yandex_disk, upload_post
import logging
import random

STATE_REQUEST_KEY = 'session'
STATE_RESPONSE_KEY = 'session_state'


# Функции для работы с Яндекс Диалогами

def make_response(text, buttons=None, state=None):
    response = {'text': text}
    if buttons:
        response['buttons'] = buttons
    
    webhook_response = {'response': response, 'version': '1.0'}
    
    if state is not None:
        webhook_response[STATE_RESPONSE_KEY] = state
    
    return webhook_response


def get_intents(event):
    return event['request']['nlu'].get('intents', {})

def is_new_session(event):
    return event['session']['new']

def is_not_new(state):
    if 'screen' in state:
        return True
    else:
        return False

def get_state(event):
    return event.get('state', {}).get(STATE_REQUEST_KEY, initialize_state())


# Функции для работы с вопросами и состояниями

def load_questions_from_url(url):
    response = requests.get(url)
    data = response.json()

    questions = {}
    for item in data:
        question_key = f"ask_{item['question_id']}"
        questions[question_key] = {
            'text': [item['question_name']]
        }
    print(questions)
    return questions

def load_next_states_from_url(url):
    response = requests.get(url)
    data = response.json()

    next_states = {}
    sorted_data = sorted(data, key=lambda x: x['priority'])

    # Создаем словарь next_states со всеми вопросами
    for item in sorted_data:
        question_key = f"ask_{item['question_id']}"
        next_states[question_key] = {
            'next_state': None,
            'question_type': None,
            'expected_intent': None,
            'slot_to_fill': None,
            'possible_values': [option['option_text'] for option in item['question_options']]
        }

    # Обрабатываем условия и устанавливаем следующие состояния
    for i, item in enumerate(sorted_data):
        question_key = f"ask_{item['question_id']}"

        if item['transition_type'] == 1:
            next_states[question_key]['question_type'] = 'option'
            if i < len(sorted_data) - 1:
                next_question_key = f"ask_{sorted_data[i+1]['question_id']}"
                next_states[question_key]['next_state'] = next_question_key
        elif item['transition_type'] == 2:
            next_states[question_key]['question_type'] = 'conditional'
            next_states[question_key]['conditions'] = []
            next_states[question_key]['next_state'] = {}
            for condition in item['question_conditions']:
                condition_question_key = f"ask_{condition['operand_question_id']}"
                if condition_question_key in next_states:
                    condition_value = next_states[condition_question_key]['possible_values'][condition['q_options'][0]['option_id'] - 1]
                    next_states[question_key]['conditions'].append([
                        {'question': condition_question_key, 'value': condition_value, 'operator': '=='}
                    ])
                    next_question_key = f"ask_{sorted_data[i+1]['question_id']}"
                    next_states[question_key]['next_state']['condition1'] = next_question_key
            if i < len(sorted_data) - 1:
                next_question_key = f"ask_{sorted_data[i+1]['question_id']}"
                next_states[question_key]['next_state']['default'] = next_question_key
            else:
                next_states[question_key]['next_state']['default'] = 'End'
    print(next_states)
    return next_states

    
def load_questions():
    return {
        'welcome_message': {'text': ['Здравствуйте, давайте познакомимся. Как к Вам лучше обращаться?',]},
        'ask_sex': {'text': ['Какой пол мне указать в анкете? М / Ж', 'Укажите, пожалуйста, ваш пол', 'Вы мужчина или женщина?']},
        'ask_age': {'text': ['Сколько Вам лет?', 'Укажите, пожалуйста, ваш возраст', 'Можете назвать свой возраст?']},
        'ask_height_weight': {'text': ['Пожалуйста, назовите свой рост в сантиметрах и вес [Например, 170 см, 60 кг]',]},
        'ask_stud': {'text': ['Вы студент? Какая у вас температура?',]},
        'ask_dom': {'text': ['Подскажите пожалуйста где вы проживаете в настоящее время: в общежитии, снимаете квартиру или с родителями?',]},
        'ask_smoke': {'text': ['Курите ли Вы в настоящее время?',]},
        'ask_tip': {'text': ['Вы курите сигареты или используете альтернативные системы нагревания табака?',]},
        'ask_past': {'text': ['А раньше курили?',]},
        'ask_cigarettes_count': {'text': ['Сколько сигарет или стиков в день Вы выкуриваете?',]},
        'ask_smoking_experience': {'text': ['Вы курите больше года/ровно год или меньше года?',]},
        'ask_smoking_years': {'text': ['Сколько лет вы курите?',]},
        'ask_conditional_question': {'text': ['Да ладно, у меня запустился этот вопрос?',]},
        'ask_question1': {'text': ['Это вопрос для мужчин',]},
        'ask_question2': {'text': ['Это вопрос для девочек',]},
    }


def load_next_states():
    return {
        'welcome_message': {
            'next_state': 'ask_sex',
            'question_type': 'check',
            'expected_intent': 'fio',
            'slot_to_fill': 'slot_fio',
            'question_of_interview_id': 1,
            'question_id': 1
        },
        'ask_sex': {
            'next_state': 'ask_age',
            'question_type': 'option',
            'expected_intent': 'sex',
            'slot_to_fill': 'var_sex',
            'possible_values': [
                {'value': 'male', 'option_id': 1},
                {'value': 'female', 'option_id': 2}
            ],
            'question_of_interview_id': 2,
            'question_id': 2
        },
        'ask_age': {
            'next_state': 'ask_height_weight',
            'question_type': 'check',
            'expected_intent': 'num',
            'slot_to_fill': 'slot_num',
            'question_of_interview_id': 3,
            'question_id': 3
        },
        'ask_height_weight': {
            'next_state': 'ask_stud',
            'question_type': 'check',
            'expected_intent': 'height_weight',
            'slots_to_fill': ['slot_height', 'slot_weight'],
            'question_of_interview_id': 4,
            'question_id': 4
        },
        'ask_stud': {
            'next_state': 'ask_dom',
            'question_type': 'option',
            'expected_intent': 'stud',
            'slots_to_fill': ['var_stud', 'slot_num'],
            'possible_values': [
                {'value': 'stud', 'option_id': 1},
                {'value': 'no_stud', 'option_id': 2}
            ],
            'question_of_interview_id': 5,
            'question_id': 5
        },
        'ask_dom': {
            'next_state': {
                'ob': 'ask_smoke',
                'kvar': 'ask_past',
                'rod': 'ask_smoking_experience'
            },
            'question_type': 'option',
            'expected_intent': 'choose_dom',
            'slots_to_fill': ['var_dom', 'slot_time'],
            'possible_values': [
                {'value': 'ob', 'option_id': 1},
                {'value': 'kvar', 'option_id': 2},
                {'value': 'rod', 'option_id': 3}
            ],
            'question_of_interview_id': 6,
            'question_id': 6
        },
        'ask_smoke': {
            'next_state': 'ask_tip',
            'question_type': 'option',
            'expected_intent': 'smoke',
            'slot_to_fill': 'var_smoke',
            'possible_values': [
                {'value': 'yes_smoke', 'option_id': 1},
                {'value': 'no_smoke', 'option_id': 2}
            ],
            'question_of_interview_id': 7,
            'question_id': 7
        },
        'ask_tip': {
            'next_state': 'ask_cigarettes_count',
            'question_type': 'option',
            'expected_intent': 'kyr',
            'slot_to_fill': 'var_kyr',
            'possible_values': [
                {'value': 'cigarettes', 'option_id': 1},
                {'value': 'vape', 'option_id': 2},
                {'value': 'icos', 'option_id': 3}
            ],
            'question_of_interview_id': 8,
            'question_id': 8
        },
        'ask_past': {
            'next_state': 'ask_cigarettes_count',
            'question_type': 'option',
            'expected_intent': 'past',
            'slot_to_fill': 'var_past',
            'possible_values': [
                {'value': 'yes_past', 'option_id': 1},
                {'value': 'no_past', 'option_id': 2}
            ],
            'question_of_interview_id': 9,
            'question_id': 9
        },
        'ask_cigarettes_count': {
            'next_state': 'ask_smoking_experience',
            'question_type': 'check',
            'expected_intent': 'num',
            'slot_to_fill': 'slot_num',
            'question_of_interview_id': 10,
            'question_id': 10
        },
        'ask_smoking_experience': {
            'next_state': 'ask_smoking_years',
            'question_type': 'option',
            'expected_intent': 'exp',
            'slot_to_fill': 'var_exp',
            'possible_values': [
                {'value': 'more_year', 'option_id': 1},
                {'value': 'less_year', 'option_id': 2}
            ],
            'question_of_interview_id': 11,
            'question_id': 11
        },
        'ask_smoking_years': {
            'next_state': 'ask_conditional_question',
            'question_type': 'check',
            'expected_intent': 'num',
            'slot_to_fill': 'slot_num',
            'question_of_interview_id': 12,
            'question_id': 12
        },
        'ask_conditional_question': {
            'next_state': {
                'condition1': 'ask_question1',
                'condition2': 'ask_question2',
                'default': 'End'
            },
            'question_type': 'conditional',
            'conditions': [
                [
                    {'question': 'ask_sex', 'value': 'male', 'operator': '=='},
                    {'question': 'ask_age', 'value': '18', 'operator': '>='}
                ],
                [
                    {'question': 'ask_sex', 'value': 'female', 'operator': '=='},
                    {'question': 'ask_age', 'value': '18', 'operator': '<'}
                ]
            ],
            'question_of_interview_id': 13,
            'question_id': 13
        },
        'ask_question1': {
            'next_state': 'End',
            'question_type': 'check',
            'expected_intent': 'num',
            'slot_to_fill': 'slot_num',
            'question_of_interview_id': 14,
            'question_id': 14
        },
        'ask_question2': {
            'next_state': 'End',
            'question_type': 'check',
            'expected_intent': 'num',
            'slot_to_fill': 'slot_num',
            'question_of_interview_id': 15,
            'question_id': 15
        }
    }

# Этот вариант загрузки вопросов ещё в доработке
# url = "http://51.250.4.123:5005/getInterviewStructure?id=1"
# questions = load_questions_from_url(url)
# next_states = load_next_states_from_url(url)

# Вариант используемый сейчас
questions = load_questions()
next_states = load_next_states()


def get_current_state(state):
    return state.get('screen')


def get_next_state(cur_state):
    return next_states[cur_state]['next_state']

def compare(actual, expected, operator):
    if operator in ['>=', '<']:  # Если оператор предполагает числовое сравнение
        try:
            actual = int(actual)
            expected = int(expected)
        except ValueError:
            print(f"Error converting {actual} or {expected} to integers.")
            return False
            
    if operator == '==':
        return actual == expected
    elif operator == '>=':
        return actual >= expected
    elif operator == '<':
        return actual < expected
    else:
        print(f"Unknown operator {operator}.")
        return False


def get_conditional_next_state(cur_state, state):
    conditions = next_states[cur_state]['conditions']
    next_states_dict = next_states[cur_state]['next_state']
    
    for i, condition_group in enumerate(conditions, start=1):
        print(f"Checking condition group {i}: {condition_group}")
        all_conditions_passed = True
        
        for condition in condition_group:
            question = condition['question']
            key_to_use = next_states[question].get('slot_to_fill', '') or next_states[question].get('slots_to_fill')
            if isinstance(key_to_use, list):
                key_to_use = key_to_use[0]  # Если есть несколько ключей, используем первый для простоты
                
            actual = state.get(question, {}).get(key_to_use, {}).get('value', '')
            expected = condition['value']
            operator = condition['operator']
            
            print(f"Comparing {actual} {operator} {expected}")
            if not compare(actual, expected, operator):
                all_conditions_passed = False
                print(f"Failed condition: {actual} {operator} {expected}")
                break
        
        if all_conditions_passed:
            print(f"Condition {i} passed, moving to {next_states_dict[f'condition{i}']}")
            return next_states_dict[f'condition{i}']
    
    print("No conditions passed, moving to default")
    return next_states_dict['default']

def get_question_type(cur_state):
    return next_states[cur_state]['question_type']

def get_expected_intent(cur_state):
    return next_states[cur_state]['expected_intent']

def get_slots_to_fill(cur_state):
    return next_states[cur_state].get('slots_to_fill', next_states[cur_state].get('slot_to_fill'))

def get_possible_values(cur_state):
    possible_values = next_states[cur_state].get('possible_values')
    if possible_values:
        return [value['value'] for value in possible_values]
    else:
        return None

def if_stop(intents):
    return 'stop' in intents

def if_skip(intents):
    return 'skip' in intents

def if_was_next(cur_state, intents):
    expected_intent = get_expected_intent(cur_state)
    return expected_intent in intents

def get_value(cur_state, intents):
    expected_intent = get_expected_intent(cur_state)
    slots_to_fill = get_slots_to_fill(cur_state)
    values = {}

    if isinstance(slots_to_fill, str):
        values[slots_to_fill] = intents[expected_intent]['slots'].get(slots_to_fill, {}).get('value')
    else:
        for slot in slots_to_fill:
            values[slot] = intents[expected_intent]['slots'].get(slot, {}).get('value')

    possible_values = get_possible_values(cur_state)
    return values, possible_values

def get_question_text(cur_state, state):
    if state.get('replay', False):
        text = 'Извините, не могли бы вы более точно ответить на вопрос:\n' + random.choice(questions[cur_state]['text'])
        state['replay'] = False
    elif state.get('no_skip', False):
        text = 'Извините, но этот вопрос нельзя пропустить, так как он влияет на следующий. Пожалуйста, ответьте на вопрос:\n' + random.choice(questions[cur_state]['text'])
        state['no_skip'] = False
    else:
        text = random.choice(questions[cur_state]['text'])
    return text


def initialize_state():
    return {'screen': None, 'not_end': None, 'no_skip': False, 'replay': False}


# Функции для обработки ответов пользователя

def format_answers(state):
    answers = []
    for question_key, answer_data in state.items():
        if question_key in next_states:
            question_of_interview_id = next_states[question_key]['question_of_interview_id']
            question_id = next_states[question_key]['question_id']
            
            if answer_data is not None:
                if isinstance(answer_data, dict):
                    option_id = None
                    answer_text = None
                    
                    for key, value_data in answer_data.items():
                        if 'possible_values' in next_states[question_key] and value_data['value'] in [val['value'] for val in next_states[question_key]['possible_values']]:
                            option_id = [val['option_id'] for val in next_states[question_key]['possible_values'] if val['value'] == value_data['value']]
                        else:
                            if value_data['value'] is not None:
                                if answer_text is None:
                                    answer_text = [value_data['value']]
                                else:
                                    answer_text.append(value_data['value'])
                    
                    if option_id:
                        answers.append({
                            "question_of_interview_id": question_of_interview_id,
                            "question_id": question_id,
                            "option_id": option_id,
                            "answer_text": answer_text,
                            "special_answer_type": None
                        })
                    else:
                        answers.append({
                            "question_of_interview_id": question_of_interview_id,
                            "question_id": question_id,
                            "option_id": None,
                            "answer_text": answer_text,
                            "special_answer_type": None
                        })
                else:
                    answers.append({
                        "question_of_interview_id": question_of_interview_id,
                        "question_id": question_id,
                        "option_id": None,
                        "answer_text": None,
                        "special_answer_type": None
                    })
            else:
                answers.append({
                    "question_of_interview_id": question_of_interview_id,
                    "question_id": question_id,
                    "option_id": None,
                    "answer_text": None,
                    "special_answer_type": 3
                })
    
    return answers

def process_stop_intent(state, cur_state, event):
    state['not_end'] = cur_state
    state['screen'] = 'End'
    return ask_question(state, event)

def process_skip_intent(state, cur_state, event):
    if next_states.get(cur_state):
        next_state = get_next_state(cur_state)
        if isinstance(next_state, dict):
            state['no_skip'] = True
            state['screen'] = cur_state
            return ask_question(state, event)
        else:
            state[cur_state] = None
            state['screen'] = next_state
            return ask_question(state, event)
    else:
        state['no_skip'] = True
        state['screen'] = cur_state
        return ask_question(state, event)

def process_check_question(state, cur_state, intents, event):
    next_state = get_next_state(cur_state)

    if if_was_next(cur_state, intents):
        values, _ = get_value(cur_state, intents)
        if cur_state not in state:
            state[cur_state] = {}
        for slot, value in values.items():
            state[cur_state][slot] = {
                'value': value,
                'type': 'text'
            }
        state['screen'] = next_state
        return ask_question(state, event)
    else:
        state['replay'] = True
        state['screen'] = cur_state
        return ask_question(state, event)


def process_option_question(state, cur_state, intents, event):
    if if_was_next(cur_state, intents):
        values, possible_values = get_value(cur_state, intents)
        slots_to_fill = get_slots_to_fill(cur_state)

        if cur_state not in state:
            state[cur_state] = {}

        if isinstance(slots_to_fill, str):
            value = list(values.values())[0]
            if possible_values is not None:
                if value in possible_values:
                    state[cur_state][slots_to_fill] = {
                        'value': value,
                        'type': 'option',
                        'option_id': [val['option_id'] for val in next_states[cur_state]['possible_values'] if val['value'] == value]
                    }
                    if isinstance(get_next_state(cur_state), dict):
                        next_state = get_next_state(cur_state)[value]
                    else:
                        next_state = get_next_state(cur_state)
                    state['screen'] = next_state
                    return ask_question(state, event)
            else:
                state[cur_state][slots_to_fill] = {
                    'value': value,
                    'type': 'text'
                }
                next_state = get_next_state(cur_state)
                state['screen'] = next_state
                return ask_question(state, event)
        else:
            for slot in slots_to_fill:
                if slot in values:
                    state[cur_state][slot] = {
                        'value': values[slot],
                        'type': 'text'
                    }
            next_state = get_next_state(cur_state)
            if isinstance(next_state, dict):
                selected_value = state[cur_state][slots_to_fill[0]]['value']
                state['screen'] = next_state[selected_value]
            else:
                state['screen'] = next_state
            return ask_question(state, event)
    else:
        state['replay'] = True
        state['screen'] = cur_state
        return ask_question(state, event)
    
def process_conditional_question(state, cur_state, intents, event):
    next_state = get_conditional_next_state(cur_state, state)
    state['screen'] = next_state
    return ask_question(state, event)

def validate_answer(state, intents, cur_state, event):
    question_type = get_question_type(cur_state)
    if if_stop(intents):
        return process_stop_intent(state, cur_state, event)
    elif if_skip(intents):
        return process_skip_intent(state, cur_state, event)
    elif question_type == 'check':
        return process_check_question(state, cur_state, intents, event)
    elif question_type == 'option':
        return process_option_question(state, cur_state, intents, event)
    elif question_type == 'conditional':
        return process_conditional_question(state, cur_state, intents, event)
    else:
        return make_response('Некорректный ответ. Пожалуйста, попробуйте еще раз.', state=state)

# Основные функции

def first_question(state):
    first_question_key = next(iter(questions))
    return make_response(random.choice(questions[first_question_key]['text']), state={'screen': first_question_key} if not state.get('screen') else state)


def ask_question(state, event):
    cur_state = get_current_state(state)
    if cur_state == 'End':
        user_id = event['session']['user_id']
        interview_result = {
            "interview_result": {
                "interview_id": 1,
                "user_id": 1,
                "user_platform_name": user_id,
                "answers": format_answers(state)
            }
        }
        upload_json_to_yandex_disk(interview_result)
        upload_post(interview_result)
        return make_response('Спасибо, анкетирование окончено, файлы сохранены', state=state)
    else:
        if cur_state in questions:
            text = get_question_text(cur_state, state)
            return make_response(text, state=state)
        else:
            return make_response('Вопрос не найден.', state=state)


def handler(event, context):
    state = get_state(event)
    intents = get_intents(event)

    if is_new_session(event):
        return first_question(state)
    elif is_not_new(state):
        cur_state = get_current_state(state)
        return validate_answer(state, intents, cur_state, event)
    elif next_states[state.get('screen')] == 'End':
        return make_response('Спасибо за прохождение анкетирования!', state=state)


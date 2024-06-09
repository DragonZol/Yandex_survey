import json
import requests
from upload import upload_json_to_yandex_disk, upload_post
from generator import load_questions_from_url, load_next_states_from_url
from manually_configured_questions import load_questions, load_next_states
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


# # Этот вариант загрузки вопросов ещё в доработке
# url1 = "http://51.250.4.123:5005/getInterviewStructure?id=1"
# url2 = "http://51.250.4.123:5005/getInterviewCUI?id=1"
# questions = load_questions_from_url(url1)
# next_states = load_next_states_from_url(url1,url2)

# # Вариант используемый сейчас
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


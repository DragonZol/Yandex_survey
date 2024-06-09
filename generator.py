import json
import requests

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

def load_next_states_from_url(url1, url2):
    response1 = requests.get(url1)
    data1 = response1.json()

    response2 = requests.get(url2)
    data2 = response2.json()

    next_states = {}
    sorted_data = sorted(data1, key=lambda x: x['priority'])

    # Создаем словарь для сопоставления question_id и данных из второго JSON
    question_data_map = {item['question_id']: item for item in data2}

    # Создаем словарь next_states со всеми вопросами
    for item in sorted_data:
        question_key = f"ask_{item['question_id']}"
        question_data = question_data_map.get(item['question_id'], {})
        next_states[question_key] = {
            'next_state': None,
            'question_type': None,
            'expected_intent': question_data.get('intent_id'),
            'slot_to_fill': question_data.get('slots', [{}])[0].get('name'),
            'possible_values': [
                {'value': value['value'], 'option_id': value['option_id']}
                for value in question_data.get('slots', [{}])[0].get('values', [])
            ],
            'question_of_interview_id': item['question_of_interview_id'],
            'question_id': item['question_id']
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
                    condition_value = next_states[condition_question_key]['possible_values'][condition['q_options'][0]['option_id'] - 1]['value']
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
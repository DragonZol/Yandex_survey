def load_questions():
    return {
        'welcome_message': {'text': ['Здравствуйте, давайте познакомимся. Как к Вам лучше обращаться?',]},
        'ask_sex': {'text': ['Какой пол мне указать в анкете? М / Ж', 'Укажите, пожалуйста, ваш пол', 'Вы мужчина или женщина?']},
        'ask_age': {'text': ['Сколько Вам лет?', 'Укажите, пожалуйста, ваш возраст', 'Можете назвать свой возраст?']},
        'ask_height_weight': {'text': ['Пожалуйста, назовите свой рост в сантиметрах и вес [Например, 170 см, 60 кг]',]},
        'ask_stud': {'text': ['Вы студент?',]},
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
            'slots_to_fill': ['var_stud'],
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
            'slots_to_fill': ['var_dom'],
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
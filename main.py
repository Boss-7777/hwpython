"""
Это программа для викторины
Для участия вы должны ввести "да"
В противоположном случае введите "нет"
На каждом вопросе, вам нужно будет выбрать вариант ответа, который вам по душе
В конце викторины вы узнаете на какаого персонажа из "Смешариков вы наиболее похожи"
"""

def isnumber(s):
    """
    функция, проверяющая, что s является числом
    """
    if s.startswith('-'):
        s = s[1:]
    return s.isdecimal()

def parse_data():
    """
    функция, считывающая данные по вопросам из файла
    """
    questions = {}  # создаем словарь который хранит вопросы и ответы на викторину
    characters = []
    # считываем с файла вопросы и коэффициенты
    with open('Quiz_Data.csv', 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.split(';')  # каждую строку разбиваем в массив с нашими данными
            line = [value.strip() for value in line]  # очищаем данные от пробелов и отступов

            if line[0]:  # проверка на конец данных в csv файле
                number, question, answer, coeffs = line[0], line[1], line[2], line[3:]
                if not isnumber(number):
                    characters = coeffs
                else:
                    coeffs = list(map(lambda x: float(x.replace(',', '.')), coeffs))
                    if question in questions:
                        questions[question]["answers"].append((answer, coeffs))
                    else:
                        questions[question] = {
                            "number": int(number),
                            "answers": [(answer, coeffs)]
                        }
            else:
                break
    # Выполняем сортировку на случай если в файле вопросы расположены в неправильном порядке
    questions = dict(sorted(questions.items(), key=lambda item: item[1]["number"]))
    return questions, characters

def quiz():
    """
    Функция запускающая викторину
    """
    questions, characters = parse_data() # запускаем функцию считывания данных

    print('Добро пожаловать на викторину!')
    characters_scores = [0.0] * len(characters)  # создаем массив очков каждого персонажа
    for question, question_info  in questions.items():  # бежим по словарю вопросов
        print(question)  # выводим на экран вопрос

        variants = {}
        # бежим по вариантам ответов и выводим их
        for i, variant in enumerate(question_info['answers'], 1):
            variants[i] = variant[0]
            print(f"{i}. {variant[0]}")

        print('Пожалуйста введите номер ответа')
        while True:
            answer = input()  # считываем написанный ответ
            if not isnumber(answer):  # проверяем, если данный ответ, является числом
                print('Пожалуйста введите номер ответа без скобки')
                continue
            answer = int(answer)  # конвертируем значение ответ в тип int
            if answer not in variants:  # если такого варианта ответа нет, выводим ошибку
                print('Такого варианта ответа нет, попробуйте еще раз')
                continue
            # берем очки ответа из словаря вопросов
            answer_coeffs = question_info['answers'][answer - 1][1]
            # складываем очки ответа с уже имеющимися в массиве
            characters_scores = [sum(x) for x in zip(characters_scores, answer_coeffs)]
            break

    max_score = max(characters_scores)
    max_score_index = characters_scores.index(max_score)
    character = characters[max_score_index] # Определяем какой персонаж в сумме набрал больше баллов
    # выводим финальное количество баллов, которое набрал участник
    print(f'Поздравляем, вы {character}!')


if __name__ == "__main__":
    print('Здравствуйте!Хотите ли принять участие в нашей викторине?')  # приветсвенная речь
    participation = ''
    # викторинаPcu не начнется, пока участник не ответит, хочет он или не хочет участвовать в ней
    while participation.lower() not in ('да', 'нет'):
        print('Пожалуйста введите "да" или "нет"')
        participation = input()
    participation = True if participation == 'да' else False
    # если участник ответил "да", начинается викторина
    if participation:
        quiz()
    # благодарим за участие и желаем удачи на экзаменах
    print('Спасибо за участие!' if participation else 'Ну что ж, в другой раз)')
    print('Удачи на экзаменах ;)')

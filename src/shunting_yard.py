#! env python3
from src.tokenizator import is_number, get_tok

# Таблица приоритетов операторов
# Чем выше число, тем выше приоритет
prio = {'+': 1, '-': 1, '*': 2, '/': 2, '//': 2, '%': 2, '**': 3, '$': 4, '~': 4}

# Таблица ассоциативности операторов
# 'left' - лево-ассоциативные, 'right' - право-ассоциативные
associativity = {'+': 'left', '-': 'left', '*': 'left', '/': 'left', '//': 'left', '%': 'left', '**': 'right',
                 '$': 'left', '~': 'left'}


def is_op_tok(tok):
    """Проверяет, является ли токен бинарной операцией"""
    return tok in ['+', '-', '*', '/', '**', '%', '//']


def is_op(tok):
    """Проверяет, является ли токен любой операцией (включая унарные)"""
    return tok in ['+', '-', '*', '/', '**', '%', '//', '~', '$']


def translate_indx_to_rpn(expr):
    """
    Преобразует инфиксное выражение в обратную польскую нотацию
    используя алгоритм Shunting Yard
    """
    result = []  # Выходная очередь для RPN
    op_stack = []  # Стек для операторов и скобок
    old_tok = None  # Предыдущий токен для проверки контекста

    # Удаляем пробелы для упрощения обработки
    expr = expr.replace(' ', '')

    while expr:
        # Получаем следующий токен
        tok, expr = get_tok(expr)

        if tok == '':
            break

        # Если токен - число, добавляем в выходную очередь
        if tok.replace('.', '').isdigit():
            result.append(tok)
            old_tok = tok
            continue

        # Проверки на синтаксические ошибки:

        # Два бинарных оператора подряд
        if is_op_tok(old_tok) and is_op_tok(tok):
            raise ValueError(f'2 бинарных знака подряд: "{old_tok}", "{tok}"')

        # Пропущен оператор между скобками
        if old_tok == ')' and tok == '(':
            raise ValueError(f'Пропущен оператор между скобкой и скобкой: "{old_tok}", "{tok}"')

        # Пропущен оператор между числом и открывающей скобкой
        if is_number(old_tok) and tok == '(':
            raise ValueError(f'Отсутствие бинарного знака между числом и скобкой: "{old_tok}", "{tok}"')

        # Пропущен оператор между закрывающей скобкой и числом
        if is_number(tok) and old_tok == ')':
            raise ValueError(f'Отсутствие бинарного знака между скобкой и числом: "{old_tok}", "{tok}"')

        # Обработка унарных операторов + и -
        if tok in '-+':
            # Унарный, если в начале или после открывающей скобки
            if old_tok == '(' or old_tok is None:
                # Заменяем на специальные символы для унарных операций
                tok = tok.replace('-', '~').replace('+', '$')
                op_stack.append(tok)
                old_tok = tok
                continue

        # Обработка бинарных операторов
        if is_op(tok):
            # Извлекаем операторы из стека согласно приоритетам и ассоциативности
            while ((op_stack and is_op(op_stack[-1]) and (prio[op_stack[-1]] >= prio[tok]) and
                    associativity[tok] == 'left') or
                   (op_stack and is_op(op_stack[-1]) and (prio[op_stack[-1]] > prio[tok]) and
                    associativity[tok] == 'right')):
                result.append(op_stack.pop())
            op_stack.append(tok)
            old_tok = tok
            continue

        # Обработка открывающей скобки
        if tok == '(':
            op_stack.append(tok)
            old_tok = op_stack[-1]
            continue

        # Обработка закрывающей скобки
        if tok == ')':
            # Извлекаем все операторы до открывающей скобки
            while op_stack and op_stack[-1] != '(':
                if '(' not in op_stack:
                    raise ValueError(f'Закрытая скобка без открытой')
                result.append(op_stack.pop())
            # Удаляем открывающую скобку
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
            old_tok = tok
            continue

        # Неизвестный токен
        raise ValueError(f'Ты что такое ввёл??? "{tok}"')

    # Извлекаем оставшиеся операторы из стека
    while op_stack:
        if op_stack[-1:] == '(':
            raise ValueError(f'Незакрытая скобка')
        result.append(op_stack.pop())

    return result
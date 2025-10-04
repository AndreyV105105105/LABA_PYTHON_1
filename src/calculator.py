#! env python3

from src.shunting_yard import translate_indx_to_rpn
from src.shunting_yard import is_op

def calc(expr):
    """
    Основная функция калькулятора.
    Принимает строку с математическим выражением, возвращает результат вычисления.
    """
    stack = []  # Стек для вычисления RPN

    # Преобразуем выражение в обратную польскую нотацию
    expr = translate_indx_to_rpn(expr)

    # Вычисляем выражение в RPN формате
    for tok in expr:
        # Если токен - число, добавляем в стек
        if not is_op(tok):
            if tok.isdigit():
                stack.append(int(tok))  # Целое число
            else:
                stack.append(float(tok))  # Вещественное число

        # Если токен - оператор
        if is_op(tok):
            # Обработка унарных операторов
            if tok in '~$':
                if not stack:
                    raise ValueError(f'Не хватает операндов')
                else:
                    unar_stack_element = stack.pop()
                    if tok == '~':  # Унарный минус
                        stack.append(-unar_stack_element)
                    else:  # Унарный плюс
                        stack.append(+unar_stack_element)
            # Обработка бинарных операторов
            else:
                # Извлекаем два операнда из стека
                op1 = stack.pop()
                op2 = stack.pop()
                if op1 is None or op2 is None:
                    raise ValueError(f'Не хватает операндов')

                res = None
                # Выполняем операцию в зависимости от типа оператора
                match tok:
                    case '+':
                        res = op2 + op1
                    case '-':
                        res = op2 - op1
                    case '*':
                        res = op2 * op1
                    case '/':
                        if op1 == 0:
                            raise ValueError(f'ДЕЛИТЬ НА 0 НЕЛЬЗЯ')
                        res = op2 / op1
                    case '//':
                        if op1 == 0:
                            raise ValueError(f'ДЕЛИТЬ НА 0 НЕЛЬЗЯ')
                        res = op2 // op1
                    case '%':
                        if op1 == 0:
                            raise ValueError(f'ДЕЛИТЬ НА 0 НЕЛЬЗЯ')
                        res = op2 % op1
                    case '**':
                        res = op2 ** op1
                # Кладем результат обратно в стек
                stack.append(res)
        expr = expr[1:]

    # Получаем конечный результат
    answer = stack.pop()

    # Проверяем, что стек пуст (нет лишних чисел)
    if not stack:
        return answer
    else:
        return "Syntax error"


class ValueError(Exception):
    """Кастомный класс ошибки для калькулятора"""
    pass
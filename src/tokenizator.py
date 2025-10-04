import string


def is_number(tok):
    """Проверяет, является ли символ частью числа (цифра или точка)"""
    return tok in list('0123456789.')


def get_tok(expr):
    """
    Токенизатор - разбивает строку выражения на отдельные токены.
    Возвращает кортеж (токен, оставшаяся_строка)
    """
    # Пропускаем начальные пробелы
    expr = expr.lstrip()

    # Проверяем двухсимвольные операторы (** и //)
    if expr[:2] == '**' or expr[:2] == '//':
        return expr[:2], expr[2:]

    # Обработка чисел (целых и вещественных)
    if is_number(expr[:1]):
        final_index = 0
        # Находим конец числа
        while final_index < len(expr) and is_number(expr[final_index]):
            final_index += 1
        return expr[:final_index], expr[final_index:]

    # Конец строки
    if not expr:
        return None, None

    # Односимвольные токены (операторы, скобки)
    return expr[:1], expr[1:]
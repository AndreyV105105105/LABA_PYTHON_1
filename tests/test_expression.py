import pytest
from src.calculator import calc as calculate, ValueError


class TestM2Calculator:
    """Тесты для калькулятора M2 с ограниченными унарными операторами"""

    def test_basic_operations(self):
        """Тест базовых операций без скобок"""
        assert calculate("2 + 3") == 5
        assert calculate("5 - 2") == 3
        assert calculate("3 * 4") == 12
        assert calculate("10 / 2") == 5
        assert calculate("7 // 2") == 3
        assert calculate("7 % 3") == 1
        assert calculate("2 ** 3") == 8

    def test_operator_priority(self):
        """Тест приоритета операторов"""
        assert calculate("2 + 3 * 4") == 14  # 2 + (3*4) = 14
        assert calculate("2 * 3 + 4") == 10  # (2*3) + 4 = 10
        assert calculate("10 - 2 ** 3") == 2  # 10 - 8 = 2
        assert calculate("2 ** 2 ** 3") == 256  # 2^(2^3) = 256

    def test_parentheses(self):
        """Тест выражений со скобками"""
        assert calculate("(2 + 3) * 4") == 20
        assert calculate("2 * (3 + 4)") == 14
        assert calculate("(1 + 2) * (3 + 4)") == 21
        assert calculate("((2 + 3) * 4)") == 20
        assert calculate("2 ** (1 + 2)") == 8

    def test_complex_parentheses(self):
        """Тест сложных выражений со скобками"""
        assert calculate("(3 + 4) * (2 - 1)") == 7
        assert calculate("(10 - (2 + 3)) * 2") == 10
        assert calculate("2 * (3 + (4 * (5 - 2)))") == 30


    def test_unary_operators_in_parentheses(self):
        """Тест унарных операторов внутри скобок"""
        assert calculate("(-5)") == -5
        assert calculate("(+3)") == 3
        assert calculate("(-2) * 3") == -6
        assert calculate("(-2) * (-3)") == 6
        assert calculate("(+2) * (+3)") == 6
        assert calculate("2 * (-3)") == -6
        assert calculate("2 + (-3)") == -1

    def test_complex_unary_in_parentheses(self):
        """Тест сложных выражений с унарными операторами в скобках"""
        assert calculate("(-(-3))") == 3
        assert calculate("(-(2 + 3))") == -5
        assert calculate("(-(2 * 3))") == -6
        assert calculate("(+(-3))") == -3
        assert calculate("2 + (-(-3))") == 5
        assert calculate("(-5) + (+3)") == -2

    def test_unary_operators_not_allowed_outside_parentheses(self):
        """Тест что унарные операторы НЕ разрешены вне скобок"""
        # Эти выражения должны вызывать ошибку
        with pytest.raises(ValueError):
            calculate("-5")

        with pytest.raises(ValueError):
            calculate("+3")

        with pytest.raises(ValueError):
            calculate("2 + -3")

        with pytest.raises(ValueError):
            calculate("2 * -3")

        with pytest.raises(ValueError):
            calculate("-2 * 3")

    def test_float_numbers(self):
        """Тест с вещественными числами"""
        assert calculate("2.5 + 3.5") == 6.0
        assert calculate("3.0 * 2.5") == 7.5
        assert calculate("10.0 / 4.0") == 2.5
        assert calculate("2.5 * (1.5 + 2.5)") == 10.0
        assert calculate("(-2.5)") == -2.5
        assert calculate("(+1.5)") == 1.5

    def test_right_associativity(self):
        """Тест право-ассоциативности оператора **"""
        assert calculate("2 ** 3 ** 2") == 512  # 2^(3^2) = 2^9 = 512
        assert calculate("(2 ** 3) ** 2") == 64  # (2^3)^2 = 8^2 = 64
        assert calculate("2 ** (-1)") == 0.5  # 2^(-1) = 0.5

    def test_division_by_zero(self):
        """Тест деления на ноль"""
        with pytest.raises(ValueError, match="Деление на ноль"):
            calculate("5 / 0")

        with pytest.raises(ValueError, match="Деление на ноль"):
            calculate("10 // 0")

        with pytest.raises(ValueError, match="Деление на ноль"):
            calculate("5 / (2 - 2)")

    def test_integer_division_modulo_float(self):
        """Тест, что // и % работают только с целыми"""
        with pytest.raises(ValueError, match="Операция // допустима только для целых чисел"):
            calculate("5.5 // 2")

        with pytest.raises(ValueError, match="Операция % допустима только для целых чисел"):
            calculate("5.5 % 2")

        with pytest.raises(ValueError, match="Операция // допустима только для целых чисел"):
            calculate("(5.5) // 2")

    def test_unbalanced_parentheses(self):
        """Тест несбалансированных скобок"""
        with pytest.raises(ValueError, match="Несбалансированные скобки"):
            calculate("(2 + 3")

        with pytest.raises(ValueError, match="Несбалансированные скобки"):
            calculate("2 + 3)")

        with pytest.raises(ValueError, match="Несбалансированные скобки"):
            calculate("((2 + 3)")

        with pytest.raises(ValueError, match="Несбалансированные скобки"):
            calculate("((-3)")

    def test_invalid_syntax(self):
        """Тест некорректного синтаксиса"""
        with pytest.raises(ValueError):
            calculate("2 + + 3")

        with pytest.raises(ValueError):
            calculate("* 2 + 3")

        with pytest.raises(ValueError):
            calculate("2 2 + 3")

        with pytest.raises(ValueError):
            calculate("(-)")  # Унарный оператор без числа

    def test_complex_expressions(self):
        """Тест комплексных выражений"""
        assert calculate("3 + 4 * 2 / ((1 - 5)) ** 2") == 3.5
        assert calculate("(-2) + 3 * (4 - 1)") == 7
        assert calculate("(2 + 3) * ((4 - 1)) ** 2") == 45
        assert calculate("2 * (-3) + 4 * (-2)") == -14
        assert calculate("((-2)) * ((-3)) + ((-4))") == 2

    def test_edge_cases(self):
        """Тест граничных случаев"""
        assert calculate("0") == 0
        assert calculate("0 * 5") == 0
        assert calculate("5 + 0") == 5
        assert calculate("1 ** 0") == 1
        assert calculate("0 ** 5") == 0
        assert calculate("1 ** 100") == 1
        assert calculate("(0)") == 0
        assert calculate("(+0)") == 0
        assert calculate("(-0)") == 0

    def test_whitespace_handling(self):
        """Тест обработки пробелов"""
        assert calculate("  2  +  3  ") == 5
        assert calculate("2+3") == 5
        assert calculate("( 2 + 3 ) * 4") == 20
        assert calculate("( -3 )") == -3
        assert calculate("(  +  2  )") == 2



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
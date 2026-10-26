import pytest

def sum_numbers(*args):
    if not args:
        return 0
    return sum(args)

@pytest.fixture(params=[
    pytest.param(([5, 10], 15), id="two_positive"),
    pytest.param(([10, -5, 3], 8), id="mixed_signs"),
    pytest.param(([0, 0, 5, -2], 3), id="with_zeros_and_neg"),
    pytest.param(([42], 42), id="single_number"),
    pytest.param(([0, 0, 0], 0), id="all_zeros"),
])
def test_data(request):
    return request.param


def test_addition_with_fixture(test_data):
    numbers, expected = test_data
    result = sum_numbers(*numbers)
    assert result == expected, f"Ожидалось {expected}, получено {result} для чисел {numbers}"


def test_specific_positive_numbers(test_data):
    numbers, expected = test_data
    all_non_negative = all(n >= 0 for n in numbers)
    if all_non_negative:
        result = sum_numbers(*numbers)
        assert result == expected, f"Ошибка суммы для положительных чисел {numbers}"


def test_mixed_signs_numbers(test_data):
    numbers, expected = test_data
    has_positive = any(n > 0 for n in numbers)
    has_negative = any(n < 0 for n in numbers)

    if has_positive and has_negative:
        result = sum_numbers(*numbers)
        assert result == expected, f"Ошибка суммы для чисел с разными знаками {numbers}"


def test_with_zeros(test_data):
    numbers, expected = test_data

    if 0 in numbers:
        result = sum_numbers(*numbers)
        assert result == expected, f"Ошибка суммы при наличии нулей в данных {numbers}"

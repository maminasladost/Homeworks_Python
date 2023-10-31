from one_hot_encoder import fit_transform
import pytest


def test_tuple_strings():
    actual = ('Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna')
    expected = [('Bob', [0, 0, 0, 0, 1]), ('Anna', [0, 0, 0, 1, 0]),
                ('Chris', [0, 0, 1, 0, 0]), ('Dan', [0, 1, 0, 0, 0]),
                ('Emily', [1, 0, 0, 0, 0]), ('Chris', [0, 0, 1, 0, 0]),
                ('Anna', [0, 0, 0, 1, 0])]
    assert fit_transform(actual) == expected


def test_list_strings():
    actual = ['Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna']
    expected = [('Bob', [0, 0, 0, 0, 1]), ('Anna', [0, 0, 0, 1, 0]),
                ('Chris', [0, 0, 1, 0, 0]), ('Dan', [0, 1, 0, 0, 0]),
                ('Emily', [1, 0, 0, 0, 0]), ('Chris', [0, 0, 1, 0, 0]),
                ('Anna', [0, 0, 0, 1, 0])]
    assert fit_transform(actual) == expected


def test_empty_arg():
    with pytest.raises(TypeError):
        fit_transform()


def test_numbers():
    actual = [555, 777, 999, 555, 777]
    expected = [(555, [0, 0, 1]), (777, [0, 1, 0]),
                (999, [1, 0, 0]), (555, [0, 0, 1]), (777, [0, 1, 0])]
    assert fit_transform(actual) == expected


def test_no_additional_info():
    actual = ['Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna']
    result = fit_transform(actual)
    assert ('Nikitos', [1, 0, 0, 0, 0]) not in result


if __name__ == '__main__':
    print('Vse Baldezhno')

from one_hot_encoder import fit_transform
import unittest


class TestFitTransform(unittest.TestCase):

    def test_tuple_strings(self):
        """
        Проверяем, что функция корректно работает при передаче tuple
        """
        actual = ('Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna')
        result = fit_transform(actual)
        expected = [('Bob', [0, 0, 0, 0, 1]), ('Anna', [0, 0, 0, 1, 0]),
                    ('Chris', [0, 0, 1, 0, 0]), ('Dan', [0, 1, 0, 0, 0]),
                    ('Emily', [1, 0, 0, 0, 0]), ('Chris', [0, 0, 1, 0, 0]),
                    ('Anna', [0, 0, 0, 1, 0])]
        self.assertEqual(result, expected)

    def test_list_strings(self):
        """
        Проверяем, что функция корректно работает при передаче листа
        """
        actual = ['Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna']
        result = fit_transform(actual)
        expected = [('Bob', [0, 0, 0, 0, 1]), ('Anna', [0, 0, 0, 1, 0]),
                    ('Chris', [0, 0, 1, 0, 0]), ('Dan', [0, 1, 0, 0, 0]),
                    ('Emily', [1, 0, 0, 0, 0]), ('Chris', [0, 0, 1, 0, 0]),
                    ('Anna', [0, 0, 0, 1, 0])]
        self.assertEqual(result, expected)

    def test_empty_arg(self):
        """
        Проверяем, что функция вызывает TypeError (перехват исключения),
        если в функцию ничего не передается
        """
        with self.assertRaises(TypeError):
            fit_transform()

    def test_numbers(self):
        """
        Проверяем, что функция правильно работает с числами
        """
        actual = [555, 777, 999, 555, 777]
        result = fit_transform(actual)
        expected = [(555, [0, 0, 1]), (777, [0, 1, 0]),
                    (999, [1, 0, 0]), (555, [0, 0, 1]), (777, [0, 1, 0])]
        self.assertEqual(result, expected)

    def test_no_additional_info(self):
        """
        Проверяем, что функция не выдает ничего лишнего
        """
        actual = ['Bob', 'Anna', 'Chris', 'Dan', 'Emily', 'Chris', 'Anna']
        result = fit_transform(actual)
        self.assertNotIn(('Nikitos', [1, 0, 0, 0, 0]), result)


if __name__ == '__main__':
    with open('result.txt', 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        unittest.main(testRunner=runner)

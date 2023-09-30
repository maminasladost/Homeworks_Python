import csv  # чтение csv
import codecs  # исправление проблем с кодировкой csv
import urllib.request  # скачивание файлов по ссылке


def load_csv(url: str = ('https://stepik.org/media/attachments/'
                         'lesson/578270/Corp_Summary.csv')) -> dict:
    """Загружает csv файл по ссылке и преобразует его в список,
    где каждый элемент это список с фрагментами записи в отчет.
    Этот список можно интерпретировать просто как таблицу

    Args:
        url (str, optional): Ссылка на скачивание файла.
            Defaults to ('https://stepik.org/media/attachments/'
                        lesson/578270/Corp_Summary.csv').

    Returns:
        dict: Список формата:
            [['Кузьмина Любовь Феликсовна', 'Разработка',
            'Внутренний портал', 'Backend-инженер',
            '4.5', '89000'], ...]

            Первым элементом списка являются названия столбцов таблицы:
                ['ФИО полностью', 'Департамент', 'Отдел', 'Должность',
                'Оценка', 'Оклад']
    """
    response = urllib.request.urlopen(url)
    raw_data = response.read().decode('utf-8')

    with codecs.open('data.csv', 'w', 'utf-8') as file:
        file.write(raw_data)

    with codecs.open('data.csv', 'r', 'utf-8') as file:
        reader = csv.reader(file)
        data = [''.join(row).split(';') for row in reader]

    return data


def print_table(data: list) -> None:
    """Печатает таблицу по списку,
    в которой названия столбцов - это первый элемент,
    а все последующие - это строки таблицы.

    Args:
        data (list): выводит на экран таблицу
    """
    # считаем максимальные длины для каждой строки
    lengths = [max(len(str(row[i])) for row in data)
               for i in range(len(data[0]))]

    print('\n')

    # выводим названия столбцов, разделенные ' | '
    print(
        ' | '.join(
            f'{data[0][i]:^{lengths[i]}}' for i in range(len(data[0]))
        )
    )

    # рисуем разделительную полоску
    print('-'.join('-' * length for length in lengths))

    # выводим строчки таблицы с разделителем ' | '
    for row in data[1:]:
        print(
            ' | '.join(
                f'{str(cell):^{lengths[idx]}}' for idx, cell in enumerate(row)
            )
        )
    print('\n')


def get_all_rows(data: list, column: str) -> list:
    """возвращает все строки исходной таблицы с данными для конкретного столбца

    Args:
        data (list): исходная таблица с данными
        column (str): название столбца

    Returns:
        list: список, в котором находятся строки для
            определенного столбца таблицы
    """
    return [data[i][data[0].index(column)] for i in range(len(data[1:]))][1:]


def get_hierarchy(data: list) -> list:
    """возвращает департамент и все отделы, которые входят в него

    Args:
        data (list): исходная таблица

    Returns:
        list: возвращает новую таблицу в формате:
            [['Название Департамента', 'Отдел1, Отдел2, ...'], ...]
        Названия столбцов для первой таблицы: ['Департамент', 'Отделы']
    """
    all_departments = get_all_rows(data, 'Департамент')
    all_teams = get_all_rows(data, 'Отдел')

    dep_teams = sorted(set(zip(all_departments, all_teams)))
    hierarchy = [['Департамент', 'Отделы']]

    for department in sorted(set(dep for dep, _ in dep_teams)):
        teams = ', '.join(
            team for dep_, team in dep_teams if dep_ == department)
        hierarchy.append([department, teams])

    return hierarchy


def get_departments_summary(data: list) -> list:
    """Возвращает сводный отчет по департаментам,
        основываясь на исходной таблице

    Args:
        data (list): исходная таблица

    Returns:
        list: Новая таблица со столбцами:
            ['Департамент', 'Численность',
               'Минимальная з/п', 'Максимальная з/п', 'Средняя з/п']
            Строками таблицы будут являться расчитанные показатели
    """

    unique_departments = sorted(set(get_all_rows(data, 'Департамент')))
    # переводим все зарплаты в числовой формат для подсчета статистик
    wages = list(map(int, get_all_rows(data, 'Оклад')))
    summary = [['Департамент', 'Численность',
               'Минимальная з/п', 'Максимальная з/п', 'Средняя з/п']]

    for department in unique_departments:
        # индексы строк для работников из каждого департамента
        indices = [i for i, x in enumerate(
            get_all_rows(data, 'Департамент')) if x == department]
        # зарплаты работников из каждого департамента
        wages_by_department = [wages[i]
                               for i, x in enumerate(wages) if i in indices]
        summary.append(
            [
                department,
                get_all_rows(data, 'Департамент').count(department),
                min(wages_by_department),
                max(wages_by_department),
                # округляем з/п, потому что важны только целые числа...
                round(sum(wages_by_department) / len(wages_by_department))
            ]
        )
    return summary


def save_summary_as_csv(data: list, filename: str) -> None:
    """
    сохраняет сводный отчет как csv файл

    Args:
        data (list): исходная таблица
        filename (str): название файла, под которым сохранится отчет
    """
    with codecs.open(filename, 'w', 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(get_departments_summary(data))


def menu() -> None:
    """
    выводит на экран меню дальнейших действий,
    начиная с выбора файла для считывания (исходный или нет),
    потом по выбору пользователя может выводить иерархию, сводный отчет и
    сохранять отчет в виде csv файла с произвольным названием
    Также по желанию пользователя, программу можно завершить на любом из шагов
    """
    while True:

        print('\nМеню:')
        print('1. Использовать исходный файл "Corp_Summary.csv".')
        print(('2. Скачать другой csv файл с'
               ' такой же структурой отчета по ссылке.'))
        print('3. Завершить программу.')

        inp = input('Введите номер пункта меню: ')

        if inp == '1':
            data = load_csv()
            print('\nФайл успешно скачан и обработан.')
            break
        elif inp == '2':
            print('\nВведите ссылку на скачивание csv файла.')
            response = input('URL: ')
            try:
                data = load_csv(response)
            except ValueError:
                print(('\nВы ввели неправильную ссылку. Попробуйте еще раз '
                      'либо выберите исходный файл.'))
                continue
            else:
                print('\nФайл успешно скачан и обработан.')
                break
        elif inp == '3':
            return None
        else:
            print('\nВы ввели некорректное число. Попробуйте еще раз.')

    while True:

        print('\nМеню:')
        print('1. Вывести иерархию команд.')
        print('2. Вывести сводный отчёт по департаментам.')
        print('3. Сохранить сводный отчёт в виде csv-файла.')
        print('4. Завершить программу.')

        inp = input('Введите номер пункта меню: ')
        print('\n')

        if inp == '1':
            print_table(get_hierarchy(data))
        elif inp == '2':
            print_table(get_departments_summary(data))
        elif inp == '3':
            # захотел кастомное название закинуть для файла на выход
            output_name = input(
                ('Введите название файла для сохранения'
                 ' сводного отчёта (в формате my_name.csv): '))
            save_summary_as_csv(data, output_name)
            # вывожу указатель на название файла
            print(f'Сводный отчёт сохранён в файл {output_name}')
        elif inp == '4':
            break
        else:
            print('Вы ввели некорректное число. Попробуйте еще раз.')


if __name__ == '__main__':
    menu()

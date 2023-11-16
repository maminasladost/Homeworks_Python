import math


class CountVectorizer:
    """
    Упрощенная версия класса CountVectorizer из sklearn,
    которая имеет всего 4 метода: fit, transform, fit_transform,
    get_feature_names
    """

    def __init__(self, lowercase: bool = True, stop_words: list = None,
                 sort: str = 'original') -> None:
        """
        Инициализация класса

        Args:
            lowercase (bool, optional): Нужно ли преобразовывать
            тексты в нижний регистр. Defaults to True.

            stop_words (list, optional): Список стоп слов или 'english' для
            стоп слов английского языка. Defaults to None.

            sort (str, optional): Порядок добавления слов в
            document-term matrix.
            'original' для добавления в том порядке, в котором слова
            встречаются в корпусе.
            'alphabetical' для добавления в алфавитном порядке. Defaults
            to 'original'

        Raises:
            ValueError: Неправильный тип данных для lowercase
            ValueError: Неправильный тип данных для stop_words
            ValueError: Неправильный тип данных для sort
        """
        # Проверка на тип lowercase
        if type(lowercase) is not bool:
            raise ValueError('Параметр lowercase должен быть True или False')

        self.lowercase = lowercase

        # Смотрим на то, что передали в stop_words
        if stop_words is not None:
            # Если выбрано 'english', то используется файлик со стоп словами
            # из английского языка
            if stop_words == 'english':
                self.stop_words = []
                with open('stopwords.txt', 'r') as file:
                    for line in file:
                        word = line.strip()
                        self.stop_words.append(word)

            # Если передан список, то смотрим что б элементами списка были
            # строки
            elif type(stop_words) is list \
                    and all(isinstance(word, str) for word in stop_words):
                self.stop_words = stop_words
            # иначе ошибка
            else:
                raise ValueError('Неправильный формат stop_words')
        # если ничего не передано, или передан None, то стоп слов не будет
        else:
            self.stop_words = None

        self.vocabulary = {}  # словарик, где ключ - слово, значение -
        # индекс в document-term matrix

        self.feature_names = []  # просто список со всеми словами

        if sort in ['original', 'alphabetical']:
            self.sort = sort  # выбираем порядок добавления слов
        else:
            raise ValueError('sort должен быть либо "original",\
                             либо "alphabetical"')

    def _remove_non_alnum(self, word: str) -> str:
        """
        Удаляет из слова все символы, которые не буквы и не числа.
        Начинается с '_' потому что функция для внутреннего пользования

        Args:
            word (str): Слово

        Returns:
            str: Слово только с числами или буквами
        """
        # для каждого слова убираем символы, которые не alnum
        new_word = ''.join(symbol for symbol in word if symbol.isalnum())

        return new_word

    def _tokenize(self, text: str) -> list:
        """
        Разделяет текст на токены
        (по сути слова без разного рода шума в виде пунктуации и тд.)
        Начинается с '_', потому что эта функция только для использования
        внутри

        Args:
            text (str): Текст

        Returns:
            list: Список токенов
        """

        # смотрим на то, нужно ли переводить в нижний регистр
        if self.lowercase:
            text = text.lower()

        # делим слова по пробелам
        words = text.split()
        # в зависимости от наличия списка стоп слов убираем non alphanumeric
        # условие any(...) нужно для того, что бы отсеять случаи, когда есть
        # слово, состоящее только из non alphanumeric символов
        if self.stop_words:
            words = [self._remove_non_alnum(word) for word in words if word
                     not in self.stop_words and any(c.isalnum() for c in word)]
        else:
            words = [self._remove_non_alnum(word) for word in words if
                     any(c.isalnum() for c in word)]

        return words

    def fit(self, corpus: list) -> None:
        """
        Создает список всех слов из корпуса, а так же
        считает их количество

        Args:
            corpus (list): Список текстов
        """
        # для каждого текста будем токенизировать слова
        for text in corpus:
            words = self._tokenize(text)
            # для каждого нового слова будем добавлять его в словарик
            # и добавлять в список всех слов
            for word in words:
                if word not in self.vocabulary:
                    self.vocabulary[word] = len(self.vocabulary)
                    self.feature_names.append(word)

        # учитываем сортировку
        if self.sort == 'alphabetical':
            self.feature_names = sorted(self.feature_names)

        # указываем флажок для фит
        self.fitted = True

    def transform(self, corpus: list) -> list:
        """
        Преобразования корпуса текстов в document-term matrix

        Args:
            corpus (list): Список текстов

        Returns:
            list: Document-term matrix
        """
        # трансформ можно применить только после фит
        if not self.fitted:
            raise RuntimeError('Метод transform можно вызывать только после \
                               вызова метода fit.')

        matrix = []  # document-term matrix

        # для каждого текста в корпусе будем токенизировать его и
        # добавлять счетчик
        for text in corpus:
            words = self._tokenize(text)
            text_count = [words.count(word) for word in self.feature_names]
            matrix.append(text_count)

        return matrix

    def fit_transform(self, corpus: list) -> list:
        """
        Одновременный fit и transform

        Args:
            corpus (list): Список текстов

        Returns:
            list: Document-term matrix
        """

        self.fit(corpus)

        return self.transform(corpus)

    def get_feature_names(self) -> list:
        """
        Получение всех слов в текстах корпуса текстов

        Returns:
            list: Список всех слов корпуса текстов
        """

        return self.feature_names


class TfidfTransformer:
    """
    Позволяет считать tf и idf матрицы по count_matrix

    """

    def __init__(self, feature_names: list) -> None:
        """
        Инициализация

        Args:
            feature_names (list): Все уникальные слова из корпуса
        """

        self.feature_names = feature_names

    def tf_transform(self, count_matrix: list) -> list:
        """
        Выводит tf матрицу по count_matrix

        Args:
            count_matrix (list): Матрица-счетчик слов

        Returns:
            list: _description_
        """

        tf_matrix = []

        for t_count in count_matrix:
            total_words = sum(t_count)
            text_tf = [round(count / total_words, 3) for count in t_count]
            tf_matrix.append(text_tf)

        return tf_matrix

    def idf_transform(self, count_matrix: list) -> list:
        """
        Выводит idf матрицу по count_matrix

        Args:
            count_matrix (list): матрица-счетчик слов

        Returns:
            list: idf matrix
        """

        idf_matrix = []

        for indx in range(len(self.feature_names)):

            document_count = sum(
                1 for text_count in count_matrix if
                text_count[indx] > 0)

            idf = round(math.log((len(count_matrix) + 1) /
                                 (1 + document_count)) + 1, 3)
            idf_matrix.append(idf)

        return idf_matrix

    def fit_transform(self, count_matrix: list) -> list:

        tf = self.tf_transform(count_matrix)
        idf = self.idf_transform(count_matrix)

        tfidf_matrix = [[round(t * i, 3) for t, i in zip(tf_row, idf)] for
                        tf_row in tf]

        return tfidf_matrix


class TfidfVectorizer(CountVectorizer):
    """
    Совмещает 2 класса: CountVectorizer и TfidfTransformer

    Args:
        CountVectorizer (_type_): Класс позволяющий считать count_matrix
    """

    def __init__(self):
        """
        Инициализация с наследованием от CountVectorizer,
        а также используем экземпляр TfidfTransformer
        """
        super().__init__()
        self.tf_idf_transformer = TfidfTransformer(
            feature_names=self.feature_names)

    def fit_transform(self, corpus: list) -> list:
        """
        Совмещает fit и transform

        Args:
            corpus (list): Список текстов

        Returns:
            list: tf-ifd matrix
        """

        count_matrix = super().fit_transform(corpus)

        return self.tf_idf_transformer.fit_transform(count_matrix)


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(tfidf_matrix)

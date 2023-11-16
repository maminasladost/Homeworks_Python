import click
import time
import random
from functools import wraps
from typing import List


class Pizza:
    """Класс для пицц.

    Attributes:
        size (str): Размер пиццы
        ingredients (List[str]): Ингридиенты в пицце
    """

    def __init__(self, size: str):
        """Инициализируем пиццу

        Args:
            size (str): Размер пиццы
        """

        self.ingredients: List[str] = []
        self.size: str = size

    def dict(self) -> dict:
        """Будет возвращать словарь с рецептом пиццы"""
        return {'ingredients': self.ingredients, 'size': self.size}

    def __eq__(self, other: 'Pizza') -> bool:
        """Функция сравнения двух пицц

        Args:
            other (Pizza): объект класса Pizza, с которым буду сравнивать

        Returns:
            bool: Одинаковые ли пиццы или нет
        """
        return (self.ingredients == other.ingredients
                and self.size == other.size)

    def get_name(self) -> str:
        """Возвращает название пиццы

        Returns:
            str: Название пиццы
        """
        return 'Pizza'


class Margherita(Pizza):
    """Класс для маргариты.

    Attributes:
        size (str): Размер пиццы.
        ingredients (List[str]): Список ингредиентов маргариты
    """

    def __init__(self, size: str):
        """Инициализация маргариты

        Args:
            size (str): Размер пиццы
        """

        super().__init__(size)

        self.ingredients.extend(
            ['🍅 🥫 tomato sauce', '🧀 mozzarella', '🍅 tomatoes'])

    def get_name(self) -> str:
        """Возвращает название маргариты

        Returns:
            str: название
        """
        return 'Margherita'


class Pepperoni(Pizza):
    """Класс для пепперони

    Attributes:
        size (str): Размер пиццы
        ingredients (List[str]): Список ингредиентов пепперони
    """

    def __init__(self, size: str):
        """Инициализация пепперони

        Args:
            size (str): Размер пиццы
        """
        super().__init__(size)
        self.ingredients.extend(
            ['🍅 🥫 tomato sauce', '🧀 mozzarella', '🌶️ 😋 pepperoni'])

    def get_name(self) -> str:
        """Возвращает название пепперони

        Returns:
            str: название
        """
        return 'Pepperoni'


class Hawaiian(Pizza):
    """Класс для гавайской

    Attributes:
        size (str): Размер пиццы
        ingredients (List[str]): Список ингредиентов гавайской
    """

    def __init__(self, size: str):
        """Инициализация гавайской

        Args:
            size (str): Размер пиццы
        """
        super().__init__(size)
        self.ingredients.extend(
            ['🍅 🥫 tomato sauce', '🧀 mozzarella', '🍗 chicken', '🍍 pineapples'])

    def get_name(self) -> str:
        """Возвращает название пепперони

        Returns:
            str: название
        """
        return 'Hawaiian'


def print_delivery_status(obj: Pizza, action: str, duration: int) -> None:
    """Выводит на экран статус доставки пиццы

    Args:
        obj (Pizza): объект класса Pizza
        action (str): совершенное действие (Приготовили, Доставили, Забрали)
        duration (int): время выполнения действия в секундах
    """
    print(f'{action} {obj.get_name()} за {duration}s!')


@click.group()
def cli() -> None:
    """команды для управления заказом пицц"""
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True,
              help='Выбрать доставку')
@click.option('--pickup', default=False, is_flag=True,
              help='Выбрать самовывоз')
@click.argument('pizza', nargs=1)
@click.argument('size', type=click.Choice(['X', 'XL']))
def order(pizza: str, size: str, delivery: bool, pickup: bool) -> None:
    """Готовит и доставляет пиццу / готовит и ожидает самововоз пиццы
    / готовит пиццу

    Args:
        pizza (str): название пиццы
        size (str): размер пиццы
        delivery (bool): флаг для доставки
        pickup (bool): флаг для самовывоза
    """
    obj = None
    if pizza.lower() == 'margherita':
        obj = Margherita(size)
    elif pizza.lower() == 'pepperoni':
        obj = Pepperoni(size)
    elif pizza.lower() == 'hawaiian':
        obj = Hawaiian(size)

    cook_time = random.randint(1, 3)
    wait_time = random.randint(1, 3)
    delivery_time = random.randint(1, 3)

    if delivery and pickup:
        print('Вы не можете выбрать доставку и самовывоз для одного заказа!')
    elif delivery:
        time.sleep(cook_time)
        print_delivery_status(obj, 'Приготовили', cook_time)
        time.sleep(delivery_time)
        print_delivery_status(obj, 'Доставили', delivery_time)
    elif pickup:
        time.sleep(cook_time)
        print_delivery_status(obj, 'Приготовили', cook_time)
        time.sleep(wait_time)
        print_delivery_status(obj, 'Забрали', wait_time)
    else:
        time.sleep(cook_time)
        print_delivery_status(obj, 'Приготовили', cook_time)


@cli.command()
def menu() -> None:
    """Выводит меню"""
    margherita = Margherita(size='X')
    pepperoni = Pepperoni(size='X')
    hawaiian = Hawaiian(size='X')

    print('🧀 Margherita :', ', '.join(margherita.ingredients))
    print('🥵 Pepperoni  :', ', '.join(pepperoni.ingredients))
    print('🏝️ Hawaiian   :', ', '.join(hawaiian.ingredients))


def log(template: str) -> wraps:
    """декоратор для логирования времени выполнения функций с пиццами

    Args:
        template (str): шаблон вывода

    Returns:
        wraps: функция, обернутая в декоратор
    """
    def decorator(func: callable) -> wraps:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = round(end_time - start_time)
            print(template.format(duration))
            return result
        return wrapper
    return decorator


@log('👨‍🍳 Приготовили за {}с!')
def bake(pizza: Pizza) -> None:
    """Готовит пиццу

    Args:
        pizza (Pizza): объект класса Pizza
    """
    time.sleep(random.randint(1, 3))


@log('🛵 Доставили за {}с!')
def delivery(pizza: Pizza) -> None:
    """Доставляет пиццу

    Args:
        pizza (Pizza): объект класса Pizza
    """
    time.sleep(random.randint(1, 3))


@log('🏎️ Забрали за {}с!')
def pickup(pizza: Pizza) -> None:
    """Самовывоз пиццы

    Args:
        pizza (Pizza): объект класса Pizza
    """
    time.sleep(random.randint(1, 3))


if __name__ == '__main__':  # pragma: no cover
    cli()

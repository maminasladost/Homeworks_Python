import pytest
from click.testing import CliRunner
from pizza import (cli, bake, delivery, pickup, print_delivery_status,
                   Pizza, Pepperoni, Hawaiian)


def test_pizza_dict():
    size = 'XL'
    pizza = Pizza(size=size)

    pizza.ingredients.extend(['cheese', 'tomatoes', 'pepperoni'])

    assert pizza.dict() == {'ingredients': [
        'cheese', 'tomatoes', 'pepperoni'], 'size': 'XL'}


def test_pizza_eq():
    size = 'XL'

    pizza1 = Pizza(size=size)
    pizza1.ingredients.extend(['cheese', 'tomatoes', 'pepperoni'])

    pizza2 = Pizza(size=size)
    pizza2.ingredients.extend(['cheese', 'tomatoes', 'pepperoni'])

    pizza3 = Pizza(size='L')
    pizza3.ingredients.extend(['cheese', 'tomatoes', 'pepperoni'])

    assert pizza1 == pizza2

    assert pizza1 != pizza3


def test_print_delivery_status(capfd):
    pizza = Pizza(size='X')
    print_delivery_status(pizza, 'Test Action', 2)
    captured = capfd.readouterr()
    assert 'Test Action Pizza за 2s!' in captured.out


def test_pepperoni_get_name():
    pepperoni = Pepperoni(size='XL')
    assert pepperoni.get_name() == 'Pepperoni'


def test_hawaiian_get_name():
    hawaiian = Hawaiian(size='XL')
    assert hawaiian.get_name() == 'Hawaiian'


@pytest.fixture
def runner():
    return CliRunner()


def test_order_delivery(runner):
    result = runner.invoke(cli, ['order', 'margherita', 'X', '--delivery'])
    assert result.exit_code == 0


def test_order_pickup(runner):
    result = runner.invoke(cli, ['order', 'margherita', 'X', '--pickup'])
    assert result.exit_code == 0


def test_order_wrong_pizza(runner):
    result = runner.invoke(cli, ['order', 'invalid_pizza', 'X', '--pickup'])
    assert result.exit_code != 0


def test_order_wrong_flags(runner):
    result = runner.invoke(
        cli, ['order', 'margherita', 'X', '--delivery', '--pickup'])
    assert ('Вы не можете выбрать доставку и самовывоз для одного заказа!'
            in result.output)


def test_order_no_flags(runner):
    result = runner.invoke(cli, ['order', 'margherita', 'X'])
    assert result.exit_code == 0
    assert 'Приготовили' in result.output
    assert 'margherita' in result.output


def test_order_pepperoni_delivery(runner):
    result = runner.invoke(cli, ['order', 'pepperoni', 'XL', '--delivery'])
    assert result.exit_code == 0
    assert 'Доставили' in result.output
    assert 'Pepperoni' in result.output


def test_order_hawaiian_pickup(runner):
    result = runner.invoke(cli, ['order', 'hawaiian', 'XL', '--pickup'])
    assert result.exit_code == 0
    assert 'Забрали' in result.output
    assert 'Hawaiian' in result.output


def test_menu(runner):
    result = runner.invoke(cli, ['menu'])
    assert result.exit_code == 0


def test_bake():
    pizza = Pizza(size='X')
    bake(pizza)


def test_delivery():
    pizza = Pizza(size='X')
    delivery(pizza)


def test_pickup():
    pizza = Pizza(size='X')
    pickup(pizza)

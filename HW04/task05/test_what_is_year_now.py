import json
import pytest
from unittest.mock import patch
from what_is_year_now import what_is_year_now


@pytest.fixture
def mock_urlopen():
    with patch('urllib.request.urlopen') as mock_urlopen:
        yield mock_urlopen


def test_format_minus(mock_urlopen):
    response_data = {
        'currentDateTime': '2023-10-31'
    }
    mock_urlopen.return_value.__enter__.return_value.read.return_value = \
        json.dumps(
            response_data)

    year = what_is_year_now()
    assert year == 2023


def test_format_dot(mock_urlopen):
    response_data = {
        'currentDateTime': '31.10.2023'
    }
    mock_urlopen.return_value.__enter__.return_value.read.return_value = \
        json.dumps(
            response_data)

    year = what_is_year_now()
    assert year == 2023


def test_format_star(mock_urlopen):
    response_data = {
        'currentDateTime': '2023/10/31'
    }
    mock_urlopen.return_value.__enter__.return_value.read.return_value = \
        json.dumps(
            response_data)

    with pytest.raises(ValueError):
        what_is_year_now()


def test_format_slash(mock_urlopen):
    response_data = {
        'currentDateTime': '2023/10/31'
    }
    mock_urlopen.return_value.__enter__.return_value.read.return_value = \
        json.dumps(
            response_data)

    with pytest.raises(ValueError):
        what_is_year_now()


def test_format_wrong_order(mock_urlopen):
    response_data = {
        'currentDateTime': '10-31-2023'
    }
    mock_urlopen.return_value.__enter__.return_value.read.return_value = \
        json.dumps(
            response_data)

    with pytest.raises(ValueError):
        what_is_year_now()

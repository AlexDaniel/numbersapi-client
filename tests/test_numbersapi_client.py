from numbersapi_client import get_number_fact, get_date_fact
from numbersapi_client import NumbersAPIException, NumbersAPIBugException
import pytest


def test_simple():
    result = get_number_fact(42)
    assert result['found']
    assert result['number'] == 42
    assert result['type'] == 'trivia'
    assert result['text'].startswith('42 ')


def test_trivia():
    result = get_number_fact(41)
    assert result['found']
    assert result['number'] == 41
    assert result['type'] == 'trivia'
    assert result['text'].startswith('41 ')


def test_math():
    result = get_number_fact(43, 'math')
    assert result['found']
    assert result['number'] == 43
    assert result['type'] == 'math'
    assert result['text'].startswith('43 ')


def test_year():
    result = get_number_fact(1900, type='year')
    assert result['found']
    assert result['number'] == 1900
    assert result['type'] == 'year'
    assert result['text'].startswith('1900 ')


def test_date():  # highly discouraged but still supported
    result = get_number_fact('10/20', type='date')
    assert result['found']
    assert result['number'] == 294
    assert result['type'] == 'date'
    assert result['text'].startswith('October 20th')


def test_date_date():
    import datetime
    result = get_date_fact(datetime.date(2020, 2, 11))
    assert result['found']
    assert result['number'] == 42
    assert result['type'] == 'date'
    assert result['text'].startswith('February 11th')


def test_date_datetime():
    import datetime
    result = get_date_fact(datetime.datetime(2020, 5, 2))
    assert result['found']
    assert result['number'] == 123
    assert result['type'] == 'date'
    assert result['text'].startswith('May 2nd')


def test_date_str():
    result = get_date_fact('12/25')
    assert result['found']
    assert result['number'] == 360
    assert result['type'] == 'date'
    assert result['text'].startswith('December 25th')


def test_random():
    result = get_number_fact('random')
    assert result['found']
    assert 'number' in result
    assert result['type'] == 'trivia'
    assert 'text'   in result


def test_wrong_number():
    with pytest.raises(NumbersAPIException):
        get_number_fact('foo')


def test_numbersapi_bug():
    with pytest.raises(NumbersAPIBugException):
        get_number_fact('10000000/1', type='date')


def test_fragment():
    result = get_number_fact(23, fragment=True)
    assert result['found']
    assert result['number'] == 23
    assert result['type'] == 'trivia'
    assert not result['text'].startswith('23 ')


def test_fragment_false():
    result = get_number_fact(23, fragment=False)
    assert result['found']
    assert result['number'] == 23
    assert result['type'] == 'trivia'
    assert result['text'].startswith('23 ')


def test_notfound_default():
    result = get_number_fact(314159265358979, notfound='default')
    assert not result['found']
    assert result['number'] == 314159265358979
    assert result['type'] == 'trivia'
    assert 'text' in result


def test_notfound_floor():
    result = get_number_fact(35353, notfound='floor')
    assert not result['found']
    assert result['number'] < 35353
    assert result['type'] == 'trivia'
    assert 'text' in result


def test_notfound_ceil():
    result = get_number_fact(-12344, notfound='ceil', type='year')
    assert not result['found']
    assert result['number'] > -12344
    assert result['type'] == 'year'
    assert 'text' in result


def test_default():
    result = get_number_fact(1234567890987654321, default='foo bar')
    assert not result['found']
    assert result['type'] == 'trivia'
    assert result['text'] == 'foo bar'


def test_minmax():
    result = get_number_fact('random', min=5, max=5)
    assert result['found']
    assert result['number'] == 5
    assert result['type'] == 'trivia'
    assert result['text'].startswith('5 ')


def test_minmax_reversed():
    with pytest.raises(NumbersAPIBugException):
        get_number_fact('random', min=10, max=5)

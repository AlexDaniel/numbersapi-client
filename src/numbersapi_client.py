"""API client for NumbersAPI."""

import json
from datetime import date, datetime
from typing import Optional, Union
from enum import Enum
import requests


class FactType(Enum):
    TRIVIA = 'trivia'
    MATH   = 'math'
    DATE   = 'date'
    YEAR   = 'year'


class NotFound(Enum):
    DEFAULT = 'default'
    FLOOR   = 'floor'
    CEIL    = 'ceil'


class NumbersAPIException(Exception):
    """The supplied arguments are not supported by NumbersAPI."""


class NumbersAPIBugException(Exception):
    """The API returned a clearly erroneous result."""


def _numify(data, response):
    # Extra logic to handle edge-cases in the API itself that result in
    # different types being returned. Hopefully the returned number will be
    # either an `int` or a `float`.
    if 'number' not in data:
        raise NumbersAPIBugException()

    if type(data['number']) in (int, float):
        return data

    if data['number'] is None:  # maybe it is +Inf or -Inf?
        import math
        if response.headers['X-Numbers-API-Number'] == 'Infinity':
            data['number'] = +math.inf
        if response.headers['X-Numbers-API-Number'] == '-Infinity':
            data['number'] = -math.inf
        raise NumbersAPIBugException()

    try:  # ok… maybe it's a stringified int?
        data['number'] = int(data['number'])
        return data
    except ValueError:
        pass

    try:  # or a stringified float?
        data['number'] = float(data['number'])
        return data
    except ValueError:
        pass

    raise NumbersAPIBugException()  # out of ideas at this point


def get_number_fact(
        number:    Union[int, str] = 'random',
        type:      FactType = FactType.TRIVIA.value,
        fragment:  Optional[bool] = None,
        notfound:  NotFound = NotFound.DEFAULT.value,
        default:   Optional[str]  = None,
        min:       Optional[int]  = None,
        max:       Optional[int]  = None,
        raw:       bool = False,
) -> Union[dict, str]:
    """
    Get JSON results from NumbersAPI.

    :param number: An int, or the string 'random' or a day of year
                   in the form 'month/day'.
    :param type: Is one of 'trivia', 'math', 'date', or 'year'.
    :param fragment: True to get the fact as a sentence fragment that can be
                     easily included as part of a larger sentence.
    :param notfound: What to do if the number is not found. One of 'default',
                     'floor' or 'ceil'.
    :param default: What to return if the number is not found.
    :param min: Inclusive min boundary for 'random' numbers.
    :param max: Inclusive max boundary for 'random' numbers.
    :param raw: True to return the raw response as a str, False to parse json
                and return it as a dict.
    :return: Response from the NumbersAPI.
    """
    params = {
        'fragment': (True if fragment else None),
        'notfound': notfound,
        'default':  default,
        'min':      min,
        'max':      max,
    }
    response = requests.get(f'http://numbersapi.com/{number}/{type}',
                            headers={'Content-Type': 'application/json'},
                            params=params)

    if 'X-Numbers-API-Number' not in response.headers:
        raise NumbersAPIException()
    if response.headers['X-Numbers-API-Number'] == 'NaN':
        raise NumbersAPIBugException()

    if raw:
        return response.text

    return _numify(json.loads(response.text), response)


def dateify(maybe_date: str):
    if maybe_date == 'random':
        return maybe_date
    if 'strftime' not in dir(maybe_date):
        maybe_date = datetime.strptime(maybe_date, '%m/%d')
    return maybe_date.strftime('%m/%d')


def get_date_fact(
        date: Union[datetime, date, str] = 'random',
        **kwargs,
):
    """
    Get JSON results about dates from NumbersAPI.

    :param date: ``date``, ``datetime`` or a `str` in “month/day” format.
    :param args: Arguments to pass to ``get_number_fact``.
    :param kwargs:  Arguments to pass to ``get_number_fact``.
    :return: Response from the NumbersAPI.
    """

    return get_number_fact(dateify(date), FactType.DATE.value, **kwargs)

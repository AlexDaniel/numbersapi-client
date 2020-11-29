import subprocess
import json


def run(args: list, exitcode: int = 0, empty_stderr: bool = True):
    result = subprocess.run(
        ['numbersapi-cli'] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert (not result.stderr) == empty_stderr
    assert result.returncode == exitcode

    return {
        'json': json.loads(result.stdout),
        'stderr': result.stderr,
    }


def test_simple():
    output = run(['42'])
    result = output['json']
    assert result['found']
    assert result['number'] == 42
    assert result['type'] == 'trivia'
    assert result['text'].startswith('42 ')


def test_noargs():
    output = run([])
    result = output['json']
    assert result['found']
    assert result['type'] == 'trivia'


def test_trivia():
    output = run(['--trivia', '41'])
    result = output['json']
    assert result['found']
    assert result['number'] == 41
    assert result['type'] == 'trivia'
    assert result['text'].startswith('41 ')


def test_math():
    output = run(['--math', '43'])
    result = output['json']
    assert result['found']
    assert result['number'] == 43
    assert result['type'] == 'math'
    assert result['text'].startswith('43 ')


def test_year():
    output = run(['--year', '1900'])
    result = output['json']
    assert result['found']
    assert result['number'] == 1900
    assert result['type'] == 'year'
    assert result['text'].startswith('1900 ')


def test_date_noargs():
    output = run(['--date'])
    result = output['json']
    assert result['found']
    assert result['type'] == 'date'


def test_date_str():
    output = run(['--date', '12/25'])
    result = output['json']
    assert result['found']
    assert result['number'] == 360
    assert result['type'] == 'date'
    assert result['text'].startswith('December 25th')


def test_date_random():
    output = run(['--date', 'random'])
    result = output['json']
    assert result['found']
    assert result['type'] == 'date'


def test_random():
    output = run(['random'])
    result = output['json']
    assert result['found']
    assert 'number' in result
    assert result['type'] == 'trivia'
    assert 'text'   in result


# def test_wrong_number():
#     with pytest.raises(NumbersAPIException):
#         get_number_fact('foo')


# def test_numbersapi_bug():
#     with pytest.raises(NumbersAPIBugException):
#         get_number_fact('10000000/1', type='date')


def test_fragment():
    output = run(['--fragment', '23'])
    result = output['json']
    assert result['found']
    assert result['number'] == 23
    assert result['type'] == 'trivia'
    assert not result['text'].startswith('23 ')


def test_notfound_default():
    output = run(['--notfound=default', '314159265358979'])
    result = output['json']
    assert not result['found']
    assert result['number'] == 314159265358979
    assert result['type'] == 'trivia'
    assert 'text' in result


def test_notfound_floor():
    output = run(['--notfound=floor', '35353'])
    result = output['json']
    assert not result['found']
    assert int(result['number']) < 35353  # int() because cli is garbage in, garbage out
    assert result['type'] == 'trivia'
    assert 'text' in result


def test_notfound_ceil():
    output = run(['--year', '--notfound=ceil', '-12344'])
    result = output['json']
    assert not result['found']
    assert int(result['number']) > -12344  # int() because cli is garbage in, garbage out
    assert result['type'] == 'year'
    assert 'text' in result


def test_default():
    output = run(['--default=foo bar', '1234567890987654321'], empty_stderr=False)
    assert b'Warning:' in output['stderr']
    assert b'likely to return incorrect answers' in output['stderr']
    result = output['json']
    assert not result['found']
    assert result['type'] == 'trivia'
    assert result['text'] == 'foo bar'


def test_minmax():
    output = run(['--min=5', '--max=5', 'random'])
    result = output['json']
    assert result['found']
    assert result['number'] == 5
    assert result['type'] == 'trivia'
    assert result['text'].startswith('5 ')


def test_warning_useless_default():
    output = run(['--default=foo', '--notfound=ceil', '5555555555'], empty_stderr=False)
    result = output['json']
    assert b'Warning:' in output['stderr']
    assert b'--default value will likely be ignored' in output['stderr']
    assert result['type'] == 'trivia'


def test_warning_useless_min():
    output = run(['--min=5', '55'], empty_stderr=False)
    result = output['json']
    assert b'Warning:' in output['stderr']
    assert b'using --min or --max for non-random numbers' in output['stderr']
    assert result['found']
    assert result['number'] == 55
    assert result['type'] == 'trivia'
    assert result['text'].startswith('55 ')


def test_warning_useless_max():
    output = run(['--max=5', '66'], empty_stderr=False)
    result = output['json']
    assert b'Warning:' in output['stderr']
    assert b'using --min or --max for non-random numbers' in output['stderr']
    assert result['found']
    assert result['number'] == 66
    assert result['type'] == 'trivia'
    assert result['text'].startswith('66 ')

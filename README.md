## NumbersAPI Python Client

A simple Python library for interfacing with [NumbersAPI](numbersapi.com/).

### Installation

Poetry is used for packaging:

```sh
poetry install
poetry build
```

If successful, it should produce a wheel in the `dist` folder.

You should also be able to use the provided command line tool:

```sh
poetry run numbersapi-cli
```

```json
{
 "text": "130 is the approximate maximum height in meters of trees.",
 "number": 130,
 "found": true,
 "type": "trivia"
}
```

A minimal example of using the library:

```sh
poetry run python3
```
```python
>>> from numbersapi_client import get_number_fact
>>> get_number_fact()
{'text': '666 is the number of the devil.', 'number': 666, 'found': True, 'type': 'trivia'}
```


### Tests

You can run the tests by using the following command:

```sh
poetry run pytest
```

The tests are non-exhaustive and the library is tested against the live service.

### Docker

The provided `Dockerfile` includes both the `numbersapi_client` module that you
can include as a library in Python scripts as well as `numbersapi-cli`
command-line tool. The Dockerfile is provided so that you can play with the
library without bothering with the installation procedure. For example:

```sh
docker build --tag numbers_api:1.0 .
docker run --rm -ti numbers_api:1.0 /bin/sh

/ $ numbersapi-cli 42

```


```

{
 "text": "42 is the answer to the Ultimate Question of Life, the Universe, and Everything.",
 "number": 42,
 "found": true,
 "type": "trivia"
}
```


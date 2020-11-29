FROM python:3.9-alpine as base


FROM base as builder

# required for poetry:
RUN apk add build-base libffi-dev libressl-dev

RUN mkdir /install
WORKDIR /install

RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml README.md /install/
RUN poetry install --no-dev --no-root

COPY /src /install/src
RUN poetry install --no-dev


FROM base

# The library is installed into /usr/local/lib/python3.X/site-packages
# but with a .pth file pointing to /install
COPY --from=builder /usr/local/ /usr/local/
COPY --from=builder /install    /install

# TODO make sure poetry itself is not in the container

USER 9000

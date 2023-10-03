FROM python:3.11.5-alpine3.18 as builder

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /ibn-battuta

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


FROM python:3.11.5-alpine3.18 as runtime

ENV VIRTUAL_ENV=/ibn-battuta/.venv \
    PATH="/ibn-battuta/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY main.py ./
COPY app ./app

ENTRYPOINT ["python", "-m", "main"]

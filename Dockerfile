FROM python:3.11.5-alpine3.18

RUN pip install poetry==1.6.1

WORKDIR /ibn-battuta

COPY pyproject.toml poetry.lock ./
COPY ./app ./app
COPY ./main.py ./

RUN touch README.md
RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "start"]

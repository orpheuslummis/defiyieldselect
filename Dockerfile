FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-dev

COPY . /app

EXPOSE 8000

CMD ["python", "-m", "run"]
FROM python:3-slim-buster

WORKDIR /app
COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

CMD [ "python3", "main.py"]

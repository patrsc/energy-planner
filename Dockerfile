FROM python:3.13-slim

RUN apt-get update
RUN apt-get install -y bash git
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

COPY energy_planner energy_planner
COPY run_planner.py .
COPY run_scheduler.py .

ENV STORAGE_DIR=/config/data/energy_planner
ENV TZ=Europe/Vienna

CMD ["poetry", "run", "python", "run_scheduler.py"]

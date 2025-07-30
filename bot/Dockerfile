FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONFAULTHANDLER=1

WORKDIR /src

RUN apt-get update \
  && apt-get install -y curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src
RUN pip install -r requirements.txt

RUN groupadd -r app && useradd --no-log-init -r -g app app && chown -R app /src

COPY --chown=app:app . /src/

USER app

CMD ["python", "main.py"]
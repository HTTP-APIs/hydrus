FROM python:3.7.6-alpine3.11 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.5 \
    PATH=/root/.local/bin:$PATH

RUN apk add --no-cache gcc libffi-dev musl-dev \
        py3-virtualenv git postgresql-dev \
        libxml2 libxml2-dev libxslt-dev

COPY . ./app
WORKDIR /app

RUN pip install --user "poetry==$POETRY_VERSION"
RUN pwd
RUN virtualenv -p $(which python) .venv

RUN pwd

RUN poetry build && .venv/bin/pip install dist/*.whl

FROM base as final

RUN apk add --no-cache libffi libpq
COPY --from=builder /app/.venv /.venv
COPY docker-entrypoint.sh ./
CMD ["./docker-entrypoint.sh"]
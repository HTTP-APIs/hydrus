FROM python:3.7.6-alpine3.11 as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

#
# building stage
#
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
# Poetry requires a virtualenv
RUN pip install --user "poetry==$POETRY_VERSION"
RUN virtualenv -p $(which python) .venv
# Build wheels with Poetry
RUN poetry build && .venv/bin/pip install dist/*.whl

#
# running stage
#
FROM base as final
RUN apk add --no-cache libffi libpq
# copy virtualenv and application
COPY --from=builder /app/.venv /.venv
COPY . ./app
WORKDIR /app
CMD ["/.venv/bin/gunicorn --bind 0.0.0.0:8080 --forwarded-allow-ips='*' hydrus:app"]

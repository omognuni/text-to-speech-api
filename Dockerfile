FROM python:3.9-slim
LABEL maintainer='Omognuni'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
    --disabled-password \
    --no-create-home \
    fastapi-user
# mkdir -p /vol/web/media && \
# mkdir -p /vol/web/static && \
# chown -R fastapi-user:fastapi-user /vol && \
# chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER fastapi-user
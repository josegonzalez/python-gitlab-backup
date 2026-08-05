FROM python:3.14-alpine3.24 AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=bind,source=release-requirements.txt,target=release-requirements.txt \
    uv venv \
    && uv pip install -r release-requirements.txt

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install .


FROM python:3.14-alpine3.24
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    ca-certificates \
    git \
    git-lfs \
    && addgroup -g 1000 appuser \
    && adduser -D -u 1000 -G appuser appuser \
    && git lfs install

COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

WORKDIR /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["gitlab-backup"]

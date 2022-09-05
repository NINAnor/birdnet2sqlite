FROM python:3.10 AS base
WORKDIR /src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install sqlite-utils

ADD birdnet2sqlite .
COPY --chmod=755 birdnet2sqlite.sh ./
FROM python:3.10 AS base
WORKDIR /src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install sqlite-utils==3.26.1

ADD birdnet2sqlite .
COPY --chmod=755 birdnet2sqlite.sh ./
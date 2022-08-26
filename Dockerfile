FROM python:3.10 AS base
WORKDIR /src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install sqlite-utils

COPY --chmod=755 birdnet2sqlite.py ./
COPY --chmod=755 utils.py ./
COPY --chmod=755 preprocess_birdnet_result.py ./

ENTRYPOINT ["/src/birdnet2sqlite.py"]

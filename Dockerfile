FROM python:3.10 AS base
WORKDIR /src

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install pdm
COPY pyproject.toml pdm.lock ./
RUN --mount=type=cache,target=/root/.cache/pdm \
    pdm install --no-self
COPY --chmod=755 birdnet2sqlite.py ./

# pdm --pep582
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages/pdm/pep582

ENTRYPOINT ["/src/birdnet2sqlite.py"]

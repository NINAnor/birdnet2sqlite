Converts a bunch of TSV files produced by BirdNet to a SQLite database.
It expects to find a YYYYmmdd_HHMMSS string in the filename.

# How to build and run locally (with Docker)

```
DOCKER_BUILDKIT=1 docker build -t localhost/birdnet2sqlite .
docker run -v $PWD:/data --workdir /data localhost/birdnet2sqlite --help
```

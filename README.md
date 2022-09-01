Converts a bunch of TSV files produced by BirdNet to a SQLite database.
It expects to find a YYYYmmdd_HHMMSS string in the filename.

# How to build and run locally (with Docker)

```
DOCKER_BUILDKIT=1 docker build -t localhost/birdnet2sqlite .
docker run -v $PWD:/data --workdir /data localhost/birdnet2sqlite --help
```

For more flexibility with the script 

```
#!/bin/bash

BASE_FOLDER=$1
OUT_FOLDER=$2

docker run --rm \
    -v $BASE_FOLDER:$BASE_FOLDER \
    -v $OUT_FOLDER:$OUT_FOLDER \
    --workdir $BASE_FOLDER \
    --entrypoint "" \
    birdnet2sqlite \
    bash -c "find $BASE_FOLDER -type f -name '*.txt' | xargs \
    /src/birdnet2sqlite.py --database_path $OUT_FOLDER/my_database.sqlite"
```

# Use the database in R

```
library(RSQLite)
library(DBI)

setwd("path/to/working/directory")
sqlite <- dbDriver("SQLite")
conn <- dbConnect(sqlite, "my_database.sqlite")

# For the full dataset
data <- dbReadTable(conn, "birdnet")

# For a subset of the dataset 
res <- dbSendQuery(con, "SELECT * FROM birdnet WHERE location = X")
```

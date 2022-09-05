#!/bin/bash

set -euo pipefail

BASE_FOLDER=$1
DB_NAME=$2
PREFIX=$3
INDEX_LOCATION_FOLDER=$4

docker run --rm \
    -v $BASE_FOLDER:$BASE_FOLDER \
    --workdir $BASE_FOLDER \
    birdnet2sqlite \
    bash -c "find $BASE_FOLDER -type f -name '*.txt' | xargs \
    /src/birdnet2sqlite.py --database_path $DB_NAME --prefix $PREFIX --index_location_folder $INDEX_LOCATION_FOLDER"
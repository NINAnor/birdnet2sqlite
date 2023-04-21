#!/bin/bash

set -euo pipefail

BASE_FOLDER=$1
DB_NAME=$2
OUT_FOLDER=$(dirname $DB_NAME)
IS_PREFIX=$3
INDEX_LOCATION_FOLDER=$4
SPECIES_LIST_FILE=$5
LANGUAGE=$6



FILES=($(find "$BASE_FOLDER" -type f -name '*.txt'))

# Batch size
BATCH_SIZE=5

# Loop over the files in batches
for (( i=0; i<${#FILES[@]}; i+=BATCH_SIZE )); do
    BATCH_FILES=("${FILES[@]:i:BATCH_SIZE}")

    docker run --rm \
        -v "$BASE_FOLDER":"$BASE_FOLDER" \
        -v "$OUT_FOLDER":"$OUT_FOLDER" \
        --workdir "$BASE_FOLDER" \
        birdnet2sqlite \
        /src/birdnet2sqlite.py \
        --database_path "$DB_NAME" \
        --prefix "$IS_PREFIX" \
        --index_location_folder "$INDEX_LOCATION_FOLDER" \
        --species_list_file "$SPECIES_LIST_FILE" \
        --language "$LANGUAGE" \
        --results "${BATCH_FILES[@]}"
done











#find "$BASE_FOLDER" -type f -name '*.txt' | while read file; do
#    echo "Processing file $file"
#    docker run --rm \
#        -v "$BASE_FOLDER":"$BASE_FOLDER" \
#        -v "$OUT_FOLDER":"$OUT_FOLDER" \
#        --workdir "$BASE_FOLDER" \
#        birdnet2sqlite \
#        /src/birdnet2sqlite.py \
#        --database_path "$DB_NAME" \
#        --prefix "$IS_PREFIX" \
#        --index_location_folder "$INDEX_LOCATION_FOLDER" \
#        --species_list_file "$SPECIES_LIST_FILE" \
#        --language "$LANGUAGE" \
#        --results "$file"
#done


#docker run --rm \
#    -v $BASE_FOLDER:$BASE_FOLDER \
#    -v $OUT_FOLDER:$OUT_FOLDER \
#    --workdir $BASE_FOLDER \
#    birdnet2sqlite \
#    bash -c "find $BASE_FOLDER -type f -name '*.txt' | xargs \
#    /src/birdnet2sqlite.py --database_path $DB_NAME --prefix $IS_PREFIX --index_location_folder $INDEX_LOCATION_FOLDER --species_list_file $SPECIES_LIST_FILE --language $LANGUAGE"
 

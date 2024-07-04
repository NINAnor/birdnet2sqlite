#!/bin/bash

BASE="/path/to/birdnet/result/files"
OUT='./db.sqlite'
IS_PREFIX=False
INDEX_LOCATION=-2

./birdnet2sqlite.sh $BASE $OUT $IS_PREFIX $INDEX_LOCATION

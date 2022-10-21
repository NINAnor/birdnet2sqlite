#!/usr/bin/env python3

import argparse
import ast
import datetime
import re

import sqlite_utils

from utils import parse_tsv, autocast
from preprocess_birdnet_result import add_info

recorder_filename_date = re.compile(r"\d{8}_\d{6}.BirdNET.selection.table.txt")

def filename_to_datetime(filename):
    matches = recorder_filename_date.search(filename)
    if not matches:
        return  # Invalid filename
    try:
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d_%H%M%S.BirdNET.selection.table.txt")
    except ValueError:
        return  # Wrong format
    return dt
        
def main(database_path, recreate, results, prefix, index_location_folder):

    db = sqlite_utils.Database(database_path, recreate=recreate)

    for result in results:
        with open(result) as tsv:
            parsed = autocast(parse_tsv(tsv))
            dt = filename_to_datetime(result)
            #improved = convert_offsets(dt, parsed)
            improved = add_info(result, parsed, prefix, index_location_folder, dt)
            db["birdnet"].insert_all(improved)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert BirdNet results into a SQLite database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--database_path",
        help="Path of the database to create or update",
        default="common.sqlite",
    )
    parser.add_argument(
        "--prefix",
        help="Does the file name has a prefix before HMS_YMD",
        default=False,
    )
    parser.add_argument(
        "--index_location_folder",
        help="Does the file name has a prefix before HMS_YMD",
        default=-1,
        type=int
    )
    parser.add_argument(
        "--recreate",
        help="Recreate the database",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "results",
        nargs="+",
        help="BirdNet result file",
    )
    args = parser.parse_args()
    main(args.database_path, args.recreate, args.results, args.prefix, args.index_location_folder)

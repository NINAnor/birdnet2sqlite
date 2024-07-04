#!/usr/bin/env python3

import argparse
import datetime
import pandas as pd
import re
import logging

import sqlite_utils

from utils import parse_tsv, autocast
from preprocess_birdnet_result import add_info

recorder_filename_date = re.compile(
    r"(?:\d{8}_\d{6}.BirdNET.selection.table.txt)|"
    r"(?:\d{8}-\d{6}.BirdNET.selection.table.txt)|"
    r"(?:\d{14}.BirdNET.selection.table.txt)|"
    r"(?:\d{8}.BirdNET.selection.table.txt)|"
    r"(?:\d{4}-\d{2}-\d{2}_\d{6}.BirdNET.selection.table.txt)|"
    r"(?:\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d{3}Z\.BirdNET\.selection\.table\.txt)"
)


def filename_to_datetime(filename):
    matches = recorder_filename_date.search(filename)

    if not matches:
        return  # Invalid filename
    if re.search(r"\d{8}_\d{6}.BirdNET.selection.table.txt", matches.group(0)):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y%m%d_%H%M%S.BirdNET.selection.table.txt"
        )
    elif re.search(r"\d{8}-\d{6}.BirdNET.selection.table.txt", matches.group(0)):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y%m%d-%H%M%S.BirdNET.selection.table.txt"
        )
    elif re.search(r"\d{14}.BirdNET.selection.table.txt", matches.group(0)):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y%m%d%H%M%S.BirdNET.selection.table.txt"
        )
    elif re.search(r"\d{8}.BirdNET.selection.table.txt", matches.group(0)):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y%m%d.BirdNET.selection.table.txt"
        )
    elif re.search(
        r"\d{4}-\d{2}-\d{2}_\d{6}.BirdNET.selection.table.txt", matches.group(0)
    ):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y-%m-%d_%H%M%S.BirdNET.selection.table.txt"
        )
    elif re.search(
        r"\d{4}-\d{2}-\d{2}T\d{2}_\d{2}_\d{2}\.\d{3}Z\.BirdNET\.selection\.table\.txt",
        matches.group(0),
    ):
        dt = datetime.datetime.strptime(
            matches.group(0), "%Y-%m-%dT%H_%M_%S.%fZ.BirdNET.selection.table.txt"
        )
    return dt


def main(database_path, recreate, results, prefix, index_location_folder):

    logging.basicConfig(
        filename="error_log.log",
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s:%(message)s",
    )

    db = sqlite_utils.Database(database_path, recreate=recreate)

    for result in results:
        print(f"Processing {result}")

        try:
            dt = filename_to_datetime(result)
            print(dt)
            with open(result) as tsv:
                parsed = autocast(parse_tsv(tsv))
                improved = add_info(result, parsed, prefix, index_location_folder, dt)
                db["birdnet"].insert_all(improved)
        except Exception as e:
            logging.error(f"Problem processing {result}: {e}")
            print(f"Problem processing {result}")


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
        type=int,
    )
    parser.add_argument(
        "--recreate",
        help="Recreate the database",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        "--results",
        help="BirdNet result file",
        type=str,
        default=False,
    )
    args = parser.parse_args()

    file_list = args.results.split(" ")
    # file_list = file_list[1:]  # for debugging

    main(
        args.database_path,
        args.recreate,
        file_list,
        args.prefix,
        args.index_location_folder,
    )

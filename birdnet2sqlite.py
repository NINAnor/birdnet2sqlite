#!/usr/bin/env python3

import argparse
import ast
import csv
import datetime
import re

import sqlite_utils

recorder_filename_date = re.compile(r"\d{8}_\d{6}")


def parse_tsv(fp):
    return csv.DictReader(fp, delimiter="\t")


def autocast(obj):
    for row in obj:
        for key, value in row.items():
            try:
                row[key] = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                pass
        yield row


def filename_to_datetime(filename):
    matches = recorder_filename_date.search(filename)
    if not matches:
        return  # Invalid filename
    try:
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d_%H%M%S")
    except ValueError:
        return  # Wrong format
    return dt


def convert_offsets(dt, parsed):
    for item in parsed:
        begin_offset = datetime.timedelta(seconds=item["Begin Time (s)"])
        end_offset = datetime.timedelta(seconds=item["End Time (s)"])
        item["Begin Time"] = dt + begin_offset
        item["End Time"] = dt + end_offset
        del item["Begin Time (s)"]
        del item["End Time (s)"]
        yield item


def main(database_path, recreate, results):
    db = sqlite_utils.Database(database_path, recreate=recreate)
    for result in results:
        with open(result) as tsv:
            parsed = autocast(parse_tsv(tsv))
            dt = filename_to_datetime(result)
            improved = convert_offsets(dt, parsed)
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
    main(args.database_path, args.recreate, args.results)

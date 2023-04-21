#!/usr/bin/env python3

import argparse
import datetime
import pandas as pd
import re

import sqlite_utils

from utils import parse_tsv, autocast
from preprocess_birdnet_result import add_info

recorder_filename_date = re.compile(r"(?:\d{8}_\d{6}.BirdNET.selection.table.txt)|(?:\d{8}-\d{6}.BirdNET.selection.table.txt)|(?:\d{14}.BirdNET.selection.table.txt)|(?:\d{8}.BirdNET.selection.table.txt)|(?:\d{4}-\d{2}-\d{2}_\d{6}.BirdNET.selection.table.txt)")

def filename_to_datetime(filename):
    matches = recorder_filename_date.search(filename)

    if not matches:
        return  # Invalid filename
    if bool(re.search(r'\d{8}_\d{6}.BirdNET.selection.table.txt', matches.group(0))):
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d_%H%M%S.BirdNET.selection.table.txt")    
    if bool(re.search(r'\d{8}-\d{6}.BirdNET.selection.table.txt', matches.group(0))):
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d-%H%M%S.BirdNET.selection.table.txt")
    if bool(re.search(r'\d{14}.BirdNET.selection.table.txt', matches.group(0))):
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d%H%M%S.BirdNET.selection.table.txt")
    if bool(re.search(r'\d{8}.BirdNET.selection.table.txt', matches.group(0))):
        dt = datetime.datetime.strptime(matches.group(0), "%Y%m%d.BirdNET.selection.table.txt")
    if bool(re.search(r'\d{4}-\d{2}-\d{2}_\d{6}.BirdNET.selection.table.txt', matches.group(0))):
        dt = datetime.datetime.strptime(matches.group(0), "%Y-%m-%d_%H%M%S.BirdNET.selection.table.txt")
    return dt
        
def parse_species_list(species_list_file):
    data=pd.read_csv(species_list_file, header=None)
    data_split=data[0].str.split(pat="_",expand=True)
    data_list=data_split[0].values.tolist()
    return data_list
    
def read_translating_file(language):
    filename = "/src/labels/V2.3/BirdNET_GLOBAL_3K_V2.3_Labels_{}.txt".format(language)
    ebird_taxonomy = "/src/labels/V2.3/ebird_taxonomy_v2022.csv"
    
    labels = pd.read_csv(filename, header=None)
    labels = labels[0].str.split("_",expand=True)
    labels.columns = ["SCI_NAME", "Common Name"]
    
    ebtaxonomy = pd.read_csv(ebird_taxonomy, header=0)[["SCI_NAME", "SPECIES_CODE"]]
    df = labels.merge(ebtaxonomy,how="left", on="SCI_NAME")

    return df

def main(database_path, recreate, results, prefix, index_location_folder, species_list_file, language):

    db = sqlite_utils.Database(database_path, recreate=recreate)

    for result in results:
        print(f"Processing {result}")
    try:
        dt = filename_to_datetime(result)
        with open(result) as tsv:
            parsed = autocast(parse_tsv(tsv))
            improved = add_info(result, parsed, prefix, index_location_folder, dt, species_list_file, language)
            db["birdnet"].insert_all(improved)
    except:
        print(f"problem processing {results}")

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
        "--species_list_file",
        help="Path to a file containing the species of interest",
        default="None",
        type=str
    )
    parser.add_argument(
        "--language",
        help="Translating the species names in the language of interest",
        default="None",
        type=str
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
        default=False,
    )
    args = parser.parse_args()
    
    species_list = parse_species_list(args.species_list_file) if args.species_list_file != "None" else None
    translation_file = read_translating_file(args.language) if args.language != "None" else None

    if species_list is not None:
        print("Loading the species list {}".format(args.species_list_file))
    if translation_file is not None:
        print("Loading the {} translation file".format(args.language))
    
    main(args.database_path, 
        args.recreate, 
        args.results, 
        args.prefix, 
        args.index_location_folder, 
        species_list, 
        translation_file)

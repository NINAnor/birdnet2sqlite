import argparse
import os
import datetime
import pandas as pd

from utils import parse_tsv, autocast

def add_location(item, filename, index_location_folder):
    location = filename.split("/")[index_location_folder]
    item["location"] = location
    return item
        
def add_prefix(item, filename):
    prefix = filename.split('/')[-1].split('_')[0]
    item["prefix"] = prefix
    return item
        
def add_filename(item, filename):
    file_name = filename.split('/')[-1]
    item["filename"] = file_name
    return item   
    
def add_date(item, dt):
    dt_ymd = dt.strftime('%Y-%m-%d')
    item["date"] = dt_ymd
    return item
    
def add_time_detection(item, dt):
    offset = datetime.timedelta(seconds=item["Begin Time (s)"])
    dt_offset = dt + offset
    item["time_detection"] = dt_offset.strftime('%H:%M:%S')
    return item
    
def filter_species(item, species_list):
    if item["Species Code"] in species_list:
        item["in_custom_list"] = True
    else
        item["in_custom_list"] = False
        
def translate_common_name(item, translation_file):
    translated_name = translation_file.loc[translation_file["Species Code"] == item["Species Code"], "Common Name"].iloc[0]
    item["Common Name"] = translated_name if not pd.isna(translated_name) else item["Common name"]
    return item
    
def add_info(filename, parsed, prefix, index_location_folder, dt, species_list_file, translation_file):
    
    for item in parsed:
        improved = add_location(item, filename, index_location_folder)
        improved = add_time_detection(item, dt)
        improved = add_date(item, dt)
        
        if prefix:
            improved = add_prefix(item, filename)
            
        improved = add_filename(item, filename)
        
        if species_list_file is not "None":
            improved=filter_species(improved)
            
        if language is not "None":
            improved=translate_common_name(improved, translation_file)
            
        yield improved
        

        

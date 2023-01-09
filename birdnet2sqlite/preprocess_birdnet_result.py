import argparse
import os
import datetime

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
    file_name = filename.split('/')[-1].split('.')[0]
    item["filename"] = file_name
    return item   
    
def add_time_detection(item, dt):
    offset = datetime.timedelta(seconds=item["Begin Time (s)"])
    dt_offset = dt + offset
    item["time_detection"] = dt_offset.strftime('%Y-%m-%d %H:%M:%S')
    return item
        
def add_info(filename, parsed, prefix, index_location_folder, dt):
    
    for item in parsed:
        improved = add_location(item, filename, index_location_folder)
        improved = add_time_detection(item, dt)
        if prefix:
            improved = add_prefix(item, filename)
        improved = add_filename(item, filename)
        yield item
        

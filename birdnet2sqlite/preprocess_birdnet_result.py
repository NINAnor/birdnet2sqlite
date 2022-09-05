import argparse
import os

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
        
def add_info(filename, parsed, prefix, index_location_folder):
    
    for item in parsed:
        if prefix:
            improved = add_prefix(item, filename)
        improved = add_filename(item, filename)
        improved = add_location(item, filename, index_location_folder)
        yield item
        

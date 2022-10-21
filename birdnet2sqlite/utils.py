import ast
import csv

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

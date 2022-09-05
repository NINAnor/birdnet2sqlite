Converts a bunch of TSV files produced by BirdNet to a SQLite database.
It expects to find a YYYYmmdd_HHMMSS string in the filename.

# How to build and run locally (with Docker)

### Build the docker image

```
docker build -t birdnet2sqlite -f Dockerfile .
```

### Run `birdnet2sqlite.sh`

`./birdnet2sqlite.sh BASE_FOLDER DB_NAME IS_PREFIX INDEX_LOCATION_FOLDER`

With:

- `BASE_FOLDER`: The folder containing all the birdnet output files.
- `DB_NAME`: The name you want to give to the database. **Note** that it has to end with `.sqlite` (e.g. `my_database.sqplite`).
- `IS_PREFIX`: Is the filename formatted such as `PREFIX_YYYmmdd_HHMMSS`? Either `True` or `False`.
- `INDEX_LOCATION_FOLDER`: The position of the foldr name that will be used as a `location` column in the database (e.g. `INDEX_LOCATION_FOLDER` would be set to `-2` for `path/to/data/my_area/file.txt`).


# Use the database in R

To open the created databse in R you can use the script below:

```
library(RSQLite)
library(DBI)

setwd("path/to/working/directory")
sqlite <- dbDriver("SQLite")
conn <- dbConnect(sqlite, "my_database.sqlite")

# For the full dataset
data <- dbReadTable(conn, "birdnet")

# For a subset of the dataset 
res <- dbSendQuery(con, "SELECT * FROM birdnet WHERE location = X")
```

Converts a bunch of TSV files produced by BirdNet to a SQLite database.
It expects to find a YYYYmmdd_HHMMSS string in the filename.

# How to build and run locally (with Docker)

```
DOCKER_BUILDKIT=1 docker build -t localhost/birdnet2sqlite .
./birdnet2sqlite BASE_FOLDER DB_NAME
```

With:

- `BASE_FOLDER` the folder containing all the birdnet output files
- `DB_NAME` the name you want to give to the database. **Note** that it has to end with `.sqlite` (e.g. `my_database.sqplite`) 


# Use the database in R

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

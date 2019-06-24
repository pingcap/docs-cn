---
title: Import Example Database
summary: Install the Bikeshare example database.
category: how-to 
aliases: ['/docs/bikeshare-example-database/']
---

# Import Example Database

Examples used in the TiDB manual use [System Data](https://www.capitalbikeshare.com/system-data) from Capital Bikeshare, released under the [Capital Bikeshare Data License Agreement](https://www.capitalbikeshare.com/data-license-agreement).

## Download all data files

The system data is available [for download in .zip files](https://s3.amazonaws.com/capitalbikeshare-data/index.html) organized per year. Downloading and extracting all files requires approximately 3GB of disk space. To download all files for years 2010-2017 using a bash script:

```bash
mkdir -p bikeshare-data && cd bikeshare-data

curl -L --remote-name-all https://s3.amazonaws.com/capitalbikeshare-data/{2010..2017}-capitalbikeshare-tripdata.zip
unzip \*-tripdata.zip
```

## Load data into TiDB

The system data can be imported into TiDB using the following schema:

```sql
CREATE DATABASE bikeshare;
USE bikeshare;

CREATE TABLE trips (
 trip_id bigint NOT NULL PRIMARY KEY auto_increment,
 duration integer not null,
 start_date datetime,
 end_date datetime,
 start_station_number integer,
 start_station varchar(255),
 end_station_number integer,
 end_station varchar(255),
 bike_number varchar(255),
 member_type varchar(255)
);
```

You can import files individually using the example `LOAD DATA` command here, or import all files using the bash loop below:

```sql
LOAD DATA LOCAL INFILE '2017Q1-capitalbikeshare-tripdata.csv' INTO TABLE trips
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
(duration, start_date, end_date, start_station_number, start_station, 
end_station_number, end_station, bike_number, member_type);
```

### Import all files

To import all `*.csv` files into TiDB in a bash loop:

```bash
for FILE in `ls *.csv`; do
 echo "== $FILE =="
 mysql bikeshare -e "LOAD DATA LOCAL INFILE '${FILE}' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);"
done;
```

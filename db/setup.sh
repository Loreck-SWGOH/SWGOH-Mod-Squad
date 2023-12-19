#!/bin/bash

mypath=`realpath "$0"`
mybase=`dirname "$mypath"`
echo $mypath
echo $mybase
cd "$mybase"

datadir="${1:-data/}"
echo $datadir
if [ ! -d $datadir ] ; then
    echo "$datadir does not exist under $mybase"
    exit 1
fi

source ../.flaskenv
dbname=$DB_NAME
echo $dbname

if [[ -n `psql -lqt | cut -d \| -f 1 | grep -w "$dbname"` ]]; then
    echo "Dropping database"
    dropdb $dbname
fi
echo "Creating database"
createdb $dbname
echo "Database created"

psql -af create.sql $dbname
echo $datadir
cd "$datadir"
psql -af "$mybase/load.sql" $dbname

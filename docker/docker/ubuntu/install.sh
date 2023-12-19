#!/bin/bash

######################################################################
# Basics:
apt-get -qq update
DEBIAN_FRONTEND=noninteractive apt-get -yq -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
apt-get -qq --yes install wget nano vim less gnupg curl man coreutils git

apt-get -qq --yes install systemd locales
timedatectl set-timezone America/New_York
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
apt-get -qq --yes install tzdata

######################################################################
# Python 3.11:
apt-get -qq --yes install python3.11
update-alternatives --install /usr/bin/python python /usr/bin/python3.11 11
apt-get -qq --yes install python3-pip
python -m pip install poetry

######################################################################
# Database clients:
apt-get -qq --yes install postgresql-client libpq-dev
python -m pip install psycopg2-binary SQLAlchemy

######################################################################
# XML:
apt-get -qq --yes install libxml2-dev libxslt1-dev libxml2-utils
apt-get -qq --yes install libsaxonb-java
python -m pip install lxml

######################################################################
# RA:
python -m pip install radb

######################################################################
# MongoDB client:
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /etc/apt/trusted.gpg.d/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" > /etc/apt/sources.list.d/mongodb-org-7.0.list
apt-get -qq --yes update
apt-get -qq --yes install mongodb-mongosh mongodb-org-tools
python -m pip install pymongo

######################################################################
# Spark:
apt-get -qq --yes install openjdk-8-jdk
python -m pip install pyspark

#!/bin/bash

APPS="users addresses batches businesses charities items members orders pages recipes surveys transactions"
rm db.sqlite3

for app in $APPS
do
rm $app/migrations/0*.py
done
./manage makemigrations
./manage migrate
for app in $APPS
do
echo $app
for fixture in $app/fixtures/*.json
do
./manage loaddata $fixture
done
done

./manage runscript member_import


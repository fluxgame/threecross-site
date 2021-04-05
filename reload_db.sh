#!/bin/bash

APPS="users addresses batches businesses charities items members orders pages recipes surveys transactions"
rm db.sqlite3

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


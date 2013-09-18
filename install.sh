#!/bin/bash
#suggested way to execute this script: sudo bash install.sh /usr/share/accomplishments

echo "Copying accomplishments to $1"
rm -rf $1/accomplishments/ubuntu-community
mkdir -p $1/accomplishments/ubuntu-community
cp -r ./accomplishments/ubuntu-community/* $1/accomplishments/ubuntu-community/

rm -rf $1/scripts/ubuntu-community
mkdir -p $1/scripts/ubuntu-community
cp -r ./scripts/ubuntu-community/* $1/scripts/ubuntu-community/

rm -rf $1/tests/ubuntu-community
mkdir -p $1/tests/ubuntu-community
cp -r ./tests/ubuntu-community/* $1/scripts/ubuntu-community/
echo "Done!"

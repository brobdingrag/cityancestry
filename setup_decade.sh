#!/bin/bash

# Set the path to the downloads directory (change this to your own path)
DOWNLOADS_PATH=~/Downloads

# Check if arguments are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <nhgis_name> <decade>"
    echo "Example: $0 nhgis0009 2010"
    exit 1
fi

# Read command line arguments
nhgis_name=$1
decade=$2

cd data

# Move csv and shape files to the current directory
cp $DOWNLOADS_PATH/${nhgis_name}_csv.zip ./
cp $DOWNLOADS_PATH/${nhgis_name}_shape.zip ./

# Unzip the files and delete the zip files in one command
unzip ${nhgis_name}_csv.zip
unzip ${nhgis_name}_shape.zip

# Go into the shape directory and unzip the files
cd ${nhgis_name}_shape
unzip '*.zip'
cd ..

# Remove the zip files
rm ${nhgis_name}_csv.zip
rm ${nhgis_name}_shape.zip

# Move the shape files to the current directory
mv ${nhgis_name}_shape geo_${decade}
mv ${nhgis_name}_csv demo_${decade}


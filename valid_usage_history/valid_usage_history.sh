#! /bin/bash
# Basic count stats from the VU database in CSV format for spreadsheet loading.
# The database was created 2016-10-05, a couple days before sdk-1.0.30.0.

#set -o errexit
set -o nounset

COUNT="grep -c"

cd "/home/mikew/gits/github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers"
INFILE="layers/vk_validation_error_database.txt"

if [ ! -r "$INFILE" ]
then
    echo "ERROR: \"$INFILE\" is not readable." >&2
    exit 1
fi

echo "\"\",\"\",\"All VUs\",\"\",\"\",\"\",\"\",\"Implicit VUs\",\"\",\"\",\"\",\"Tests\",\"\",\"\",\"\""
echo "\"Tag\",\"Date\",\"\",\"Total\",\"Done (Y)\",\"Not done (N)\",\"Unknown (U)\",\"\",\"Total\",\"Done (Y)\",\"Not done (N)\",\"\",\"None\",\"Unknown\",\"NotTestable\""

for i in sdk-1.0.30.0 sdk-1.0.32.0 sdk-1.0.33.0 sdk-1.0.37.0 sdk-1.0.38.0 sdk-1.0.39.1 sdk-1.0.42.2 sdk-1.0.46.0 sdk-1.0.51.0 sdk-1.0.54.0 sdk-1.0.57.0 master
do
    git checkout $i > /dev/null 2>&1
    echo "\"$(git describe --all --long)\",\"\",\"\",$($COUNT '^VALIDATION_ERROR_' $INFILE),$($COUNT '~^~Y~^~' $INFILE),$($COUNT '~^~N~^~' $INFILE),$($COUNT '~^~U~^~' $INFILE),\"\",$($COUNT 'implicit' $INFILE),$(grep 'implicit' $INFILE | $COUNT '~^~Y~^~'),$(grep 'implicit' $INFILE | $COUNT '~^~N~^~'),\"\",$($COUNT '~^~None~^~' $INFILE),$($COUNT '~^~Unknown~^~' $INFILE),$($COUNT '~^~NotTestable~^~' $INFILE)"
    git show --stat | grep "Date"
    echo
done

# vim: set sw=4 ts=8 et ic ai:

#!/bin/bash

if [ $# -ne 1 ] || [ ! -d $1 ]; then
	echo "Usage: $0 DIR_DATA"
	exit 1
fi

pushd $1 &> /dev/null
for file in $(ls *-prelucrat.csv); do
	xls_file=$(basename $file .csv).xls
	echo "Convert $file to $xls_file."
	ssconvert $file $xls_file &> /dev/null
done
popd &> /dev/null

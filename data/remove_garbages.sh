#!/bin/bash


dir=$1

cd $dir
for file in ./*.csv
do
	echo $file
	
	l_num=$(cat ${file} | wc -l)
	garbage_lines=5
	l_num=$(($l_num-$garbage_lines))
        
	echo $l_num
	
	tail -n $l_num $file > "${file%.csv}-fixed.csv"
	mv "${file%.csv}-fixed.csv" $file

done


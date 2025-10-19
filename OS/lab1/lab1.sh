#!/bin/bash

min=$1
max=$2
owner_name=$3
Directory=$4
file_path=$5
amnt_of_files=0
> "$file_path"
find "$Directory" -type f | while read file ;  
do
    if [ -f "$file" ]; then
    filesize=$(stat -c%s "$file")
    file_owner=$(stat -c%U "$file")
        if [ "$filesize" -le "$max" ] && [ "$filesize" -ge "$min" ] && [ "$file_owner" = "$owner_name" ] ; then
        filename=$(basename "$file")
        	echo  "Путь:$file,Имя:$filename,Размер:$filesize байт">>"$file_path"
        	echo  "Путь:$file,Имя:$filename,Размер:$filesize байт"
        	amnt_of_files=$(expr $amnt_of_files + 1)
        	echo -e " Количество: $amnt_of_files"
	fi
	
    fi  
         	
done
#sh lab1.sh 1 1000 kirillromanoff /home/kirillromanoff/University ui.txt

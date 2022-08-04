#! /bin/bash

rm final_result.txt
for ((i=1; i<=10; i++))
do
     cat /dev/urandom | tr -dc "[^a-zA-Z0-9]" | head -c 78 > testfile.txt
     echo '\n' >> testfile.txt
     for ((j=1; j<=10; j++))
     do
	 python3 encoder.py testfile.txt && python3 decoder.py > result.txt
	 diff -s testfile.txt result.txt >> final_result.txt 
     done
done

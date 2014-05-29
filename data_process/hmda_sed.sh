##this shell script replaces any double quotes next to each other with nothing
##this allows for importing of null numeric fields into postgres

sed 's/""//g' hmda_lar_al.csv > ./reformat/hmda_lar_al.csv

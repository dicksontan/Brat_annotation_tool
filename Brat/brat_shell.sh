#! /bin/bash

echo 'Creating Config File...'

echo > ./desktop/brat_annotations/annotation.conf

echo 'Creating Entity Files...'

python ./Desktop/Vs_Code_Projects/brat/brat_run.py

echo 'Transferring Entity Files to Linux VM containing volumes...'

chmod -R u=rwx,g=rwx,o=rwx ./desktop/brat_annotations

docker cp ./desktop/brat_annotations c5a09d229264:bratdata/mt_samples

echo 'Entity Files Transferred'

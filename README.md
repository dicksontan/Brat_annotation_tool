### Contents:
- [Prologue](#prologue)
- [Datasets](#Datasets)
- [Requirements/Packages](#Requirements-Packages)
- [Docker Set-up](#Docker-Set-up)
- [Testing file transfer and creating input folder](#Testing-file-transfer-and-creating-input-folder)
- [Creating Labels DataFrame for evauation](#Creating-Labels-DataFrame-for-evauation)
- [Brat_model notebook](#Brat_model-notebook)
- [Other Useful Shell Commands](#Other-Useful-Shell-Commands)

---

### Prologue

This is a guide on how to set-up the brat annotation tool through docker and do Named-Entity Recognition Labelling. Do note documententation is based on MacOS.

---

### Datasets

The clinical notes dataset used for this project is based off data scraped from mt samples.

[Dataset Link](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions)

---

### Requirements-Packages

I have highlighted the more important packages in the requirements.txt file. Notably, you will have to use python 3.6 if you want to run spacey. You will also need to download the ner packages, which can be referenced [here](https://github.com/allenai/scispacy)

---

### Docker Set-Up

Reference: [cassj/brat](https://user-images.githubusercontent.com/50508538/187128975-c774562f-21dc-44dc-b7a8-92c11956e7f3.png)

In terminal, input the following commands:

```
docker volume create --name brat-data
docker volume create --name brat-cfg
```

Mapping port 81 on your local to brat:

```
docker run --platform linux/amd64 -it --privileged --pid=host --name=brat1 -d -p 81:80 -v brat-data:/bratdata -v brat-cfg:/bratcfg -e BRAT_USERNAME=brat -e BRAT_PASSWORD=brat -e BRAT_EMAIL=brat@example.com cassj/brat
```
### Testing file transfer and creating input folder

To get container id:

```
docker ps
```

Create a folder called mt_samples on your desktop. Assuming your container id is c5a09d229264, run the following to transfer the folder in:

```
docker cp ./desktop/mt_samples c5a09d229264:bratdata
```

Open a new terminal and access container bash through:

```
docker exec -it brat1 /bin/bash
cd bratdata
ls
```

Confirm that you are able to see mt_samples folder. At this point in time, you should be able to open the browser UI of brat through docker to see if mt_samples folder resides in it. Note that in the viewer, it may state that you do not have permissions in a certain file etc. If thats the case, cd to that file's directory and enter the following:

```
chmod +wrx [filename]

e.g. chmod +wrx brat-v1.3_crunchy_Frog.tar.gz

```
Next, download the brat_shell.sh file from this repo and put it in your desktop. 

Create a brat_annotations folder on your desktop.

Download the python files brat_run.py, brat_clean.py, extract_labels_to_csv.py

In brat_run.py and extract_labels_to_csv.py, under: if __name__ == "__main__", make sure you read the required input instructions. When you run the shell commands, the terminal will prompt you for inputs to be fed into the python script.

Also, change the python file path in brat_shell.sh if required.

Then, everytime you want to run the script, enter this into terminal (make sure you are using environment that has python 3.6):

```
./desktop/brat_shell.sh
```

Go back into your browser UI and view the annotations.

In the brat browser UI, login with user: brat, pass: brat, to make changes to annotations.

---

### Creating Labels DataFrame for model evauation

After you have manually reviewed and corrected data inside brat, you may want to extract labelling info for model evaluation e.g. creation of confusion matrix. We have created a python file to create csv files with labelling info after you have extracted the new annotated files from the brat container. This python file will create 2 csvs, 1 csv with labelling info from your labelling, and another csv with labelling info from spacy. You first have to create a extract_labels_csv folder in the brat_extracted folder. Then, read the input instructions in the extract_labels_to_csv.py file and it. Sample Query:



```
python /Users/user_1/Desktop/Vs_Code_Projects/Brat/extract_labels_to_csv.py
```

|tag_index|class|start|end|entity|index|
|---|---|---|---|---|---|
|T1|ORGAN|871|878|abdomen|110|
|T2|SIMPLE CHEMICAL|900|910|loratadine|110|

---

### Brat_scrapbook notebook

EXploratory data cleaning, visualizations and other functions is provided in this notebook.

---

### Other Useful Shell Commands

For transferring files out from brat container, create a folder called brat_extracted on your desktop and enter into terminal:

```
docker cp c5a09d229264:bratdata/mt_samples/brat_annotations ./desktop/brat_extracted
```

For extracting selected files (e.g. only those that you reviewed/did manual labelling), create a folder called "annotated" inside brat_extracted. Note down the index which you want to extract (e.g. 0043,0173). Then enter into terminal:

```
list=(0043 0173)
for val in $list; do cp -v ./desktop/brat_extracted/brat_annotations/$val* ./desktop/brat_extracted/annotated;done
```

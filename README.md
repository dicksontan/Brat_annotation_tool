### Contents:
- [Prologue](#prologue)
- [Datasets](#Datasets)
- [Requirements/Packages](#Requirements-Packages)
- [Docker Set-up](#Docker-Set-up)
- [Conclusion and Recommendations](#Conclusion-and-Recommendations)
- [Sources](#Sources)

---

### Prologue

This is a guide on how to set-up the brat annotation tool through docker and do Named-Entity Recognition Labelling. Do note documententation is based on MacOS.

---

### Datasets

The clinical notes dataset used for this project is based off data scraped from mt samples.

[Dataset Link](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions)

---

### Requirements-Packages

I have highlighted the more important packages in the requirements.txt file. Notably, you will have to use python 3.6 if you want to run spacey.

---

### Docker Set-up

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

To get image id:

```
docker ps
```

Create a folder called mt_samples on your desktop. Assuming your container id is c5a09d229264, run the following to transfer the folder in:

```
docker cp ./desktop/mt_samples c5a09d229264:bratdata/examples
```

Open a new terminal and access container bash through:

```
docker exec -it brat1 /bin/bash
cd bratdata
cd examples
ls
```

Confirm that you are able to see mt_samples folder in examples folder. At this point in time, you should be able to open the UI of brat through docker and view the examples folder to see if mt_samples folder resides in it. Note that in the viewer, it may state that you do not have permissions in a certain file etc. If thats the case, cd to that file's directory and enter the following:

```
chmod +wrx [filename]
```
Next, download the brat_shell.sh file and put it in your desktop. Create a brat_annotations folder on your desktop.

Then, everytime you want to run the script, enter this into terminal:

```
./desktop/brat_shell.sh
```

---

### Conclusion and Recommendations

---

### Sources
    

1. https://www.cityofames.org/government/departments-divisions-i-z/public-works/alley-maintenance

   Summary: Government website summarising alley length where we infer that many houses probably will not have alleys.

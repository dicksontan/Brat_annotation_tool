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
### Testing file transfer

To get image id:

```
docker ps
```

Create a folder called brat_annotations and touch a.txt in the folder. Assuming your container id is c5a09d229264, run the following to transfer files in:

```
docker cp ./desktop/brat_annotations/a.txt c5a09d229264:bratdata/examples 
```

Open a new terminal and access container bash through:

```
docker exec -it brat1 /bin/bash
cd bratdata
cd examples
ls
```

Confirm that you are able to see a.txt in examples folder. At this point in time, you should be able to open the UI of brat through docker and view the examples folder to see if a.txt resides in it.

Then remove the file:

```
rm a.txt
```

---

### Conclusion and Recommendations

* Neighborhood: For neighborhoods, there is only a strong positive relationship when the house is in a wealthier neighborhood such as Stone Brook or Northridge Heights. This may be due to buyers being able to flaunt one's status <sup> 2 </sup>. Hence, sellers who have houses in these areas can expect to price their houses higher.

* Quality: We see that we have to care about many aspects of quality, such as exterior quality, kitchen quality and also basement quality. The materials used for foundation also plays an important role in fetching higher prices. Sellers should hence ensure that their exterior is refurbished with the best materials. Appliances and equipment in the kitchen should also be of high quality.

* Condition: We observe that houses with better condition do fetch higher prices. Hence, sellers should ensure that the house is undamaged and any damage is repaired immediately.

* Age: Out of all the features, age since last remodelling/addition has the highest negative relationship. We see a drop of -$7,813 with each unit increase of age since remodelled. Hence, sellers have to ensure that they modify or remodel whenever possible. Moreover, buyers hoping to resell houses should also not buy houses that are too old as old houses generally fetch lower prices.

* Size: As expected, the size of the house will affect the house price. Having more rooms above ground level dramatically increases the cost of the house, especially in combination with a wealthy neighborhood. As an unfinished basement has a high negative relationship with price, sellers should ensure that their basement is completed before selling.
---

### Sources
    

1. https://www.cityofames.org/government/departments-divisions-i-z/public-works/alley-maintenance

   Summary: Government website summarising alley length where we infer that many houses probably will not have alleys.
   
2. https://www.census.gov/construction/chars/
    
   Summary: Goverment data which shows number of houses that own fireplaces broken down by year. From 2006-2010, about 40% of houses do not have fireplaces.
   
3. https://statisticalatlas.com/neighborhood/Iowa/Ames/Stone-Brooke/Household-Income

   Summary: The source displays graphs that show how Stone Brook had a higher household income at each percentile as compared to the general Ames population.
   
4. https://www.weichert.com/search/community/neighborhood.aspx?hood=60290

   Summary: The article displayed graphs which show that 75% of the workforce in NorthRidge Heights were white collar jobs, indicating higher wealth.
   
5. https://www.99.co/singapore/insider/factors-affecting-resale-value/

   Summary: We see that age, condition, size and location all play a part in housing valuation.


6. https://www.thebalance.com/pricing-houses-to-sell-1798968
   
   Summary: Perceptions of desirability causes neighborhoods to have a relationship with house prices. Wealthier neighborhoods allows for one to flaunt their status. Age of the house is also crucial


7. https://www.compmort.com/home-location-and-property-value/

   Summary: This article highlights the importance of neighborhoods and proximity to amenities like schools and hospitals.
   

8. https://www.investopedia.com/articles/mortages-real-estate/11/factors-affecting-real-estate-market.asp
   
   Summary: This article highlights how government policies/subsidies and economic factors like inflation and supply/demand have a relationship with house prices.

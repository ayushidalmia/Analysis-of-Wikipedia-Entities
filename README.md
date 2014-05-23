Analysis-of-Wikipedia-Entities
==============================

This repository consists of the project done as part of the course Web Mining- Monsoon 2013. The course was instructed by [Dr. Manish Gupta](http://research.microsoft.com/en-us/people/gmanish/)

A detailed report is available <a href="https://drive.google.com/file/d/0B87x7EOOS4ztdVRuVHlWR3JIQnM/edit?usp=sharing",target="blank">here</a>

##Requirements
Python 2.6 or Higher
Java

Python Library  
sqlite3

##Problem
Analysis of entity types on Wikipedia is done on the entire Wikipedia XML Dump. We are asked to extract information about various entity types. 

The code contains the following files/folders:

* extractPages.py  
It takes the entire dump and returns each page of the dump.

* wikiXML  
This folder contains the code for extracting infoboxes from page. It returns files containing infoboxes for each page.

* extractEntityTypes.py  
It takes as input the infoboxes and returns the following files:  
1)Files for each entity type: It contains all possible attributes, the datatype, max, min values and unit for each entity type. Each file contains tab separated values as follows:  

Attribute_name Attribute_Type Min_Attribute_Value Max_Attribute_Value Unit_of_the_Attribute

2)NumberOfEntities:It contains number of entities for each entity type

3)AverageNumberOfAttributes: It contains the average number of attributes for each entity type
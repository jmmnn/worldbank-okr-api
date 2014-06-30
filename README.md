OpenKnowledgeRepo
=================

Pipeline for querying the World Bank Open Knowledge Repository

# OKR-Sumit Pipeline
The OKR API-Querying Pipeline consists of 5 classes and methods,
each of which handle a broad purpose in the pipeline:

1. **Querying** - Creating the API query url and making HTTP requests to the OKR server
2. **Processing** - Converting xml to dictionary/json format
3. **Formatting** - Modifying the uketd dublin core schema to fit sumit-okr schema
4. **Flow Control** - A class that handles flow control of HTTP requests through resumption tokens
5. **Database Syncing** - A class that handles syncing json data to a Mongo document database.

# Access to subset of dataset (100 publications)
You can find a .json file containing 100 publications of the OKR [here](https://github.com/the-sumit/OKR/tree/master/local_DS). Each the .json file hashes each document with a unique okr_id, where each document conforms to the following schema:

#### Document
*  **okrID**: the unique okr id for each publication  
*  **uri**: the uri pointing to the publication page on the okr website  
*  **issueDate**: issue date of publication  
*  **pubtype**: type of publication e.g. 'World Bank Publication'  
*  **title**: publication title  
*  **abstract**: publication summary  
*  **subjectTags**: okr-subject metatags  
*  **pdfUrl**: url pointing to the pdf  
*  **txtUrl**: url pointing to the txt  
*  **thumbUrl**: url pointing to a thumbnail image  
*  **licenseUrl**: url pointing to the license documentations  

#### Note:
The .nrjson file is 'not really json', because it's a file that seperates each .json document by line instead of hashing each object with a unique id.

# Functional APIs:
1. Querying Module
2. Processing Module
3. Formatting Module

# Todo
1. Flow control
2. Database Syncing
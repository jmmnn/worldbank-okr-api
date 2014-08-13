# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Class for processing API response from OKR to obtain
necessary metadata.

For more information about the API go to:
https://openknowledge.worldbank.org/harvesting-the-okr

SUMIT-OKR Schema:

'''

import os
import bs4
import json
from schema import schemaHeader, schemaMetadata


class Processor(object):

    def __init__(self, response, responseFormat, soupifyResponse=False):
        self.format = responseFormat
        self.response = response
        self.recordList = None

        # resumption token metadata
        self.resumptionToken = None
        self.completeListSize = None

        # xml element and API request metadata attribute
        self.xmlMetadata = None
        self.requestMetadata = None

        # counter attributes for iterating through responses and queries
        self.cursor = None  # cursor is a tag element in a OKR query response
        self.recordCount = 0  # total records processed within response

        # calling method to soupify the xml response and getRecordList
        if soupifyResponse is True:
            self.soupify()
            self.getRecordList()

        # calling methods to get resumptionToken and completeListSize
        self.getResumptionToken()

    def soupify(self):
        self.response = bs4.BeautifulSoup(self.response, self.format)

    def getRecordList(self):
        self.recordList = self.response.find_all('record')

    def getResumptionToken(self):
        try:
            token = self.response.find('resumptionToken')
        except:
            print 'no resumption token in the response'

        self.resumptionToken = token.get_text()
        self.cursor = token['cursor']

        if self.completeListSize is None:
            self.completeListSize = int(token['completeListSize'])

        return self.resumptionToken

    def processRecord(self, record):
        '''
        Method for processing a single record
        '''
        recordDict = {}
        #parse header
        recordDict = self.parseRecord(recordDict, record,
                                      schemaHeader, 'header')
        #parse metadata
        recordDict = self.parseRecord(recordDict, record,
                                      schemaMetadata, 'metadata')
        return recordDict

    def parseRecord(self, recordDict, record, schema, parseTag):
        '''
        Helper function for processRecord method
        '''
        tag = record.find(parseTag)
        for field in schema.keys():
            elements = tag.find_all(schema[field])
            recordDict[field] = [e.get_text() for e in elements]

        return recordDict

    def record2json(self, recordDict):
        '''
        A method for converting a record dictionary into json format
        '''
        return json.dumps(recordDict)

    def processResponse(self, count=None, processFormat='json'):
        '''
        A generator method for processing a query response

        'count' is an optional argument for specifying how
        many records to process in the response.
        by default, processes
        '''

        if count:
            size = count
        else:
            size = self.completeListSize
        for i in range(size):
            if processFormat == 'json':
                yield self.processRecord(self.recordList[i])
            if processFormat == 'xml':
                yield self.recordList[i]

    def save2file(self, filePath, record):
        '''
        A method for saving a record to file
        '''
        with open(filePath, 'r+') as recordFile:
            if len(recordFile.readlines()) == 0:
                recordFile.write(record)
            else:
                recordFile.write('\n%s' % record)

    def initJson(self, filePath):
        '''
        Method for initializing a json file.
        '''
        with open(filePath, mode='w') as f:
            json.dump({}, f)

    def save2json(self, filePath, recordDict):
        '''
        Saves individual json objects to json file
        specified in filePath
        '''
        with open(filePath) as f:
            data = json.load(f)

        data.update(recordDict)

        with open(filePath, 'w') as f:
            json.dump(data, f)

    # methods to build out once we need to start caching queries
    def cacheXmlMetadata(self):
        pass

    def cacheRequestMetadata(self):
        pass

if __name__ == "__main__":

    with open('./sampleData/sampleResponse.xml') as response:
        data = Processor(response.read(), 'xml', soupifyResponse=True)

    #print data.getResumptionToken()
    '''
    #### Test for Processor.processRecord function ####
    record = data.response.find_all('record')[0]
    for k, v in data.processRecord(record).items():
        print k, v
        print '\n'

    #### Test script for getResumptionToken method ####
    token = data.getResumptionToken()
    print data.resumptionToken, data.completeListSize

    #### Test script for record2json ####
    record = data.response.find_all('record')[0]
    jsonRecord = json.dumps(data.processRecord(record))
    with open('./test.json', 'w') as testFile:
        testFile.write(jsonRecord)

    #### Test script for processResponse ####
    recordGen = data.processResponse()
    print data.processResponse()
    for record in recordGen:
        print record


    #### Test script for saving json records to .nrjson format ####

    #------------------------------------------------#
    # .nrjson == "not really json"                   #
    # each json document is saved to a file          #
    # that seperates each json object by a linebreak #
    #------------------------------------------------#

    recordGen = data.processResponse()
    filePath = '../local_DS/sampleResponse.rnjson'

    count = 0
    for record in recordGen:
        line = data.record2json(record)
        if count == 0:
            data.save2file(filePath, line)
        else:
            data.append2file(filePath, line)
        count += 1


    #### Test script for saving json records in .json format ####

    # count is an optional argument for specifying how
    # many records to process in the response.
    # by default, processes the entire response

    recordGen = data.processResponse(count=100)
    filePath = '../local_DS/test.json'

    data.initJson(filePath)

    for record in recordGen:
        okr_id = record['okr_id'][0]
        jsonRecord = {okr_id: record}
        data.save2json(filePath, jsonRecord)
    '''

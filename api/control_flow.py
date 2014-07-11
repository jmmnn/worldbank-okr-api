# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Class for handling the API query pipeline to local

For more information about the API, go to:
https://openknowledge.worldbank.org/harvesting-the-okr
'''

from query import QueryContainer
from process import Processor
from format_record import Formatter
import json


class FlowController(object):

    def __init__(self, baseUrl, initParams, formatter=Formatter()):

        #initializing the queryContainer with parameters and initial request
        self.query = QueryContainer(baseUrl)
        self.params = initParams
        self.query.setParameters(self.params)
        self.query.setRequest()

        #initialize Formatter object
        #this object converts responses to Sumit's json format
        self.formatter = formatter

        #initialize the processor
        self.query.getResponse()
        self.processor = Processor(self.query.response,
                                   'xml', soupifyResponse=True)

    def initFlow(self, harvester,
                 filePath=None,
                 connector=None,
                 processFormat=None,
                 limit=None):
        '''
        sets limit to how many records are stored
        '''
        self.harvest = harvester
        self.filePath = filePath
        self.connector = connector
        self.processFormat = processFormat
        self.responseCount = len(self.processor.recordList)

        if limit:
            self.limit = limit
        else:
            self.limit = self.processor.completeListSize

        if self.limit < self.responseCount:
            self.responseCount = self.limit

        print self.limit
        self.totalRecordCount = 0

        #create empty file if filePath is specified
        if self.filePath:
            with open(self.filePath, 'w') as f:
                f.write('')

        while self.totalRecordCount < self.limit:
            #harvest responses from current processor state
            self.harvest(self.filePath, self.connector, self.processFormat)
            self.updateParams()
            self.updateRequest()
            self.updateProcessor()
            self.responseCount = len(self.processor.recordList)
            print "updating pipeline for next HTTP call..."
            print "resumption token: %s" % self.params['resumptionToken']

    def harvest(self, filePath=None,
                connector=None,
                processFormat=None):
        '''
        Method that saves multiple documents to file

        *connector* takes a function as an argument that saves file to
        to a cloud server storage system, e.g. aws-s3.

        The connector function should be able to handle the http calls
        to the server. For now it works for a key-value data store and takes
        two arguments, one for the key name, and the other the content of the
        file to be saved
        '''
        recordList = self.processor.processResponse(
            count=self.responseCount,
            processFormat=processFormat)

        for r in recordList:
            self.totalRecordCount += 1

            #serialize json or xml format to be saved to file or
            #to a server specified by the connector function
            if processFormat == 'json':
                formattedRecord = self.formatter.formatRecord(r)
                keyName = formattedRecord['okrID']
                record = json.dumps(formattedRecord)
            elif processFormat == 'xml':
                keyName = r.find_all('identifier')[0].get_text()
                record = unicode(r)

            print keyName

            try:
                self.processor.save2file(filePath, record)
                print "Record %d saved to file." % self.totalRecordCount
            except:
                pass

            try:
                connector(keyName, record)
            except:
                pass

    def updateParams(self):
        '''
        updates parameters with processor's current resumptionToken
        '''
        try:
            del self.params['metadataPrefix']
        except:
            pass

        try:
            self.params['resumptionToken'] = self.processor.resumptionToken
            self.query.setParameters(self.params)
        except:
            print 'the processor does not have resumptionToken'

    def updateRequest(self):
        self.query.setRequest()
        self.query.getResponse()

    def updateProcessor(self):
        self.processor = Processor(self.query.response,
                                   'xml', soupifyResponse=True)

if __name__ == '__main__':
    # setting baseUrl and initial parameters for harvesting OKR repo
    baseUrl = "https://openknowledge.worldbank.org/oai/request?"
    parameters = {
        'verb': 'ListRecords',
        'metadataPrefix': 'uketd_dc',
        }

    # initialize the flow controller
    control = FlowController(baseUrl, parameters)
    filePath = '../local_DS/flowTest6_keyNames.json'
    control.initFlow(control.harvest, filePath=filePath,
                     processFormat='json', limit=10)

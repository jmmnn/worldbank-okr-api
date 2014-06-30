# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Class for handling OKR open access API queries

For more information about the API go to:
https://openknowledge.worldbank.org/harvesting-the-okr
'''

import urllib2


class QueryContainer(object):

    def __init__(self, baseUrl, parameters=None, request=None, response=None):
        self.baseUrl = baseUrl
        self.parameters = None
        self.request = None
        self.response = None
        self.json = None

    def setParameters(self, parameters):
        '''
        set parameters for query
        args: dictionary of key (query field) and value
        '''
        #checks if parameters is a dict
        assert type(parameters) is dict, \
            'parameter is not a dictionary: %r' % parameters
        self.parameters = parameters

    def setRequest(self):
        '''
        create the request string for the query
        '''
        #checks if self.parameters are defined
        assert self.parameters, \
            'parameters for query are not set'
        paramString = '&'.join(['='.join(p) for p in self.parameters.items()])
        self.request = ''.join([self.baseUrl, paramString])

    def getResponse(self):
        '''
        get HTTP response for query request
        '''
        assert self.request, \
            'request string is not defined'
        self.response = urllib2.urlopen(self.request).read()

    def save2file(self, path, fileFormat):
        '''
        saves xml response to .format file
        '''
        with open('.'.join([path, fileFormat]), 'w') as textFile:
            textFile.write(self.response)


if __name__ == "__main__":
    baseUrl = "https://openknowledge.worldbank.org/oai/request?"
    queryOKR = QueryContainer(baseUrl)

    #setting query parameters for testing
    parameters = {
        'verb': 'ListRecords',
        'metadataPrefix': 'uketd_dc',
        }

    queryOKR.setParameters(parameters)
    queryOKR.setRequest()
    queryOKR.getResponse()
    print queryOKR.response
    #queryOKR.save2file('./sampleData/sampleResponse', 'xml')
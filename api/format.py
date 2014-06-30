# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Class for formatting jsonResponse API response from OKR to obtain
necessary metadata.

For more information about the API go to:
https://openknowledge.worldbank.org/harvesting-the-okr
'''

import re
import json


class Formatter(object):

    def __init__(self, record):
        self.record = dict(json.loads(record))
        self.sumitSchema = {
            'okrID': self.getId(),
            'uri': self.getUri(),
            'issueDate': self.getDate(),
            'pubtype': self.getPubType(),
            'title': self.getTitle(),
            'abstract': self.getAbstract(),
            'subjectTags': self.getSubjectTags(),
            'pdfUrl': self.getPdfLink(),
            'txtUrl': self.getTxtLink(),
            'thumbUrl': self.getThumbnail(),
            'licenseUrl': self.getLicense()
        }

    def formatRecord(self):
        return {key: self.sumitSchema[key] for key in self.sumitSchema}

    def getId(self):
        assert len(self.record['relation']) == 1,\
            "\'_id\' tag contains more than one relation"
        return self.record['_id'][0]

    def getUri(self):
        assert len(self.record['uri']) == 1,\
            "\'uri\' tag contains more than one relation"
        return self.record['uri'][0]

    def getDate(self):
        '''
        gets the first date in the list of dates in the record schema
        '''
        return self.record['dates'][0]

    def getPubType(self):
        assert len(self.record['relation']) == 1,\
            "\'relation\' tag contains more than one relation"
        return self.record['relation'][0]

    def getAbstract(self):
        description = self.record['description']
        assert len(description) == 1, "description has multiple elements"
        return self.cleanText(description[0])

    def getTitle(self):
        title = self.record['title']
        assert len(title) == 1, "title has multiple elements"
        return self.cleanText(title[0])

    def cleanText(self, text):
        '''
        A helper method for getAbstract and getTitle methods
        '''
        return re.sub('\r\n\s+', ' ', text)

    def getSubjectTags(self):
        return [tag.lower() for tag in self.record['subjectTags']]

    def getPdfLink(self):
        return self.findLink('.pdf/?', self.record['identifiers'])

    def getTxtLink(self):
        return self.findLink('.txt/?', self.record['identifiers'])

    def getThumbnail(self):
        return self.findLink('.jpg/?', self.record['identifiers'])

    def getLicense(self):
        return self.findLink('.license/?', self.record['identifiers'])

    def findLink(self, pattern, stringList):
        '''
        A helper method for finding links in the identifiers value
        '''
        for string in stringList:
            if re.search(pattern, string):
                return string

    def printRecord(self):
        for key, value in self.record.items():
            print key, value
            print '\n'

if __name__ == '__main__':

    with open('../local_DS/sampleResponse.json') as dataFile:
        lines = dataFile.readlines()

    formatter = Formatter(lines[2])
    '''
    #### Test getDescription method ####
    print formatter.getDescription()

    #### Test methods for finding specific identifiers ####
    print formatter.getPdfLink()
    print formatter.getTxtLink()
    print formatter.getThumbnail()
    print formatter.getLicense()
    '''

    print formatter.formatRecord()

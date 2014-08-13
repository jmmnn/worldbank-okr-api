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

    def formatRecord(self, record):
        self.record = record
        return {
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

    def getId(self):
        if len(self.record['okrID']) == 1:
            return self.record['okrID'][0]
        elif len(self.record['okrID']) > 1:
            print "'id' tag contains more than one id,\
                storing both id's for later verification"
            return self.record['okrID']

    def getUri(self):
        if len(self.record['uri']) == 1:
            return self.record['uri'][0]
        elif len(self.record['uri']) > 1:
            print "'uri' tag contains more than one uri,\
                storing both uri's for later verification"
            return self.record['uri']

    def getDate(self):
        '''
        gets the first date in the list of dates in the record schema
        '''
        return self.record['dates'][0]

    def getPubType(self):
        return self.record['relation']

    def getAbstract(self):
        try:
            description = self.record['description']
            return self.cleanText(description[0])
        except:
            print 'this record has no description'
            return 'n/a'

    def getTitle(self):
        title = self.record['title']
        if len(title) == 1:
            return self.cleanText(title[0])
        elif len(title) > 1:
            print "title has multiple elements"
            return [self.cleanText(t) for t in title]

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

    with open('../local_DS/sampleResponse.nrjson') as dataFile:
        lines = dataFile.readlines()

    formatter = Formatter()
    '''
    #### Test getDescription method ####
    print formatter.getDescription()

    #### Test methods for finding specific identifiers ####
    print formatter.getPdfLink()
    print formatter.getTxtLink()
    print formatter.getThumbnail()
    print formatter.getLicense()
    '''

    print formatter.formatRecord(lines[2])

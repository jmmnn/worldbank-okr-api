# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Script for syncing query responses to S3 datastore.
'''

from boto.s3.key import Key
from boto.s3.connection import S3Connection
from api.control_flow import FlowController


class S3Connector(object):

    def __init__(self, aws_access_key=None, aws_secret_key=None):

        if ((aws_access_key is not None) & (aws_secret_key is not None)):
            self.conn = S3Connection(aws_access_key, aws_secret_key)
        else:
            self.conn = S3Connection()

    def createBucket(self, name, loc=None):
        try:
            self.conn.create_bucket(name, loc)
        except:
            self.conn.create_bucket(name)

    def accessBucket(self, name, validate=True):
        self.bucket = self.conn.get_bucket(name, validate=validate)

    def storeContent(self, keyName, contents):
        assert self.bucket, 'bucket is not specified'
        k = Key(self.bucket)
        k.key = keyName
        k.set_contents_from_string(contents)

    def getContent(self, keyName):
        k = Key(self.bucket)
        k.key = keyName
        return k.get_contents_as_string()

    def deleteContent(self, keyName):
        k = Key(self.bucket)
        k.key = keyName
        self.bucket.delete_key(k)

if __name__ == "__main__":
    # setting baseUrl and initial parameters for harvesting OKR repo
    baseUrl = "https://openknowledge.worldbank.org/oai/request?"
    parameters = {
        'verb': 'ListRecords',
        'metadataPrefix': 'uketd_dc',
        }

    #creating connector to S3 server 'sumit_okr' bucket
    bc = S3Connector()
    bc.accessBucket('sumit_okr')

    '''
    #Script for saving 100 files to s3 bucket 'sumit_okr'

    #initializing flow controller
    control = FlowController(baseUrl, parameters)
    control.initFlow(control.harvest,
                     filePath=None,
                     connector=bc.storeContent,
                     processFormat='json',
                     limit=100)

    #Script for downloading all OKR metadata

    #initializing flow controller
    control = FlowController(baseUrl, parameters)
    control.initFlow(control.harvest,
                     filePath=None,
                     connector=bc.storeContent,
                     processFormat='json')

    '''

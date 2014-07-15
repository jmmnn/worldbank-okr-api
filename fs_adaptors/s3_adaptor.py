# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Class for handling queries and access to S3 datastore.
'''

from boto.s3.key import Key
from boto.s3.connection import S3Connection


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

        self.accessBucket(name)
        print 'created %s, now accessing' % name

    def accessBucket(self, name, validate=True):
        self.bucket = self.conn.get_bucket(name, validate=validate)

    def storeStringContent(self, keyName, contents):
        assert self.bucket, 'bucket is not specified'
        k = Key(self.bucket)
        k.key = keyName
        k.set_contents_from_string(contents)

    def getStringContent(self, keyName):
        k = Key(self.bucket)
        k.key = keyName
        return k.get_contents_as_string()

    def storeFilenameContent(self, keyName, fileName):
        assert self.bucket, 'bucket is not specified'
        k = Key(self.bucket)
        k.key = keyName
        k.set_contents_from_filename(fileName)

    def getFilenameContent(self, keyName, fileName):
        k = Key(self.bucket)
        k.key = keyName
        return k.get_contents_to_filename(fileName)

    def storeFileContent(self, keyName, fp):
        assert self.bucket, 'bucket is not specified'
        k = Key(self.bucket)
        k.key = keyName
        k.set_contents_from_file(fp)

    def getFileContent(self, keyName, fp):
        k = Key(self.bucket)
        k.key = keyName
        return k.get_contents_to_file(fp)

    def deleteContent(self, keyName):
        k = Key(self.bucket)
        k.key = keyName
        self.bucket.delete_key(k)

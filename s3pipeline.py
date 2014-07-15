# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

Script for syncing query responses to S3 datastore.
'''

from fs_adaptors.s3_adaptor import S3Connector

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
    count = 0
    for key in bc.bucket:
        print key
        count += 1
        if count > 10:
            break
    '''
    #Script for saving 100 files to s3 bucket 'sumit_okr'

    #initializing flow controller
    control = FlowController(baseUrl, parameters)
    control.initFlow(control.harvest,
                     filePath=None,
                     connector=bc.storeStringContent,
                     processFormat='json',
                     limit=100)

    #Script for downloading all OKR metadata

    #initializing flow controller
    control = FlowController(baseUrl, parameters)
    control.initFlow(control.harvest,
                     filePath=None,
                     connector=bc.storeStringContent,
                     processFormat='json')

    '''

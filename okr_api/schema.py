# -*- coding: utf-8 -*-
'''
------------------------------
Open Knowledge Repository: OKR
------------------------------

SUMIT-OKR Schema

This file defines a specific document-based schema
that overlays the processing and formatting pipeline.

For more information about the API go to:
https://openknowledge.worldbank.org/harvesting-the-okr

For more information about the OAI-PMH go to:
http://www.openarchives.org/OAI/openarchivesprotocol.html
'''

#base URL for making requests to the OKR API
okrBaseUrl = 'https://openknowledge.worldbank.org/oai/request?'

#Attribute names for dublin core metadata documents
dublinCore = [
    'xmlns:dc',
    'xmlns:dcterms',
    'xmlns:doc',
    'xmlns:uketd_dc',
    'xmlns:uketdterms',
    'xmlns:xsi',
    'schemalocation'
]

#Argument keys for requests
requestArgs = [
    'verb',
    'identifier',
    'from',
    'until',
    'resumptionToken',
    'metadataPrefix'
]

#Header schema for OKR records
schemaHeader = {
    'okrID': 'identifier',
    'setSpecs': 'setSpec'
}

#Metadata schema for OKR records
schemaMetadata = {
    'dates': 'date',
    'issued': 'issued',
    'uri': 'isReferencedBy',
    'abstract': 'abstract',
    'title': 'title',
    'creators': 'creator',
    'subjectTags': 'subject',
    'description': 'description',
    'identifiers': 'identifier',
    'relation': 'relation',
    'rights': 'rights',
    'publisher': 'publisher',
}

#Possible error codes returned for HTTP requests
errorCodes = [
    'badArgument',
    'badResumptionToken',
    'badVerb',
    'cannotDisseminateFormat',
    'idDoesNotExist',
    'noRecordsMatch',
    'noMetadataFormats',
    'noSetHierarchy'
]

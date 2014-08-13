from s3pipeline import S3Connector
import json
from pattern.web import URL

if __name__ == "__main__":
    okrMain = S3Connector()
    okrMain.accessBucket('sumit_okr')

    okrPdfBc = S3Connector()
    okrPdfBc.accessBucket('sumit_okr_pdf')

    for key in okrMain.bucket:
        if okrPdfBc.bucket.get_key(key):
            print 'key exists... skipping %s' % key
            continue
        else:
            print 'saving .pdf of %s' % key
            record = json.loads(okrMain.getStringContent(key))
            pdfUrl = record['pdfUrl']
            try:
                url = URL(pdfUrl)
                okrPdfBc.storeStringContent(key, url.download(cached=False))
            except:
                print '%s is not a valid URL' % pdfUrl
                okrPdfBc.storeStringContent(key, '<No pdf for this article>')

from s3pipeline import S3Connector


if __name__ == "__main__":
    okrPdfBc = S3Connector()
    okrPdfBc.accessBucket('sumit_okr_pdf')

    #generate public urls

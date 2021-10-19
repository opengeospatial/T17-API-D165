from requests_aws4auth import AWS4Auth
import boto3
import os

def getAWSAuth(awsConfig):
    region = awsConfig["region"]
    service = 'es' #elasticsearchservice
    
    if "profile" in awsConfig:
        session = boto3.session.Session(profile_name=awsConfig["profile"])
    else:
        session = boto3.session.Session()

    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service) 

    return awsauth
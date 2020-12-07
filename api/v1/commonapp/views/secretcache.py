import boto3
import base64
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from botocore.exceptions import ClientError
import json

class SecretManager():
    region_name="us-east-2"                  #store region name
    session=boto3.session.Session()          #creating session
    client=session.client(                   #Create a Secrets Manager client
        service_name="secretsmanager",  
        region_name=region_name
    )
    cache= SecretCache(SecretCacheConfig(),client)  #Create a cache

    def get_secret(self,secret_name):
        print("Inside SecretCache")            
        try:
            get_secret_value_response=self.cache.get_secret_string(secret_name)  #Get secret string from the cache

        except ClientError as e:
            print("inside except")
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                    # An error occurred on the server side.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                    # You provided an invalid value for a parameter.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                    # You provided a parameter value that is not valid for the current state of the resource.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                    # We can't find the resource that you asked for.
                raise e
        else:
            secret = get_secret_value_response
            secret=json.loads(secret)
            return secret[secret_name]

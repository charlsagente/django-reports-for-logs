__author__ = 'charls'
import os

import boto3


class DynamoBD:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name="us-east-1",
                                       aws_access_key_id=os.environ['AWSACCESSKEYID'],
                                       aws_secret_access_key=os.environ['AWSSECRETACCESSKEY'])

    def getTableCreationDate(self):
        table = self.dynamodb.Table('eventlogs')
        print(table.creation_date_time)

    def putItem(self,item):
        table = self.dynamodb.Table('eventlogs')
        table.put_item(
            Item=item
        )

    def getItem(self):
        table = self.dynamodb.Table('eventlogs')
        response = table.get_item(
            Key={
                'execution_date_time': 234443343434
            }
        )
        item = response['Item']
        print(item)

    def deleteItem(self):
        table = self.dynamodb.Table('eventlogs')
        table.delete_item(
            Key={
                'execution_date_time': 234443343434
            }
        )

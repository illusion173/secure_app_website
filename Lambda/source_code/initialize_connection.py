import json
import boto3
import botocore
import hashlib
import base64
import time
from boto3.dynamodb.conditions import Attr


def scan_db(table, scan_kwargs=None):
    """
    Get all records of the dynamodb table where the FilterExpression holds true
    :param scan_kwargs: Used to pass filter conditions
    :type scan_kwargs: dict
    :param table: dynamodb table name
    :type table: str
    :return: list of records
    :rtype: dict
    """
    if scan_kwargs is None:
        scan_kwargs = {}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)

    complete = False
    records = []
    while not complete:
        try:
            response = table.scan(**scan_kwargs)
        except botocore.exceptions.ClientError as error:
            raise Exception('Error quering DB: {}'.format(error))

        records.extend(response.get('Items', []))
        next_key = response.get('LastEvaluatedKey')
        scan_kwargs['ExclusiveStartKey'] = next_key

        complete = True if next_key is None else False
    return records
    
def lambda_handler(event, context):
   
    # load needed session data sent from user
    clear_session_id = event['clear_session_id']
    #Set New Status note that it says connected, NOT Authenticated!
    status = 'connected'
    #now we need to verify that the user's session id is valid & open
    kwargs = {
        'FilterExpression': Attr("session_status").eq("open"),
        'FilterExpression' : Attr("session_id").eq(clear_session_id)
    }
    
    final_records = scan_db("sessions_are_us", kwargs)
    #checks if session is open and does exist
    if len(final_records) == 0:
        return {
            'status' : 'dynamodb error'
        }
        
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

    table = dynamodb.Table('sessions_are_us')
    # add new expiration time increase by 8 hours
    expiration = int(time.time()) + 28800
    # update the item in session are us table 
    response = table.update_item(
        Key={
            'session_id': clear_session_id
        },
        UpdateExpression="set #session_connection=:r",
        ExpressionAttributeNames={
            '#session_connection': 'session_status'
        },
        ExpressionAttributeValues={
            ':r': "Connected"
           
        },
        ReturnValues="UPDATED_NEW"
    )

    response = table.update_item(
        Key={
            'session_id': clear_session_id
        },
        UpdateExpression="set #session_ttl=:r",
        ExpressionAttributeNames={
            '#session_ttl': 'ttl'
        },
        ExpressionAttributeValues={
            ':r': expiration
           
        },
        ReturnValues="UPDATED_NEW"
    )    
    
    # return no data to the user, if user gets a 200, successful initialization 
    return {
        'status' : 200
    }

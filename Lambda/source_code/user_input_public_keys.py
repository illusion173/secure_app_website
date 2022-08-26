import json
import boto3
'''
Allows a user to input their own public keys.

Input is via event:
    user_id,
    ecc_key_id,
    ecc_public_key,
    ttl <- time to live, should be INT
'''
def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    
    sessions_are_us_table = dynamodb.Table('keys_are_us')
    # put item into table
    try: 
        session_response = sessions_are_us_table.put_item(
        Item={
            'user_id' : event['user_id'],
            'ecc_key_id' : event['ecc_key_id'],
            'ecc_public_key' : event['ecc_public_key'],
            'ttl': event['ttl']
        }    
    )
    except:
        return {'error' : "DynamoDb input error"}    
    
    
   # return 200 if putting keys into database was successful.  
    return {
        'statusCode': 200
    }

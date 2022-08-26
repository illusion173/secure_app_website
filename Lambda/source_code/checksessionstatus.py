import json
import boto3


'''
Analyzes whether or not queried session id has a jwt token and is Authenticated.

If the session id is authenticated and has a token, return the token.

Called by the website.

rtype: string or int JSON


'''
def lambda_handler(event, context):
    
    clear_session_id = event['session_id_unsigned']
    
    client = boto3.client('dynamodb')

    response = client.get_item(
        TableName='sessions_are_us',
        Key={
        'session_id': {
            'S': clear_session_id,
            }
        },
        AttributesToGet=[
        'jwt_token',
        'session_status'
    ]
    )    
    
    if response['Item']['session_status']['S'] == "Authenticated":
        if 'jwt_token' in response['Item']:
            return {
                'jwt_token' : response['Item']['jwt_token']['S']
            }
        else: 
            return {
                'jwt_token' : 511
            }
    else:
        return{
            'jwt_token': 401
        }

import json
import boto3
from base64 import b64encode
import datetime
import time
import uuid
'''
void input
returns new data key pair

current key pairs outputted: RSA 4096, ECC P521.
KMS reccomends that a system use RSA for encryption, ECC for signatures.

Ensure that all data outputted is put in secrets manager.

'''

def lambda_handler(event, context):
    # master key data
    kms_client = boto3.client('kms', "us-west-2")
    alias_arn = "arn:aws:kms:us-west-2:006840835651:alias/user_app_master_key"
    alias_name = "alias/user_app_master_key"
    key_id = "mrk-2bf0b98efa5e45d286a8ef19bf87f60a"
    
    #request to create keys
    #RSA for encryption/decryption
    rsa_response = kms_client.generate_data_key_pair(
        KeyId=key_id,
        KeyPairSpec= 'RSA_4096',
    )
    
    #Request for ECC SIGNING
    ecc_response = kms_client.generate_data_key_pair(
        KeyId = key_id,
        KeyPairSpec = "ECC_NIST_P521"
    )
    
    '''
    response
    PrivateKeyCiphertextBlob
    PrivateKeyPlaintext
    PublicKey
    KeyId
    KeyPairSpec = RSA_4096 or ECC_NIST_P521
    ResponseMetadata
    '''

   #KEEP NOTE PRIVATE KEY IS ENCRYPTED!
    #Getting time stamp when keys are generated
    
    expiration = int(time.time()) + 10520000
    creation = int(time.time())
    
    now = datetime.datetime.now()
    expiring = datetime.datetime.now() + datetime.timedelta(days=120)
    date_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    date_time_expiring = expiring.strftime("%Y-%m-%dT%H:%M:%S")
    rsa_key_id_uuid = str(uuid.uuid1()) + ":" + rsa_response['KeyId']
    ecc_key_id_uuid = str(uuid.uuid1()) + ":" + ecc_response['KeyId']
   
    #Make sure to copy this outputted data into secrets manager as one big Json Document
    return {
        "human_date_time" : date_time,
        "human_date_time_expiring" : date_time_expiring,
        "system_date_time" : creation,
        "system_date_time_expiring" : expiration,
        "rsa_key_id" :  rsa_key_id_uuid,
        "rsa_private_key" : b64encode(rsa_response['PrivateKeyCiphertextBlob']).decode('utf-8'),
        "rsa_private_key_un" : b64encode(rsa_response['PrivateKeyPlaintext']).decode('utf-8'),
        "rsa_public_key" : b64encode(rsa_response['PublicKey']).decode('utf-8'),
        "ecc_key_id" : ecc_key_id_uuid,
        "ecc_private_key" : b64encode(ecc_response['PrivateKeyCiphertextBlob']).decode('utf-8'),
        "ecc_private_key_un" : b64encode(ecc_response['PrivateKeyPlaintext']).decode('utf-8'),
        "ecc_public_key" : b64encode(ecc_response['PublicKey']).decode('utf-8')
    }

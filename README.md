# Secure App & Password-less Logging in via QR code Scanning

### Authors: Fabian Da Silva, Tanner Bacon, Jeremiah Webb

## <ins>Description</ins>
The functionality of this project is to implement password-less logging in to a website via scanning a QR code. By using asymmetric key handshakes (ECC P521 & RSA 4096) one can verify themselves between a mobile application and a website client's backend. The website or client receiving the token can then proceed to make API calls using the JWT.

## <ins>Requirements</ins>
- latest npm installed
- aws account
- Cognito User Pool configured for custom authentication
- A confirmed user in user pool. In a user group named 'Managers'.

## <ins>Initial Setup</ins>
- Download repository
- Import database_cf_template.json into CloudFormation to generate two DynamoDB tables. Ensure on both that ttl is enabled.
- Import all Lambda functions either via SAM or the provided zip files
- NOTE: for system_receive_session_id & generate_sign_session_id Lambda functions, both must have the cryptography layer to function.
- Import AppSync API & API gateway. 
- For GraphQL AppSync API ensure API key is allowed and Amazon Cognito User Pool is allowed.
- For API gateway ensure ONLY checkadminstatus resource is Authorization: COGNITO_USER_POOLS 
- Generate system keys via KMS, First generate symmetric master key, then using create_key_pairs_app Lambda function to create the actual keys. Proceed to input the outputted JSON to a secret named "system_keys". 
<br>

### <ins>Website Setup</ins>
- Navigate to src folder of website.
- Edit app.js & aws-exports.js to your API endpoint arn, api-keys & user pool.
- Do the following commands:
- <code>npm install</code>
- <code>npm run build</code>
- <code>npm start</code>
- This will generate a localhost client, click Sign in Via QR Code First, scan with mobile application then click check JWT status.
- Check console in browser to see confirmation that JWT worked

### <ins>Known Issues</ins>
Please note that in some lambda functions & in src/app.js there are hard coded ARNs and IDs. Ensure to update them with your specific codes.

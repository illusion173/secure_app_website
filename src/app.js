import { Amplify, API, graphqlOperation } from "aws-amplify";

import awsconfig from "./aws-exports";
import * as queries from "./graphql/queries";
Amplify.configure(awsconfig);

// function to get a session id, signed and unencrypted
async function getSessionID(){
   return await API.graphql(graphqlOperation(queries.getSignedSessionID));
}

async function checkMyStatus(session_id_unsigned){
   return await API.graphql(graphqlOperation(queries.checkSessionStatus, {'session_id_unsigned' : session_id_unsigned}))
}


async function adminCheck(jwt_token){

      const newAppConfig = {
     API: {
       endpoints: [
         {
           name: "secure_app_api",
           endpoint: "https://774cf5appa.execute-api.us-west-2.amazonaws.com/beta11",
           custom_header: async () => { 
             return {
                'Authorization' : 'Bearer ' + jwt_token,
                'Authentication' : 'Bearer ' + jwt_token
             } 
           }
         }
       ]
     }
   }

   Amplify.configure(newAppConfig);

   
   const apiName = 'secure_app_api';
    const path = '/check_admin';
    const myInit = { 
      headers: { 
         'Authorization' : 'Bearer ' + jwt_token,
         'Authentication' : 'Bearer ' + jwt_token
      },
    };
    return await API.post(apiName, path, myInit);

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

document.getElementById("MutationEventButton").addEventListener('click', () => {
   getSessionID().then(res => {

      let session_data_json_string = JSON.stringify(res.data.getSignedSessionID)
      // We need the unsigned string 
      let session_id_unsigned = res.data.getSignedSessionID.clear_session_id

      console.log("Creating QR code")

      var qrcode = new QRCode(document.getElementById("qrcode-2"), {
      	text: session_data_json_string,
      	width: 150,
      	height: 150,
      	colorDark : "#000000",
      	colorLight : "#ffffff",
      	correctLevel : QRCode.CorrectLevel.H
      });

     document.getElementById("checkAdminStatusButton").addEventListener('click',() =>{
        console.log('Checking status')
      checkMyStatus(session_id_unsigned).then(newres=>{
         let jwt_token = newres.data.checkSessionStatus.jwt_token
         console.log(jwt_token)
         console.log('Checking if user is in manager group')
         adminCheck(jwt_token).then(newRes=>{
           console.log(newRes.managerConfirmation)

            });
         }); 
      });
   });
});




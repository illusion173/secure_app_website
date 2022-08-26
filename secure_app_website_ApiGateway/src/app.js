import { Amplify, API, graphqlOperation } from "aws-amplify";

import awsconfig from "./aws-exports";
Amplify.configure(awsconfig);

Amplify.configure({
  API: {
    endpoints: [
      {
        name: "secure_app_api",
        endpoint: "https://774cf5appa.execute-api.us-west-2.amazonaws.com/beta11",
        custom_header: async () => { 
          return {
               'x-api-key' : '#',
             'Authorization' : 'Bearer #',
               'Authentication' : 'Bearer #'} 
        }
      }
    ]
  }
});


async function getSessionID(){
   const apiName = 'secure_app_api';
   const path = '/getsignedsessionstatus'; 


   return await API.get(apiName, path)
 }

async function checkMyStatus(session_id_unsigned){
   const apiName = 'secure_app_api'
   const path = '/checksessionstatusgetjwt'
   const myInit = {
      body: {
         'session_id_unsigned' : session_id_unsigned
      }
   }
    
   return await API.post(apiName, path, myInit)
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


document.getElementById("MutationEventButton").addEventListener('click', () =>{
  getSessionID().then(res => {

      let session_data_json_string = JSON.stringify(res)
      console.log(res.signed_session_id)
      console.log(res.clear_session_id)
      let clear_session_id = res.clear_session_id
      let signed_session_id = res.signed_session_id
      var qrcode = new QRCode(document.getElementById("qrcode-2"), {
      	text: session_data_json_string,
      	width: 150,
      	height: 150,
      	colorDark : "#000000",
      	colorLight : "#ffffff",
      	correctLevel : QRCode.CorrectLevel.H
      });

      document.getElementById("checkAdminStatusButton").addEventListener('click', ()=>{
         console.log("checking jwt status")
         checkMyStatus(clear_session_id).then(newitem =>{
            let jwt_token = newitem.jwt_token
            console.log(jwt_token)
               adminCheck(jwt_token).then(newadmin => {
                  console.log(newadmin)
            if(newadmin.managerConfirmation){
               document.getElementById("confirmation").innerHTML = newadmin.managerConfirmation

            }
               })
         })
      })
  }) 
});

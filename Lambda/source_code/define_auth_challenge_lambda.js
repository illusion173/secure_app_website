// This is triggered when we try to do admin initiate auth when receiving the secret string
// This ensures we get the JWT token.
// And since we are doing our own custom verification of a user, checking again is redundant.
exports.handler = async (event) => {
  // Don't do any checks just say that authentication is successfull
  event.response.issueTokens = true;
  event.response.failAuthentication = false;
  return event;
};

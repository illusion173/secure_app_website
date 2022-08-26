/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getSignedSessionID = /* GraphQL */ `
  query GetSignedSessionID {
    getSignedSessionID {
      signed_session_id
      clear_session_id
    }
  }
`;
export const checkSessionStatus = /* GraphQL */ `
  query CheckSessionStatus($session_id_unsigned: String!) {
    checkSessionStatus(session_id_unsigned: $session_id_unsigned) {
      jwt_token
    }
  }
`;
export const adminCheck = /* GraphQL */ `
  query AdminCheck {
    adminCheck {
      managerConfirmation
    }
  }
`;

$(document).ready(function () {

    // https://developers.google.com/identity/openid-connect/openid-connect#obtainuserinfo
    let info = parseJwt(data.id_token)

    $("#user_email").html("Hi! " + info.email);
    sessionStorage.setItem('user_email', info.email)
    $("#user_email_nav").html(sessionStorage.getItem('user_email'));

})


const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };
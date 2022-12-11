
$(document).ready(function () {

    // // https://developers.google.com/identity/openid-connect/openid-connect#obtainuserinfo
    // let info = parseJwt(data.id_token)
    // console.log(data)
    // console.log(info)
    // $("#user_email").html("Hi! " + info.email);
    // sessionStorage.setItem('user_email', info.email)
    // $("#user_email_nav").html(sessionStorage.getItem('user_email'));

    const form  = document.getElementById('search_form_welcome');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var keyword = form.elements['search_keyword'].value

        console.log(keyword)

        $.ajax({
            type: "POST",
            url: "../search",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(keyword),
            success: function () {
                console.log("submitted")
                window.location.href = `../search_page/` + keyword
            },
            error: function(jq,status,message) {
                alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
            }
        });

    });
})


const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };
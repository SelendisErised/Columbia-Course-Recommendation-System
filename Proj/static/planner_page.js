
$(document).ready(function () {

    const form  = document.getElementById('search_form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var keyword = form.elements['search_keyword'].value

        console.log(keyword)

        window.location.href = `../planner_page/` + keyword
        // $.ajax({
        //     type: "POST",
        //     url: "../search",
        //     contentType: "application/json; charset=utf-8",
        //     data: JSON.stringify(keyword),
        //     success: function () {
        //         console.log("submitted")
        //         window.location.href = `../planner_page/` + keyword
        //     },
        //     error: function(jq,status,message) {
        //         alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
        //     }
        // });
    });

    const res  = document.getElementById('search_res');
    console.log(data)
    $('#search_res').append(
        `
        <div>
        ${data} result
        </div>
        `
    )
    $.each(data, function(index, value) {
        let new_row = display_log(value);
        $("#log_list").append(new_row);
    });
})
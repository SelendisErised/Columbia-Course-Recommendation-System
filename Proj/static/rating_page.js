
$(document).ready(function () {
    $("#user_email_nav").html(sessionStorage.getItem('user_email'));
    $('#search_res').append(
        `
        <div>
        ${data}
        </div>
        `
    )

    display_search_res();
})

function submitRatings() {
    var evaluation = [];
    for (let i = 1; i < 5; i++) {
        var form = document.getElementById('rating_' + i.toString());
        form.submit();
        var rating = 0;
        for (let j = 1; j < 6; j++) {
            if (form.elements['star-' + j.toString() + '-' + i.toString()].checked === true) {
                rating = j;
            }
        }
        evaluation.push(rating);
    }
    console.log(evaluation);
    return evaluation;
}

function display_search_res() {
    $("#search_res").empty();

    $.each(data, function(index, value) {
        var course_name = $("<h3></h3>");
        course_name.addClass("row pt-2");
        var name = $("<h3></h3>");
        name.addClass("col");
        name.html(value.Course);
        course_name.append(name);
        $("#search_res").append(course_name);

        var number_and_instructor = $("<h3></h3>");
        number_and_instructor.addClass("row pt-2");

        var number = $("<h3></h3>");
        number.addClass("col-md-3");
        number.html(value.Number);
        number_and_instructor.append(number);

        var instructor = $("<h3></h3>");
        instructor.addClass("col-md-4");
        instructor.html(value.Instructor);
        number_and_instructor.append(instructor);
        $("#search_res").append(number_and_instructor);

        console.log(value)
    });
}

function rating() {
    var search_key = '';
    $.each(data, function (index, value) {
        search_key = value.Number + '&' + value.Instructor + '&' + value.Course;
    });
    let evaluation = submitRatings();

    console.log(search_key);
    console.log(evaluation);
    const json_arg = {
        "search_key": search_key,
        "evaluation": evaluation
    }

    $.ajax({
            type: "POST",
            url: "../rating",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(json_arg),
            // complete: function () {
            //     window.location.href = '../evaluation_page/' + search_key;
            // },
            success: function () {
                        location.reload();
                    },
            error: function(jq,status,message) {
                alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
            }
        });
}
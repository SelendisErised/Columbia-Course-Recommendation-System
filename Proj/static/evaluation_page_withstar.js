
$(document).ready(function () {
    $("#user_email_nav").html(sessionStorage.getItem('user_email'));
    const search_res  = document.getElementById('search_res');
    
    $('#search_res').append(
        `
        <div>
        ${data}
        </div>
        `
    )

    // const form  = document.getElementById('search_form');
    // form.addEventListener('submit', (event) => {
    //     event.preventDefault();
    //     var keyword = form.elements['search_keyword'].value
    //
    //     console.log(keyword)
    //
    //     window.location.href = `../evaluation_page/` + keyword
    //     // $.ajax({
    //     //     type: "POST",
    //     //     url: "../search",
    //     //     contentType: "application/json; charset=utf-8",
    //     //     data: JSON.stringify(keyword),
    //     //     success: function () {
    //     //         console.log("submitted")
    //     //         window.location.href = `../search_page/` + keyword
    //     //     },
    //     //     error: function(jq,status,message) {
    //     //         alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
    //     //     }
    //     // });
    // });


    // $('#search_res').append(
    //     `
    //     <div>
    //     ${data} result
    //     </div>
    //     `
    // )
    // $.each(data, function(index, value) {
    //     let new_row = display_log(value);
    //     $("#log_list").append(new_row);
    // });

    display_search_res();
})

function show_star(grade){
    var star = 0, half = 0, no_star = 0;
    grade = parseFloat(grade);

    star = parseInt(grade)
    if (grade - star > 0.5) half = 1;
    no_star = 5 - star - half;

    var path = '../static/images',
        star_img = path + '/star-on.png',
        half_img = path + '/star-half.png',
        no_star_img = path + '/star-off.png',
        html = '';

    for(var i=0; i< star; i++){
            html += '<img src="' + star_img + '"/>';
            html += ' '
        }
    if (half == 1){
            html += '<img src="' + half_img + '"/>';
            html += ' '
        }
    for(var j=0; j < no_star; j++){
            html += '<img src="' + no_star_img + '"/>';
            html += ' '
        }
    return html;
}

function display_search_res() {
    $("#search_res").empty();

    $.each(data, function(index, value) {
        var course_name = $("<h1></h1>");
        course_name.addClass("row pt-2");
        var name = $("<h1></h1>");
        name.addClass("col");
        name.html(value.Course);
        course_name.append(name);
        $("#search_res").append(course_name);

        var number_and_instructor = $("<h2></h2>");
        number_and_instructor.addClass("row pt-2");

        var number = $("<h2></h2>");
        number.addClass("col-md-3");
        number.html(value.Number);
        number_and_instructor.append(number);

        var instructor = $("<h2></h2>");
        instructor.addClass("col-md-4");
        instructor.html(value.Instructor);
        number_and_instructor.append(instructor);
        $("#search_res").append(number_and_instructor);

        var workload = $("<h4></h4>");
        workload.addClass("row pt-4");

        var workload_title = $("<h4 style=\"font-weight: normal\">Workload</h4>");
        workload_title.addClass("col-md-4");
        workload.append(workload_title);

        var workload_star = $("<h4></h4>");
        workload_star.addClass("col-md-3");
        workload_star.html(show_star(value.Workload));
        workload.append(workload_star);
        $("#search_res").append(workload);

        var accessibility = $("<h4></h4>");
        accessibility.addClass("row pt-4");

        var accessibility_title = $("<h4 style=\"font-weight: normal\">Accessibility</h4>");
        accessibility_title.addClass("col-md-4");
        accessibility.append(accessibility_title);

        var accessibility_star = $("<h4></h4>");
        accessibility_star.addClass("col-md-3");
        accessibility_star.html(show_star(value.Accessibility));
        accessibility.append(accessibility_star);
        $("#search_res").append(accessibility);

        var delivery = $("<h4></h4>");
        delivery.addClass("row pt-4");

        var delivery_title = $("<h4 style=\"font-weight: normal\">Delivery</h4>");
        delivery_title.addClass("col-md-4");
        delivery.append(delivery_title);

        var delivery_star = $("<h4></h4>");
        delivery_star.addClass("col-md-3");
        delivery_star.html(show_star(value.Delivery));
        delivery.append(delivery_star);
        $("#search_res").append(delivery);

        var difficulty = $("<h4></h4>");
        difficulty.addClass("row pt-4");

        var difficulty_title = $("<h4 style=\"font-weight: normal\">Difficulty</h4>");
        difficulty_title.addClass("col-md-4");
        difficulty.append(difficulty_title);

        var difficulty_star = $("<h4></h4>");
        difficulty_star.addClass("col-md-3");
        difficulty_star.html(show_star(value.Difficulty));
        difficulty.append(difficulty_star);
        $("#search_res").append(difficulty);

        console.log(value)
    });
}
function redirect_rating(id, instructor, name) {
    window.location.href = `../rating_page/` + id + '&' + instructor + '&' + name
}

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

    var stars = $("<div class='stars'></div>");

    for(var j=0; j < no_star; j++){
            stars.append($("<div class='star-o'></div>"))
        }
    if (half == 1){
            stars.append($("<div class='star-half-o'></div>"));
        }
    for(var i=0; i< star; i++){
            stars.append($("<div class='star'></div>"));
        }
    return stars;
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

        var workload = $("<div class='rt-container'></div>");
        workload.addClass("row");

        var workload_title = $("<h4 style='font-weight: normal'>Workload</h4>");
        workload_title.addClass("col-md-5");
        workload.append(workload_title);

        var workload_star = show_star(value.Workload);
        workload.append(workload_star);
        $("#search_res").append(workload);

        var accessibility = $("<div class='rt-container'></div>");
        accessibility.addClass("row");

        var accessibility_title = $("<h4 style='font-weight: normal'>Accessibility</h4>");
        accessibility_title.addClass("col-md-5");
        accessibility.append(accessibility_title);

        var accessibility_star = show_star(value.Accessibility);
        accessibility.append(accessibility_star);
        $("#search_res").append(accessibility);

        var delivery = $("<div class='rt-container'></div>");
        delivery.addClass("row");

        var delivery_title = $("<h4 style='font-weight: normal'>Delivery</h4>");
        delivery_title.addClass("col-md-5");
        delivery.append(delivery_title);

        var delivery_star = show_star(value.Delivery);
        delivery.append(delivery_star);
        $("#search_res").append(delivery);

        var difficulty = $("<div class='rt-container'></div>");
        difficulty.addClass("row");

        var difficulty_title = $("<h4 style='font-weight: normal'>Difficulty</h4>");
        difficulty_title.addClass("col-md-5");
        difficulty.append(difficulty_title);

        var difficulty_star = show_star(value.Difficulty);
        difficulty.append(difficulty_star);
        $("#search_res").append(difficulty);

        let new_load_btn = $("<button></button>");
        new_load_btn.addClass("col-md-1 btn evaluation_btn ml-5");
        let new_id = value.Number;
        let new_instructor = value.Instructor;
        let new_course_name = value.Course;
        new_load_btn.attr('id', new_id);
        new_load_btn.attr('instructor', new_instructor)
        new_load_btn.attr('course_name', new_course_name);
        console.log(new_id);
        console.log(instructor);
        console.log(course_name);
        new_load_btn.html("Rating");
        $("#search_res").append(new_load_btn);

        console.log(value);
    });

    $(".evaluation_btn").click(function() {
        console.log("eval btn clicked")
        redirect_rating($(this).attr("id"), $(this).attr("instructor"), $(this).attr("course_name"));
    });
}
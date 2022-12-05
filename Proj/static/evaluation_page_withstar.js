
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

    const form  = document.getElementById('search_form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var keyword = form.elements['search_keyword'].value

        console.log(keyword)

        window.location.href = `../evaluation_page/` + keyword
        // $.ajax({
        //     type: "POST",
        //     url: "../search",
        //     contentType: "application/json; charset=utf-8",
        //     data: JSON.stringify(keyword),
        //     success: function () {
        //         console.log("submitted")
        //         window.location.href = `../search_page/` + keyword
        //     },
        //     error: function(jq,status,message) {
        //         alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
        //     }
        // });
    });


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


function display_search_res() {
    $("#search_res").empty();

    $.each(data, function(index, value) {
        let new_row = display_each_course(value);
        $("#search_res").append(new_row);
        console.log(value)
    });

    // //delete button function
    // $(".delete_btn").click(function() {
    
    //     delete_sale($(this).attr("id"));
    //     display_sales_list();

    // });
    // console.log(sales)
}

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
        }
    if (half == 1){
            html += '<img src="' + half_img + '"/>';
        }
    for(var j=0; j < no_star; j++){
            html += '<img src="' + no_star_img + '"/>';
        }
    return html;
}

function display_each_course(course) {
    var new_row = $("<div></div>");
    new_row.addClass("row pt-2");

    //div for Course
    var new_Course = $("<div></div>");
    new_Course.addClass("col-md-2");
    new_Course.html(course.Course);
    new_row.append(new_Course);

    //div for Instructor
    var new_instructor = $("<div></div>");
    new_instructor.addClass("col-md-2");
    new_instructor.html(course.Instructor);
    new_row.append(new_instructor);

    //div for Workload
    var new_workload = $("<div></div>");
    new_workload.addClass("col-md-2");
    new_workload.html(show_star(course.Workload));
    new_row.append(new_workload);

    //div for Accessibility
    var new_accessibility = $("<div></div>");
    new_accessibility.addClass("col-md-2");
    new_accessibility.html(show_star(course.Accessibility));
    new_row.append(new_accessibility);

    //div for Delivery
    var new_delivery = $("<div></div>");
    new_delivery.addClass("col-md-2");
    new_delivery.html(show_star(course.Delivery));
    new_row.append(new_delivery);

    //div for Difficulty
    var new_difficulty = $("<div></div>");
    new_difficulty.addClass("col-md-1.5");
    new_difficulty.html(show_star(course.Difficulty));
    new_row.append(new_difficulty);


    // var delete_button = $("<button></button>");
    // delete_button.addClass("col-md-1 btn delete_btn");
    // delete_button.prop("id", log.id);
    // console.log("button id(real index): "+ log.id);
    // delete_button.html("X");
    // new_row.append(delete_button);

    return new_row;
}
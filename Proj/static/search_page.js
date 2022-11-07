
$(document).ready(function () {
<<<<<<< HEAD
    const res  = document.getElementById('search_res');
    
    $('#search_res').append(
        `
        <div>
        ${data}
        </div>
        `
    )
=======
>>>>>>> my-backup

    const form  = document.getElementById('search_form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var keyword = form.elements['search_keyword'].value

        console.log(keyword)

        window.location.href = `../search_page/` + keyword
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

    const res  = document.getElementById('search_res');
    console.log(data[0])
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

function display_each_course(course) {
    var new_row = $("<div></div>");
    new_row.addClass("row pt-2");
    
    //div for Course number and name
    var new_num_and_course = $("<div></div>");
    new_num_and_course.addClass("col-md-4");

    var new_course_number = $("<div></div>");
    new_course_number.addClass("row");
    new_course_number.html(course.Number);
    new_num_and_course.append(new_course_number);

    var new_course_name = $("<div></div>");
    new_course_name.addClass("row");
    new_course_name.html(course.Course);
    new_num_and_course.append(new_course_name);
    new_row.append(new_num_and_course);

    //div for loc & time
    var new_loc_and_time = $("<div></div>");
    new_loc_and_time.addClass("col-md-3");
    
    var new_location = $("<div></div>");
    new_location.addClass("row");
    new_location.html(course.Location);
    new_loc_and_time.append(new_location);

    var new_time = $("<div></div>");
    new_time.addClass("row");
    new_time.html(course.Time);
    new_loc_and_time.append(new_time);
    new_row.append(new_loc_and_time);

    //div for instructor
    var new_instructor = $("<div></div>");
    new_instructor.addClass("col-md-2");
    new_instructor.html(course.Instructor);
    new_row.append(new_instructor);


    // var delete_button = $("<button></button>");
    // delete_button.addClass("col-md-1 btn delete_btn");
    // delete_button.prop("id", log.id);
    // console.log("button id(real index): "+ log.id);
    // delete_button.html("X");
    // new_row.append(delete_button);

    return new_row;
}
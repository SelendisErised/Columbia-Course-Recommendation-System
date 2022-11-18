
$(document).ready(function () {
    $("#user_email_nav").html(sessionStorage.getItem('user_email'));

    const form  = document.getElementById('search_form');
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var keyword = form.elements['search_keyword'].value

        console.log("search_keyword: " + keyword)

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

    // const res  = document.getElementById('search_res');
    // console.log(data)
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
    // $("#wish_list").empty();
    // $('#wish_list').append(
    //     `
    //     <div>
    //     ${wish_list}
    //     </div>
    //     `
    // )

    display_wish_list();
    display_search_res();
})

function display_search_res() {
    $("#search_res").empty();
    console.log(data)
    $.each(data, function(index, value) {
        // console.log(value)
        let new_row = display_each_course(value);

        let add_course_button = $("<button></button>");
        add_course_button.addClass("col-md-1 btn add_course_btn");
        add_course_button.prop("id", value.Number);
        // console.log("button id(course.Number): "+ course.Number);
        add_course_button.html("Add");
        new_row.append(add_course_button);

        $("#search_res").append(new_row);
    });

    //add_course button function
    $(".add_course_btn").click(function() {
    
        add_course($(this).attr("id"));
        // console.log("button id(course.Number): "+ $(this).attr("id"));
        // display_search_res();
    });
}

function display_wish_list() {
    console.log(wish_list)
    $("#wish_list").empty();

    $.each(wish_list, function(index, value) {
        
        // let new_row = display_each_course(value);
        let new_row = $(`<div>${value}</div>`);

        let add_course_button = $("<button></button>");
        add_course_button.addClass("col-md-1 btn remove_course_btn");
        // add_course_button.prop("id", value.Number);
        add_course_button.prop("id", value);
        add_course_button.html("Remove");
        new_row.append(add_course_button);

        $("#wish_list").append(new_row);
        
    });

    //remove_course button function
    $(".remove_course_btn").click(function() {
    
        remove_course($(this).attr("id"));
        console.log("remove: button id(course.Number): "+ $(this).attr("id"));

    });
}


function add_course(id) {
    console.log(id);
    $.ajax({
            type: "POST",
            url: "../add_course",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(id),
            success: function () {
                        location.reload();
                        // this segment is for future working of refresh wish list and search result without refresh whole page
                        const segments = new URL(window.location.href).pathname.split('/');
                        const last = segments.pop() || segments.pop(); // Handle potential trailing slash
                        console.log(last);
                    },
            error: function(jq,status,message) {
                alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
            }
        });
}

function remove_course(id) {
    console.log(id);
    $.ajax({
            type: "POST",
            url: "../remove_course",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(id),
            success: function () {
                        location.reload();
                    },
            error: function(jq,status,message) {
                alert('A jQuery error has occurred. Status: ' + status + ' - Message: ' + message);
            }
        });
}

function display_each_course(course) {
    let new_row = $("<div></div>");
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

    //div for tag
    var new_tag = $("<div></div>");
    new_tag.addClass("col-md-1");
    new_tag.html(course.Tag);
    new_row.append(new_tag);




    return new_row;
}
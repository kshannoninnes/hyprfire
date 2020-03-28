function get_file_details(selected_file_name){
    // Make http request to django server for details of selected_file_name
    // Use said details to update HTML img_element src

    $.get({
        url: `${selected_file_name}/`
    })
}

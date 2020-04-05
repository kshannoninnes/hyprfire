function load_graph(filename){
    // Perform a get request to http://127.0.0.1:8000/<filename>/ which will respond with HTML/JavaScript data
    // for loading the graph relevant to the specified file
    $.get({
        url: `${filename}/`,
        success: function (response) {
            $('#svg_container').html(response)
        }
    });
}

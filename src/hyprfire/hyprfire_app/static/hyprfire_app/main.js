// Default selected item will be the first file in the list
let selected = $( "#file_list li:nth-child(2)" ).text();

function load_graph(filename){
    // Perform a get request to http://127.0.0.1:8000/<filename>/ which will respond with HTML/JavaScript data
    // for loading the graph relevant to the specified file
    $.get({
        url: `${filename}/`,
        success: function (response) {
            $('#right_container').html(response)
        }
    });
}

function set_selected(filename){
    selected = filename;
}

function analyse(){
    console.log(`Selected file is '${selected}'`);
}
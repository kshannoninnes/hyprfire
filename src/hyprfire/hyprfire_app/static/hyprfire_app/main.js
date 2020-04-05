function load_graph(filename){
    $.get({
        url: `${filename}/`,
        success: function (response) {
            let imported = document.importNode(response.documentElement, true);

            // Ensure the image is centered within the container html tag
            imported.setAttribute("width", "100%");
            imported.setAttribute("height", "100%");
            imported.setAttribute('style', 'position:absolute; top:(calc 50% - 24px); left:(50% - 24px);');

            $('#svg_container').html(imported);
        }
    });
}

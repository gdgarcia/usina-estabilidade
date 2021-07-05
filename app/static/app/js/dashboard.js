/* globals Chart:false, feather:false */

function carrega_blocos_ajax () {
    // get the url of the `load_blocos` view
    var url = $("#plotForm").attr("usina-blocos-url");
    // get the selected country ID from the HTML input
    var usinaId = $(this).val();

    // initialize an AJAX request
    $.ajax({
        // set the url of the request (= localhost:8000/hr/ajax/load-cities)
        url: url,
        data: {
            // add the country id to the GET parameters
            'usina': usinaId
        },
        // `data` is the return of the `load_cities` view function
        success: function (data) {
            // replace the contents of the city input with data that came from 
            // the server
            $("#id_bloco").html(data);
        }
    });
}

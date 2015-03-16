$(document).ready(function(){
    $('#searchanimebutton').bind('click', function(event) {
        event.preventDefault();
        console.log("hi");
        $.ajax({
            type: "POST",
            url: "addanime",
            data: $('#animesearchform').serialize(),
            success: function(returnData) {
                $('#addanimeform').empty();
                $('#searchformpage').replaceWith(returnData);
                },
            return: function(failData) {
                console.log(failData);
                }
        });
    });

    $('#animesearchbutton').bind('click', function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "addanime",
            data: $('#addanimeform').serialize(),
            success: function(returnData) {
                //$('#searchformpage').replaceWith(returnData);
                console.log("success");
                },
            return: function(failData) {
                console.log(failData);
                }
        });
        $.ajax({
            type: "POST",
            url: "addanime",
            data: $('#animesearchform').serialize(),
            success: function(returnData) {
                console.log("second")
                $('#addanimeform').empty();
                $('#searchformpage').replaceWith(returnData);
                var element = document.getElementById("addanimeform");
                element.scrollIntoView({block: "start", behavior: "smooth"});
                },
            return: function(failData) {
                console.log(failData);
                }
        });

    });
});
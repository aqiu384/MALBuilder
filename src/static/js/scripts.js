$(document).ready(function(){
    $('#searchanimebutton').bind('click', function(event) {
        event.preventDefault();
        console.log("hi");
        $.ajax({
            type: "POST",
            url: "addanime",
            data: $('#animesearchform').serialize(),
            success: function(returnData) {
                $('#searchformpage').replaceWith(returnData);
                },
            return: function(failData) {
                console.log(failData);
                }
        });
});
$(document).ready(function(){
    $('#addanimebutton').bind('click', function(event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "addanime",
            data: $('#addanimeform').serialize(),
            success: function(returnData) {
                //$('#searchformpage').replaceWith(returnData);
                $('addanimeform').replaceWith(returnData)
                console.log("success");
                },
            return: function(failData) {
                console.log(failData);
                }
        });

    });
});
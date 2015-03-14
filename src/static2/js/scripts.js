
$(document).ready(function(){
    $('#sidebar').affix({
      offset: {
        top: 240
      }
    });
    $('#searchanimebutton').bind('click', function() {
        alert("hi");
    }
});

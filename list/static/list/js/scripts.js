document.addEventListener('DOMContentLoaded', function() {


    $('#delete').click(function(e){

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        e.preventDefault();
        var id_number = $(this).data('id');
        // alert(id_number);
        $.ajax({
            method : 'DELETE',
            url : `${id_number}`,
            data: 'identifer='+id_number,
            success: function(data){
                if(data) {alert("Success!")
                location.href = "/"}

            },
            error: function(err){
                console.log(err)
            }
        });
    });

    $('#filter').click(function(){

        var dueDate = $('#dueDate').val();
        console.log(dueDate);
        location.href = `/?dueDate=${dueDate}`


    });

});




function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


function deleteList(e){
    


}
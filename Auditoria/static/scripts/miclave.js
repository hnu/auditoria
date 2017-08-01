
function sendData()
{
    $.ajax(
        {
            url: '/change_my_pass',
            data:{
                password: $('#password').val(),
            },
            type: 'POST',
            success:function(response)
            {
                if(response=='1')
                {
                    window.location.replace('/')
                }
            }
        }
      )
}


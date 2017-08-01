$('#message').hide()

function sendData()
{
    $.ajax(// '/process_login',
        {
            url: '/process_login',
            data:{
                user: $('#user').val(),
                password: $('#password').val(),
            },
            type: 'POST',
            success:function(response)
            {
                if(response=='1')
                {
                    window.location.replace('/')
                }
                else if (response=='0') {
                    $('#message').show()
                    setMessage('Credenciales invalidas')
                }
                else
                {
                    $('#message').show()
                    setMessage(response)
                }
            }
        }
      )
}

function setMessage(msg)
{
    $('#message').empty().append('<span><strong>' + msg + '</strong></span>')
}
$('#message').hide()

function sendData() {

    if ($('#mv').val() != '')
    {
    $.ajax(
        {
            url: '/process_asignacion',
            data: {
                auditor: $('#auditor').val(),
                estacion: $('#estacion').val(),
                mv: $('#mv').val(),
            },
            type: 'POST',
            success: function (response) {
                if (response == '1') {
                    window.location.replace('/')
                }
                else if (response == '0') {
                    $('#message').show()
                    setMessage('CCV o MV inválido')
                }
            }
        }
      )
    }
}

function setMessage(msg) {
    $('#message').empty().append('<span><strong>' + msg + '</strong></span>')
}

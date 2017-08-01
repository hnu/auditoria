var uid = -1
var password_changed = false

var edit_new = 1

function edit_user(id)
{
    edit_new = 1
    $('#realname').val(users[id].urealname)
    $('#username').val(users[id].uname)
    $('#usertype').val(users[id].utype)
    $('#userpass').val('')
    $('#userpass').prop('disabled', false);
    uid = id
    password_changed = false
    $('#editDialog').modal('show');
}

function delete_user(id)
{
    $.ajax(
        {
            url: '/delete_user',
            data: {
                uid: id,
            },
            type: 'POST',
            success: function (response) {
                if (response == "1") {

                    $('#row_' + id).remove()
                    delete users[uid]
                }
            }
        }
      )

}

function pass_changed()
{
    password_changed = true
}

function edit_store()
{
    if (edit_new == 2)
        new_store()
    var realname = $('#realname').val()
    var username = $('#username').val()
    var usertype = $('#usertype').val()
    var pass = ''

    if (pass_changed)
    {
        pass = $('#userpass').val()
    }

    $.ajax(
        {
            url: '/edit_user',
            data: {
                uid: uid,
                realname: realname,
                username: username,
                usertype: usertype,
                pass: pass
            },
            type: 'POST',
            success: function (response) {
                if(response=="1")
                {
                    var newrow = '<td>'+realname+'</td>'
                    newrow += '<td>'+username+'</td>'
                    newrow += '<td>'+usertype+'</td>'
                    newrow += '<td><a href="#" onclick="edit_user(' + uid + ')">Modificar</a> &nbsp; <a href="#" onclick="delete_user(' + uid + ')">Eliminar</a></td>'

                    users[uid] = new User(uid, realname, username, usertype)

                    $('#row_' + uid).empty().append(newrow)
                }
            }
        }
      )

    $('#editDialog').modal('hide');
}

function new_store()
{
    var realname = $('#realname').val()
    var username = $('#username').val()
    var usertype = $('#usertype').val()
    var pass = $('#userpass').val()

    $.ajax(
        {
            url: '/new_user',
            data: {
                realname: realname,
                username: username,
                usertype: usertype,
                pass: pass
            },
            type: 'POST',
            success: function (response) {
                if (response != "0") {

                    
                    var newrow = '<td>' + realname + '</td>'
                    newrow += '<td>' + username + '</td>'
                    newrow += '<td>' + usertype + '</td>'
                    newrow += '<td><a href="#" onclick="edit_user(' + response + ')">Modificar</a> &nbsp; <a href="#" onclick="delete_user(' + response + ')">Eliminar</a></td>'

                    users[uid] = new User(uid, realname, username, usertype)

                    console.log("new")

                    console.log($('#table tr:last'))
                    
                    $('#table_body').append(newrow)
                    

                   // $('#table_body').empty().append(newrow)
                }
            }
        }
      )

    $('#editDialog').modal('hide');
}

function new_user()
{
    edit_new = 2
    $('#realname').val('')
    $('#username').val('')
    $('#usertype').val(3)
    $('#userpass').val('123123')
    $('#userpass').prop('disabled', true);

    uid = -1
    password_changed = false
    $('#editDialog').modal('show');


}

class User {
    constructor(uid, urealname, uname, utype)
    {
        this.uid = uid
        this.urealname = urealname
        this.uname = uname
        this.utype = utype
    }
}


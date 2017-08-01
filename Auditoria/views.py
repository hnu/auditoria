"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from Auditoria import app
import MySQLdb as mysql
import random

db_user = 'root'
db_pass = ''
db_name = 'auditoria'
db_address = 'localhost'

def updatePrivileges(userType):

    session.pop('logged_in', None)
    session.pop('users', None)
    session['utype'] = userType
    
    if userType == 0:
        session['logged_in'] = True
        session['users'] = True
    elif userType == 1:
        session['logged_in'] = True
    elif userType == 2:
        session['logged_in'] = True
    elif userType == 3:
        session['logged_in'] = True

@app.route('/')
@app.route('/home')
def home():

    if not 'user' in session:
        return redirect(url_for('login'))

    global db_address, db_user, db_pass, db_name
    con = mysql.connect(db_address, db_user, db_pass, db_name)

    with con:
        cur = con.cursor()

        if session['utype']<=1: # admin or coordinator
            sql = """select mv.id,tm.codigo,tm.mesa,tm.nombre,tm.direccion,e.nombre,m.nombre,p.nombre,u1.realname,u2.realname,mv.estacion 
from tabla_mesa tm, mv, estado e, municipio m, parroquia p, user u1, user u2
where mv.estacion is not null and mv.id_tm=tm.id and tm.id_estado=e.id and tm.id_estado=m.id_estado and tm.id_municipio=m.id_municipio and
tm.id_estado=p.id_estado and tm.id_municipio=p.id_municipio and tm.id_parroquia=p.id_parroquia and
u1.id = mv.asistente_id and u2.id = mv.auditor_id"""
        elif session['utype']==2: # auditor
            sql = """select mv.id,tm.codigo,tm.mesa,tm.nombre,tm.direccion,e.nombre,m.nombre,p.nombre,u1.realname,u2.realname,mv.estacion 
from tabla_mesa tm, mv, estado e, municipio m, parroquia p, user u1, user u2
where mv.estacion is not null and mv.id_tm=tm.id and tm.id_estado=e.id and tm.id_estado=m.id_estado and tm.id_municipio=m.id_municipio and
tm.id_estado=p.id_estado and tm.id_municipio=p.id_municipio and tm.id_parroquia=p.id_parroquia and
u1.id = mv.asistente_id and u2.id = mv.auditor_id and (u2.id=%d or u1.id=%d)"""%(session['uid'],session['uid'])
        elif session['utype']==3:  # asistente
            sql = """select mv.id,tm.codigo,tm.mesa,tm.nombre,tm.direccion,e.nombre,m.nombre,p.nombre,u1.realname,u2.realname,mv.estacion 
from tabla_mesa tm, mv, estado e, municipio m, parroquia p, user u1, user u2
where mv.estacion is not null and mv.id_tm=tm.id and tm.id_estado=e.id and tm.id_estado=m.id_estado and tm.id_municipio=m.id_municipio and
tm.id_estado=p.id_estado and tm.id_municipio=p.id_municipio and tm.id_parroquia=p.id_parroquia and
u1.id = mv.asistente_id and u2.id = mv.auditor_id and u1.id=%d"""%session['uid']

        cur.execute(sql)

        mvs = []
        ccvs = []

        for row in cur:
            cod_cuad = "%s%.2d1"%(row[1],row[2])
            ccvs.append(cod_cuad)
            mvs.append(row)

        #mvs = cur.fetchall

        #print(mvs)

        #for mv in mvs:
        #    cod_cuad = "%d%2d1"%(mv[1],mv[2])
         #   print(cod_cuad)


    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        mvs = mvs,
        ccvs = ccvs,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/cargarvotos', methods = ['POST'])
def cargarvotos():
    global db_address, db_user, db_pass, db_name

    if not 'user' in session:
        return redirect(url_for('login'))

    con = mysql.connect(db_address, db_user, db_pass, db_name)
    
    mv = request.form['mv']
    #mv = request.form['mv']

    with con:
        cur = con.cursor()
        sql = """select tm.codigo,tm.mesa,tm.nombre,e.nombre,m.nombre,p.nombre
from tabla_mesa tm, estado e, municipio m, parroquia p,mv
where mv.id=%s and tm.id=mv.id_tm and tm.id_estado=e.id and tm.id_estado=m.id_estado and tm.id_municipio=m.id_municipio and
tm.id_estado=p.id_estado and tm.id_municipio=p.id_municipio and tm.id_parroquia=p.id_parroquia"""%(mv)
        cur.execute(sql)
        data = cur.fetchone()

        sql = """select * from cargo_clase where id>=100"""
        cur.execute(sql)

        sectorial = []

        for row in cur:
            fila = {}
            fila['id'] = row[0]
            fila['nombre'] = row[1]
            sectorial.append(fila)

        # ahora buscamos para ese estado los candidatos validos territoriales
        # ahora los candidatos validos sectoriales nacionales
        # candidtaos validos sectoriales municipales
        # candidatos validos sectoriales regionales

    return render_template(
        'cargarvotos.html',
        title='Transcripción de Comprobantes',
        mv = mv,
        codcentro = data[0],
        nombre_centro = data[2],
        edo = data[3],
        mun = data[4],
        parr = data[5],
        mesa = data[1],
        sectorial = sectorial

    )


        
@app.route('/asignacion')
def asignacion():

    global db_address, db_user, db_pass, db_name

    con = mysql.connect(db_address, db_user, db_pass, db_name)

    with con:

        cur = con.cursor()
        cur.execute("select id,realname from user where type <= 2")
        users = cur.fetchall()

        cur.execute("select id from estacion")
        stations = cur.fetchall()

    """Renders the users page."""
    return render_template(
        'asignacion.html',
        title='Asignación',
        users = users,
        stations = stations,
    )



    return render_template(
        'asignacion.html',
        title='Asignación de MV',
    )

@app.route('/miclave')
def miclave():
    """Renders the contact page."""
    return render_template(
        'miclave.html',
        title='Mi Clave',
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/users')
def users():
    if not 'user' in session:
        return redirect(url_for('login'))

    if not 'users' in session:
        return redirect(url_for('home'))

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()
        cur.execute("select id,name,realname,type from user")
        rows = cur.fetchall()

    """Renders the users page."""
    return render_template(
        'users.html',
        title='Usuarios',
        users = rows,
    )

@app.route('/login')
def login():
    return render_template(
        'login.html',
        title='Login'
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
    updatePrivileges(-1)
    return redirect("/login")


@app.route('/change_my_pass', methods=['POST'])
def change_my_pass():

    global db_name, db_pass, db_user, db_address

    uid = session['uid']
    newpass= request.form['password']

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()

        cur.execute("update user set pass='%s' where id=%d"%(newpass, uid))

        return "1"

    return "0"


@app.route('/process_login', methods=['POST'])
def process_login():

    global db_name, db_pass, db_user, db_address

    name = request.form['user']
    password = request.form['password']

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()
        cur.execute("select count(1) from user where name='%s' and pass='%s'"%(name, password))
        row = cur.fetchone()

        response = row[0]

        if row[0]==1:  # set session
            session['user'] = name

            cur.execute("select id,type,realname from user where name='%s'"%(name))
            row = cur.fetchone()

            session['uid'] = row[0]
            session['utype'] = row[1]
            session['realname'] = row[2]

            updatePrivileges(row[1])



        return str(response)

    return 'Could not connect to database'


@app.route('/edit_user', methods=['POST'])
def edit_user():

    global db_name, db_pass, db_user, db_address

    uid = request.form['uid']
    realname = request.form['realname']
    username = request.form['username']
    usertype = request.form['usertype']
    passwd = request.form['pass']

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()
        changepass = ''
        if passwd != '':
            changepass = ",pass='%s'"%passwd
        sql = "UPDATE user SET name='%s',realname='%s',type=%s %s WHERE id=%s"%(username, realname, usertype,changepass,uid)
        cur.execute(sql)

        return "1"

    return "0"


@app.route('/new_user', methods=['POST'])
def new_user():

    global db_name, db_pass, db_user, db_address

    realname = request.form['realname']
    username = request.form['username']
    usertype = request.form['usertype']
    passwd = request.form['pass']

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()
        sql = "insert into user (name,pass,type,realname) values('%s','%s',%s,'%s')"%(username, passwd, usertype,realname)
        cur.execute(sql)

        sql = "SELECT LAST_INSERT_ID()"
        cur.execute(sql)
        row = cur.fetchone()
        response = row[0]

        return str(response)

    return "0"

@app.route('/delete_user', methods=['POST'])
def delete_user():

    global db_name, db_pass, db_user, db_address

    uid = request.form['uid']
    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()
        sql = "delete from user where id=%s"%uid
        cur.execute(sql)

        return "1"

    return "0"



@app.route('/process_asignacion', methods=['POST'])
def process_asignacion():

    global db_name, db_pass, db_user, db_address

    asistente = session['uid']
    auditor = request.form['auditor']
    estacion = request.form['estacion']
    mv = request.form['mv']

    mv = mv.replace('.','')

    con = mysql.connect(db_address, db_user, db_pass, db_name);

    with con:
        cur = con.cursor()

        sql = "SELECT id FROM mv WHERE id=%s"%mv
        cur.execute(sql)
        row = cur.fetchone()

        if row == None:
            sql = "SELECT id FROM mv WHERE ccv='%s'"%mv
            cur.execute(sql)
            row = cur.fetchone()

            if row == None:  # not found
                return "0"

            mv = row[0]

        sql = "update mv set asistente_id=%s,auditor_id=%s,estacion=%s where id=%s"%(asistente, auditor,estacion,mv)
        cur.execute(sql)

        return "1"

    return "0"

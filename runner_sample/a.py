from bottle import route, run, template, post, get, request
import sqlite3
con = sqlite3.connect('running.db')
cur = con.cursor()

@post('/insert')
def insert():
    runnername = request.forms.get('runnername')
    age = request.forms.get('age')
    yearsrunning = request.forms.get('yearsrunning')
    favrace = request.forms.get('favrace')
    # print(runnername, age, yearsrunning, favrace)
    cur.execute("insert into runner values ('{0}', {1}, {2}, '{3}')".format(runnername, age, yearsrunning, favrace))
    con.commit()
    return runnername +  " inserted </br> return to main <a href = \"/listall\">page</a>"

@route('/delete/<name>')
def delete(name):
    cur.execute("delete from runner where runnername = '" + name + "'")
    con.commit()
    return name + " deleted </br> return to main <a href = \"/listall\">page</a>"

@route('/listall')
def hello():
    html = "<h2> all runners</h2> <br /> <table>"
    for row in cur.execute('select * from runner'):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
        html += "<td><a href=\"/delete/" + row[0] + "\">delete me</a> </td>  </tr>"
    html += "</table>"

    html += "<br /><br /><br /><br /><br />"
    html += '''
        <form action = "/insert" method = "post">
            Runnername: <input name = "runnername" type="text" />
            age: <input name = "age" type="text" />
            yearsrunning: <input name = "yearsrunning" type="text" />
            favrace: <input name = "favrace" type="text" />
            <input value = "Insert!" type = "submit" />
        </form>
    '''
    return html

run(host='localhost', port=8080, debug = True)
import bottle
from bottle import request
import sqlite3

app = bottle.Bottle()

con = sqlite3.connect('ecommerce.db')
cur = con.cursor()

PER_PAGE = 20
USER_TOTAL, = cur.execute('SELECT COUNT(*) FROM customers').fetchone()

@app.route('/customer/<user_id>')
def detail(user_id):
    customer = cur.execute('SELECT cust_id, cust_name, cust_email, def_bill_add, def_ship_add, cust_phone FROM customers WHERE cust_id=' + user_id)

    html = "<a href=\"/\">Back</a>"
    for row in customer:
        html += "<h1>" + row[1] + "</h1> <br/> <table>"
        for cell in row[2:]:
            html += "<tr> <td>" + str(cell) + "</td> </tr> "
        html += "</table>"

    return html

@app.route('/')
@app.route('/<page:int>')
def main(page=0):
    # number of records per page
    per = int(request.query.per or PER_PAGE)
    start, end = page*PER_PAGE, (page+1)*PER_PAGE

    contacts = cur.execute(f'SELECT cust_id, cust_name, cust_email, cust_phone FROM customers WHERE cust_id >= {start} AND cust_id < {end}')
    has_next = end < USER_TOTAL
    query_string = '?per=' + str(per)

    html = "<h1>Basic Customer Contacts</h1> <br/>"
    html += "<h2>" + str(page) + "<h2> <br/>"
    html += "<table>"
    for row in contacts:
        html += "<tr>"
        for cell in row[1:]:
            html += "<td>" + str(cell) + "</td>"
        html += "<td> <a href=\"/customer/" + str(row[0]) + "\">View Details</a> </td> </tr>"
    html += "</table>"

    if page > 0:
        if page == 1:
            html += "<a href=\"/" + query_string + "\">prev</a>"
        else:
            html += "<a href=\"" + str((page-1)) + query_string + "\">prev</a>"
    if has_next:
        html += "<a href=\"" + str((page+1)) + query_string + "\">next</a>"

    return html

if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug = True)
from bottle import route, run, template, post, get, request
import sqlite3

con = sqlite3.connect('ecommerce.db')
cur = con.cursor()

@route('/contacts/<user_id>')
def detail(user_id):
    customer = cur.execute('select cust_id, cust_name, cust_email, def_bill_add, def_ship_add, cust_phone from customers where cust_id=' + user_id)

    html = "<a href=\"/contacts/\">Back</a>"
    for row in customer:
        html += "<h1>" + row[1] + "</h1> <br/> <table>"
        for cell in row[2:]:
            html += "<tr> <td>" + str(cell) + "</td> </tr> "
        html += "</table>"

    return html

@route('/contacts/')
@route('/contacts')
def main():
    contacts = cur.execute('select cust_id, cust_name, cust_email, cust_phone from customers')

    html = "<h1>Basic Customer Contacts</h1> <br/> <table>"
    for row in contacts:
        html += "<tr>"
        for cell in row[1:]:
            html += "<td>" + str(cell) + "</td>"
        html += "<td> <a href=\"/contacts/" + str(row[0]) + "\">View Details</a> </td> </tr>"
    html += "</table>"

    return html

run(host='localhost', port=8080, debug = True)
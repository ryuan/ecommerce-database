import bottle
from bottle import request, jinja2_template as template
import sqlite3

app = bottle.Bottle()

con = sqlite3.connect('ecommerce.db')
cur = con.cursor()

PER_PAGE = 30
TOTAL, = cur.execute('SELECT COUNT(*) FROM products').fetchone()


@app.post('/search')
def search():
    # collect GET query data
    if request.forms.get('p_name') != None:
        p_name = request.forms.get('p_name')
    if request.forms.get('type') != None:
        type = request.forms.get('type')
    if request.forms.get('vendor') != None:
        vendor = request.forms.get('vendor')

    results = cur.execute('SELECT p_id, p_name, type, vendor FROM products WHERE p_name LIKE \"%' + p_name.strip() + '%\" AND type LIKE \"%' + type.strip() + '%\" AND vendor LIKE \"%' + vendor.strip() + '%\" LIMIT 20;')

    keys = ('p_id', 'p_name', 'type', 'vendor')
    results = (dict(zip(keys, result)) for result in results)

    parameters = {
        'results' : results,
        }

    return template("search.html", **parameters)


@app.route('/product/<p_id>')
def detail(p_id):
    # fetch the db data for p_id
    product = cur.execute('SELECT * FROM products WHERE p_id =' + p_id + ';')
    keys = ('p_id', 'p_name', 'type', 'vendor', 'p_description')
    product = (dict(zip(keys, data)) for data in product)

    parameters = {
        'p_id' : p_id,
        'product' : product
        }

    return template("product.html", **parameters)

@app.route('/')
@app.route('/<page:int>')
def main(page=0):
    # number of records per page
    per = int(request.query.per or PER_PAGE)
    start, end = page*per, (page+1)*per

    # fetch the db data
    products = cur.execute(f'SELECT p_id, p_name, type, vendor FROM products WHERE p_id >= {start} AND p_id < {end};')
    keys = ('p_id', 'p_name', 'type', 'vendor')
    products = (dict(zip(keys, product)) for product in products)

    parameters = {
        'page' : page,
        'products' : products,
        'has_next' : end < TOTAL,
        'query_string' : '?' + request.query_string,
        }

    return template('home.html', **parameters)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug = True)
import bottle
from bottle import static_file, request, jinja2_template as template
import sqlite3

app = bottle.Bottle()

con = sqlite3.connect('ecommerce.db')
cur = con.cursor()

PER_PAGE = 20


@app.route('/delete')
def delete():
    p_id = request.query.get('p_id')

    # fetch just the name of the p_id product to display confirmation in view
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    cur.execute(f'DELETE FROM products WHERE p_id = { p_id };')
    con.commit()

    parameters = {
        'p_name' : p_name,
        }

    return template("delete.html", parameters)


@app.post('/search')
def search():
    queries = {
        'p_name': '',
        'type': '',
        'vendor': ''
        }

    # collect GET query data
    if request.forms.get('p_name') != None:
        p_name = request.forms.get('p_name')
        queries["p_name"] += p_name.strip()
    if request.forms.get('type') != None:
        type = request.forms.get('type')
        queries["type"] += type.strip()
    if request.forms.get('vendor') != None:
        vendor = request.forms.get('vendor')
        queries["vendor"] += vendor.strip()

    results = cur.execute('SELECT p_id, p_name, type, vendor FROM products WHERE p_name LIKE \"%' + p_name.strip() + '%\" AND type LIKE \"%' + type.strip() + '%\" AND vendor LIKE \"%' + vendor.strip() + '%\" LIMIT 20;')

    keys = ('p_id', 'p_name', 'type', 'vendor')
    results = (dict(zip(keys, result)) for result in results)

    parameters = {
        'queries' : queries,
        'results' : results,
        }

    return template("search.html", **parameters)


@app.route('/product/<p_id>')
def detail(p_id):
    # fetch just the name of the p_id product for meta tag title
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    # fetch the db data for p_id
    product = cur.execute('SELECT * FROM products WHERE p_id =' + p_id + ';')
    keys = ('p_id', 'p_name', 'type', 'vendor', 'p_description')
    product = (dict(zip(keys, data)) for data in product)

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'product' : product
        }

    return template("product.html", **parameters)


@app.route('/')
@app.route('/<page:int>')
def main(page=0):
    # number of records per page
    per = int(request.query.per or PER_PAGE)
    start, end = page*per, (page+1)*per
    total, = cur.execute('SELECT COUNT(*) FROM products').fetchone()

    # fetch the db data
    products = cur.execute(f'SELECT p_id, p_name, type, vendor FROM products WHERE p_id >= {start} AND p_id < {end};')
    keys = ('p_id', 'p_name', 'type', 'vendor')
    products = (dict(zip(keys, product)) for product in products)

    parameters = {
        'page' : page,
        'products' : products,
        'has_next' : end < total,
        'total_products' : total,
        'query_string' : '?' + request.query_string,
        }

    return template('index.html', **parameters)


# Static CSS and favicon files
@app.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css')

@app.route('/static/images/<filename:re:.*\.ico>')
def send_favicon(filename):
    return static_file(filename, root='static/images')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug = True)
from urllib import response
import bottle
from bottle import static_file, HTTP_CODES, request, jinja2_template as template
import sqlite3
from inflection import parameterize

from numpy import var

app = bottle.Bottle()

con = sqlite3.connect('ecommerce.db')
cur = con.cursor()

PER_PAGE = 20


@app.route('/product/<p_id>/variants/create')
@app.route('/product/<p_id>/variants/create/')
def create_var(p_id):
    # fetch just the name of the p_id product for dynamic reference
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name
        }

    return template("create_var.html", parameters)


@app.post('/product/<p_id>/variants/insert')
@app.post('/product/<p_id>/variants/insert/')
def insert_var(p_id):
    # fetch just the name of the p_id product to display confirmation in view
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    v_title = request.forms.get('v_title')
    v_name = request.forms.get('v_name')
    sku = request.forms.get('sku')
    price = int(float(request.forms.get('price')) * 100)
    quantity = int(request.forms.get('quantity'))
    weight = int(float(request.forms.get('weight')) / 0.0625)

    # insert new variant as tuple into variants table
    cur.execute(f'INSERT INTO variants (v_title, v_name, sku, price, quantity, weight, p_id) VALUES ("{v_title}", "{v_name}", "{sku}", {price}, {quantity}, {weight}, {p_id});')
    con.commit()

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'v_title' : v_title,
        'v_name' : v_name,
        'sku' : sku,
        'price' : price,
        'quantity' : quantity,
        'weight' : weight
        }

    return template("insert_var.html", parameters)


@app.post('/product/<p_id>/variants/update')
@app.post('/product/<p_id>/variants/update/')
def update_var(p_id):
    # fetch just the name of the p_id product to display confirmation in view
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    v_id = request.forms.get('v_id')
    v_title = request.forms.get('v_title')
    v_name = request.forms.get('v_name')
    sku = request.forms.get('sku')
    price = int(float(request.forms.get('price')) * 100)
    quantity = int(request.forms.get('quantity'))
    weight = int(float(request.forms.get('weight')) / 0.0625)

    # update variant given v_id
    cur.execute(f'UPDATE variants SET v_title = "{ v_title }", v_name = "{ v_name }", sku = "{ sku }", price = { price }, quantity = { quantity }, weight = { weight } WHERE v_id = { v_id };')
    con.commit()

    price = format(price * 0.01, ".2f")
    weight = format(weight * 0.0625, ".2f")

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'v_title' : v_title,
        'v_name' : v_name,
        'sku' : sku,
        'price' : price,
        'quantity' : quantity,
        'weight' : weight
        }

    return template("update_var.html", parameters)


@app.route('/product/<p_id>/variants')
@app.route('/product/<p_id>/variants/')
def variants(p_id):
    # fetch just the name of the p_id product for dynamic reference
    product = cur.execute('SELECT p_name FROM products WHERE p_id =' + p_id + ';')
    p_name = product.fetchone()[0]

    # fetch the db data for p_id's variants
    variants = cur.execute('SELECT * FROM variants WHERE p_id =' + p_id + ';')

    keys = ('v_id', 'sku', 'v_title', 'v_name', 'price', 'quantity', 'weight')
    variants = (dict(zip(keys, variant)) for variant in variants)

    fixed_variants = []
    for variant in variants:
        variant['price'] = format(variant['price'] * 0.01, ".2f")
        variant['weight'] = format(variant['weight'] * 0.0625, ".2f")
        fixed_variants.append(variant)

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'variants' : fixed_variants
        }

    return template("variants.html", **parameters)


@app.route('/create')
@app.route('/create/')
def create_pro():
    return template("create_pro.html")


@app.post('/insert')
@app.post('/insert/')
def insert_pro():
    p_name = request.forms.get('p_name')
    type = request.forms.get('type')
    vendor = request.forms.get('vendor')
    p_description = request.forms.get('p_description')

    # insert new variant as tuple into variants table
    cur.execute(f'INSERT INTO products (p_name, type, vendor, p_description) VALUES ("{p_name}", "{type}", "{vendor}", "{p_description}");')
    con.commit()

    # fetch the p_id of the most recently added tuple
    row = cur.execute('SELECT last_insert_rowid();')
    p_id = row.fetchone()[0]

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'type' : type,
        'vendor' : vendor,
        'p_description' : p_description
        }

    return template("insert_pro.html", parameters)


@app.route('/delete')
@app.route('/delete/')
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


@app.post('/product/<p_id>/update')
@app.post('/product/<p_id>/update/')
def update_pro(p_id):
    p_name = request.forms.get('p_name')
    type = request.forms.get('type')
    vendor = request.forms.get('vendor')
    p_description = request.forms.get('p_description')

    # update variant given v_id
    cur.execute(f'UPDATE products SET p_name = "{ p_name }", type = "{ type }", vendor = "{ vendor }", p_description = "{ p_description }" WHERE p_id = { p_id };')
    con.commit()

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'type' : type,
        'vendor' : vendor,
        'p_description' : p_description
        }

    return template("update_pro.html", parameters)


@app.route('/product/<p_id>')
@app.route('/product/<p_id>/')
def product(p_id):
    # fetch p_id's product data from the db
    product = cur.execute('SELECT p_name, type, vendor, p_description FROM products WHERE p_id =' + p_id + ';')
    product = product.fetchone()
    p_name = product[0]
    type = product[1]
    vendor = product[2]
    p_description = product[3]

    # fetch the db data for p_id's variants
    variants = cur.execute('SELECT v_id, v_title, v_name, price, quantity FROM variants WHERE p_id =' + p_id + ';')

    keys = ('v_id', 'v_title', 'v_name', 'price', 'quantity')
    variants = (dict(zip(keys, variant)) for variant in variants)

    fixed_variants = []
    for variant in variants:
        variant['price'] = format(variant['price'] * 0.01, ".2f")
        fixed_variants.append(variant)

    parameters = {
        'p_id' : p_id,
        'p_name' : p_name,
        'type' : type,
        'vendor' : vendor,
        'p_description' : p_description,
        'variants' : fixed_variants
        }

    return template("product.html", **parameters)


@app.post('/search')
@app.post('/search/')
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

    results = cur.execute('SELECT p_id, p_name, type, vendor FROM products WHERE p_name LIKE "%' + p_name.strip() + '%" AND type LIKE \"%' + type.strip() + '%\" AND vendor LIKE \"%' + vendor.strip() + '%\" LIMIT 20;')

    keys = ('p_id', 'p_name', 'type', 'vendor')
    results = (dict(zip(keys, result)) for result in results)

    parameters = {
        'queries' : queries,
        'results' : results,
        }

    return template("search.html", **parameters)


@app.route('/')
@app.route('/<page:int>')
def index(page=0):
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


# Error handling
@app.error(400)
@app.error(403)
@app.error(404)
@app.error(405)
@app.error(406)
@app.error(407)
@app.error(408)
@app.error(413)
@app.error(414)
@app.error(415)
@app.error(416)
@app.error(417)
@app.error(418)
@app.error(422)
@app.error(423)
@app.error(428)
@app.error(429)
@app.error(431)
@app.error(500)
@app.error(501)
@app.error(502)
@app.error(503)
@app.error(504)
@app.error(511)
def error_handler(error):

    parameters = {
        'error' : error
        }
    return template("error_handler.html", parameters)



if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug = True)
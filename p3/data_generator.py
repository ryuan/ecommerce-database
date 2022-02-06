#Import the packages 
from turtle import st
from faker import Faker 
import faker_commerce
import random

#Initiate the Faker object 
fake = Faker()
fake.add_provider(faker_commerce.Provider)

#Prepare additional pool of data to randomly draw from
vendors = ["Billabong", "Burton", "Bauer", "CCM", "West Elm", "Adidas", "Zara", "Anthropologie"]
var_titles = ["Title", "Size", "Color"]
var_names = [["Default"],["Small", "Medium", "Large"], ["Blue","Red","Green","Black","White"]]
c_pre_1 = ["Summer", "Back-to-School", "Independence Day", "Christmas", "Labor Day", "Memorial Day"]
c_pre_2 = ["Modern Furniture", "Essentials", "Jeans", "Must-Have Tech", "Tech Lovers", "Ski and Snowboard"]
c_suf = ["Collection", "Sale", "Releases", "Flash Sale", "Sales Event"]
ship_opts = ["Ground", "2-Day", "Next Day"]
ship_costs = [0, 10, 20]
order_statuses = ["Canceled", "Processed", "Shipped", "Delivered", "Refund Requested", "Refunded"]


#Initialize insertion code containers
products = []
images = []
variants = []
collections = []
orders = []
customers = []
sellers = []
coll_prod = []
sell_prod = []
ord_prod = []
ord_cust = []


#Generate fake products
for i in range(30):
    p_name = fake.ecommerce_name()
    type = fake.ecommerce_category()
    vendor = vendors[random.randint(0,len(vendors)-1)]
    p_description = fake.paragraph(nb_sentences=5)
    
    products.append(f"INSERT INTO products VALUES ({i}, {p_name}, {type}, {vendor}, {p_description});")
    
    #Generate fake images
    for j in range(random.randint(1,4)):
        img_name = p_name.lower().replace(" ","_")
        img_vendor = vendor.lower().replace(" ","_")
        url = f"{img_name}_{img_vendor}_{j}.jpg"

        images.append(f"INSERT INTO images VALUES ({url}, {i});")

    #Generate variants
    title_choice = random.randint(0,len(var_titles)-1)
    num_variants = random.randint(0,len(var_names[title_choice])-1)
    start_index = random.randint(0,len(var_names[title_choice])-1-num_variants)
    base_price = random.randint(2000,30000)
    base_weight = random.randint(1,500)

    for k in range(num_variants+1):
        sku_prefix = p_name.upper().replace(" ","")[0:3] + p_name.upper().replace(" ","")[0:3]
        sku = f"{sku_prefix}{i}{k}"
        var_title = var_titles[title_choice]
        var_name = var_names[title_choice][start_index+k]
        price = int(base_price + (k * round(base_price * 0.1, 0)))
        quantity = random.randint(0,12)
        weight = int(base_weight + (k * round(base_price * 0.05, 0)))

        variants.append(f"INSERT INTO variants VALUES ({sku}, {var_title}, {var_name}, {price}, {quantity}, {weight});")


#Generate fake collections
for i in range(10):
    pre_1_choice = c_pre_1[random.randint(0, len(c_pre_1)-1)]
    pre_2_choice = c_pre_2[random.randint(0, len(c_pre_2)-1)]
    suf_choice = c_suf[random.randint(0, len(c_suf)-1)]
    c_name = pre_1_choice + " " + pre_2_choice + " " + suf_choice
    c_description = fake.paragraph(nb_sentences=3)

    collections.append(f"INSERT INTO collections VALUES ({i}, {c_name}, {c_description});")


#Generate fake orders
for i in range(20):
    ship_opt = random.randint(0, len(ship_opts)-1)
    ship_cost = ship_opts[ship_opt]
    person = fake.profile()
    bill_add = person['address']
    ship_add = person['residence']
    o_date = fake.date_this_decade()
    o_phone = fake.phone_number()
    o_status = order_statuses[random.randint(0, len(order_statuses)-1)]

    orders.append(f"INSERT INTO orders VALUES ({i}, {ship_opt}, {ship_cost}, {bill_add}, {ship_add}, {o_date}, {o_phone}, {o_status});")


#Generate fake customers
for i in range(15):
    person = fake.profile()
    cust_name = person['name']
    cust_email = person['mail']
    cust_password = fake.sha256(raw_output=False)
    def_bill_add = person['address']
    def_ship_add = person['residence']
    cust_phone = fake.phone_number()

    customers.append(f"INSERT INTO customers VALUES ({i}, {cust_name}, {cust_email}, {cust_password}, {def_bill_add}, {def_ship_add}, {cust_phone});")


#Generate fake sellers
for i in range(10):
    s_name = fake.name()
    s_email = fake.email()
    s_password = fake.sha256(raw_output=False)
    bus_name = fake.company(),
    bus_phone = fake.phone_number()
    dummy_ssn = fake.ssn().replace("-","")
    ein = dummy_ssn[:3] + "-" + dummy_ssn[3:]

    sellers.append(f"INSERT INTO sellers VALUES ({i}, {s_name}, {s_email}, {s_password}, {bus_name}, {bus_phone}, {ein});")


#Generate coll_prod relationships
indices = []
for i in range(len(products)):
    indices.append(i)
for i in range(len(collections)):
    selection = random.choices(indices, k = len(indices))
    for j in selection:
        coll_prod.append(f"INSERT INTO coll_prod VALUES ({i},{j});")


#Generate sell_prod relationships
indices = []
for i in range(len(sellers)):
    indices.append(i)
for i in range(len(products)):
    selection = random.choice(indices)
    sell_prod.append(f"INSERT INTO sell_prod VALUES ({selection},{i});")


#Generate ord_prod relationships
indices = []
for i in range(len(products)):
    indices.append(i)
for i in range(len(orders)):
    order_size = random.choices([1,2,3,4,5,6], weights = [10,5,3,2,1,1], k=1)
    selection = random.choices(indices, k = order_size[0])
    for j in selection:
        ord_prod.append(f"INSERT INTO ord_prod VALUES ({i},{j});")


#Generate ord_cust relationships
indices = []
for i in range(len(customers)):
    indices.append(i)
for i in range(len(orders)):
    selection = random.choice(indices)
    ord_cust.append(f"INSERT INTO ord_cust VALUES ({i},{selection});")



print("---------PRODUCTS INSERTION CODE---------")
for product in products:
    print(product)
print("---------IMAGES INSERTION CODE---------")
for image in images:
    print(image)
print("---------VARIANTS INSERTION CODE---------")
for variant in variants:
    print(variant)
print("---------COLLECTIONS INSERTION CODE---------")
for collection in collections:
    print(collection)
print("---------ORDERS INSERTION CODE---------")
for order in orders:
    print(order)
print("---------CUSTOMERS INSERTION CODE---------")
for customer in customers:
    print(customer)
print("---------SELLERS INSERTION CODE---------")
for seller in sellers:
    print(seller)


print("---------COLL_PROD INSERTION CODE---------")
for r in coll_prod:
    print(r)
print("---------SELL_PROD INSERTION CODE---------")
for r in sell_prod:
    print(r)
print("---------ORD_PROD INSERTION CODE---------")
for r in ord_prod:
    print(r)
print("---------ORD_CUST INSERTION CODE---------")
for r in ord_cust:
    print(r)
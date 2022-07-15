"""
Generates fake data for the ecommerce SQL database. Output is a .sql file with insertion queries.
Author: Ruoda Yuan
"""

#Import the packages 
from turtle import st
from faker import Faker 
import faker_commerce
import random


def main():
    #Initiate the Faker object 
    fake = Faker()
    fake.add_provider(faker_commerce.Provider)

    #Prepare additional pool of data to randomly draw from
    vendors = ["Billabong", "Burton", "Bataleon", "Rossignol", "Salomon", "Arbor", "Bauer", "CCM", "True", "Warrior", "West Elm", "CB2", "Williams-Sonoma", "Oculus", "DJI", "Sony", "Apple", "Western Digital", "Nike", "Adidas", "Champion", "Zara", "Brandy Melville", "Banana Republic", "Free People", "EverLane", "Spell", "Anthropologie", "rag & bone", "Patagonia", "Arc''teryx", "Fjällräven"]
    v_titles = ["Title", "Size", "Color"]
    v_names = [["Default"],["Small", "Medium", "Large"], ["Blue","Red","Green","Black","White"]]
    c_pre_1 = ["Spring", "Summer", "Fall", "Winter", "Back-to-School", "Independence Day", "Christmas", "Labor Day", "Memorial Day", "New Year", "Black Friday", "Anniversary", "Valentine''s Day", "Chinese New Year", "President''s Day", "Mother''s Day", "Father''s Day", "4th of July", "Cyber Monday", "Halloween", "Editors'' Picks"]
    c_pre_2 = ["Modern Furniture", "Essentials", "Jeans", "Must-Have Tech", "Tech Lovers", "Ski & Snowboard", "Gear", "New Release", "Fresh Designs", "Blockbuster Clearance", "Limited Time", "Closeout", "Hot Styles", "Wardrobe Favorites", "New Season", "Hockey Must-Haves"]
    c_suf = ["Collection", "Sale", "Flash Sale", "Event", "Promotions", "Sales Event"]
    ship_opts = ["Ground", "2-Day", "Next Day"]
    ship_costs = [5, 10, 20]
    order_statuses = ["Canceled", "Processed", "Shipped", "Delivered", "Refund Requested", "Refunded"]


    #Initialize dictionary for storing each table's generated data
    master_data = {
        "products": [],
        "images": [],
        "variants": [],
        "collections": [],
        "orders": [],
        "customers": [],
        "sellers": [],
        "coll_prod": [],
        "sell_prod": [],
        "ord_var": [],
        "ord_cust": []
        }

    v_indices = []      #used to store v_id for order generation
    v_free_index = 0    #used to track next index available for variant index assignment
    customers_basics = {}


    #Generate fake products
    for i in range(8000):
        p_name = fake.ecommerce_name()
        type = fake.ecommerce_category()
        vendor = vendors[random.randint(0,len(vendors)-1)]
        p_description = fake.paragraph(nb_sentences=5)
        
        master_data["products"].append(f"INSERT INTO products VALUES ({i}, '{p_name}', '{type}', '{vendor}', '{p_description}');")
        
        #Generate fake images
        for j in range(random.randint(1,4)):
            img_name = p_name.lower().replace(" ","_")
            img_vendor = vendor.lower().replace(" ","_")
            url = f"{i}_{img_name}_{img_vendor}_{j}.jpg"

            master_data["images"].append(f"INSERT INTO images VALUES ('{url}', {i});")

        #Generate variants
        title_choice = random.randint(0,len(v_titles)-1)
        num_variants = random.randint(0,len(v_names[title_choice])-1)
        start_index = random.randint(0,len(v_names[title_choice])-1-num_variants)
        base_price = random.randint(1500,120000)
        base_weight = random.randint(1,500)

        for k in range(num_variants+1):
            v_title = v_titles[title_choice]
            v_name = v_names[title_choice][start_index+k]
            sku_prefix = p_name.upper().replace(" ","")[0:3] + type.upper().replace(" ","")[0:3] + v_name.upper().replace(" ","")[0:3]
            sku = f"{sku_prefix}{i}{k}"
            price = int(base_price + (k * round(base_price * 0.1, 0)))
            quantity = random.randint(0,12)
            weight = int(base_weight + (k * round(base_price * 0.05, 0)))

            master_data["variants"].append(f"INSERT INTO variants VALUES ({v_free_index} ,'{sku}', '{v_title}', '{v_name}', {price}, {quantity}, {weight}, {i});")

            v_indices.append(v_free_index)
            v_free_index += 1


    #Generate fake collections
    for i in range(50):
        pre_1_choice = c_pre_1[random.randint(0, len(c_pre_1)-1)]
        pre_2_choice = c_pre_2[random.randint(0, len(c_pre_2)-1)]
        suf_choice = c_suf[random.randint(0, len(c_suf)-1)]
        c_name = pre_1_choice + " " + pre_2_choice + " " + suf_choice
        c_description = fake.paragraph(nb_sentences=3)

        master_data["collections"].append(f"INSERT INTO collections VALUES ({i}, '{c_name}', '{c_description}');")


    #Generate fake customers
    for i in range(5000):
        person = fake.profile()
        cust_name = person['name']
        cust_email = person['mail']
        cust_password = fake.sha256(raw_output=False)
        def_bill_add = person['address']
        def_ship_add = person['residence']
        cust_phone = fake.phone_number()

        customers_basics[i] = {"def_bill_add": def_bill_add, "def_ship_add": def_ship_add, "cust_phone": cust_phone}

        master_data["customers"].append(f"INSERT INTO customers VALUES ({i}, '{cust_name}', '{cust_email}', '{cust_password}', '{def_bill_add}', '{def_ship_add}', '{cust_phone}');")


    #Generate fake sellers
    for i in range(250):
        s_name = fake.name()
        s_email = fake.email()
        s_password = fake.sha256(raw_output=False)
        bus_name = fake.company()
        bus_phone = fake.phone_number()
        dummy_ssn = fake.ssn().replace("-","")
        ein = dummy_ssn[:3] + "-" + dummy_ssn[3:]

        master_data["sellers"].append(f"INSERT INTO sellers VALUES ({i}, '{s_name}', '{s_email}', '{s_password}', '{bus_name}', '{bus_phone}', '{ein}');")


    #Generate fake orders
    for i in range(10000):
        option = random.randint(0, len(ship_opts)-1)
        ship_opt = ship_opts[option]
        ship_cost = ship_costs[option]

        #Generate ord_cust relationships
        customer_id = random.choice(list(customers_basics))
        customer = customers_basics[customer_id]
        master_data["ord_cust"].append(f"INSERT INTO ord_cust VALUES ({i},{customer_id});")
        
        bill_add = random.choices([customer["def_bill_add"], fake.address()], weights = [90,10], k=1)[0]
        ship_add = random.choices([customer["def_ship_add"], fake.address()], weights = [90,10], k=1)[0]
        o_date = fake.date_this_decade()
        o_time = fake.time()
        o_phone = random.choices([customer["cust_phone"], fake.phone_number()], weights = [80,10], k=1)[0]
        o_status = order_statuses[random.randint(0, len(order_statuses)-1)]

        master_data["orders"].append(f"INSERT INTO orders VALUES ({i}, '{ship_opt}', {ship_cost}, '{bill_add}', '{ship_add}', '{o_date}', '{o_time}', '{o_phone}', '{o_status}');")


    #Generate coll_prod relationships
    indices = []
    for i in range(len(master_data["products"])):
        indices.append(i)
    for i in range(len(master_data["collections"])):
        selection = random.choices(indices, k = len(indices))
        for j in selection:
            master_data["coll_prod"].append(f"INSERT INTO coll_prod VALUES ({i},{j});")


    #Generate sell_prod relationships
    indices = []
    for i in range(len(master_data["sellers"])):
        indices.append(i)
    for i in range(len(master_data["products"])):
        selection = random.choice(indices)
        master_data["sell_prod"].append(f"INSERT INTO sell_prod VALUES ({selection},{i});")


    #Generate ord_var relationships
    for i in range(len(master_data["orders"])):
        order_size = random.choices([1,2,3,4,5,6], weights = [60,20,10,6,3,1], k=1)
        selection = random.choices(v_indices, k = order_size[0])
        for j in selection:
            master_data["ord_var"].append(f"INSERT INTO ord_var VALUES ({i},{j});")


    #Write all data to populate_db.sql file
    with open(f'populate_db.sql', 'w') as f:
        for name, dataset in master_data.items():
            f.write("--\n")
            f.write(f"-- Data for Name: {name}; Type: TABLE DATA\n")
            f.write("--\n")
            for data in dataset:
                f.write(f"{data}\n")


if __name__ == "__main__":
    main()
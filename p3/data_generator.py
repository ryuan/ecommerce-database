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

#Initialize insertion code containers
products = []
images = []
variants = []

#Generate fake products
for i in range(30):
    p_name = fake.ecommerce_name()
    type = fake.ecommerce_category()
    vendor = vendors[random.randint(0,len(vendors)-1)]
    
    products.append(f"INSERT INTO products VALUES ({i}, {p_name}, {type}, {vendor});")
    
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


print("---------PRODUCTS INSERTION CODE---------")
for product in products:
    print(product)
print("---------IMAGES INSERTION CODE---------")
for image in images:
    print(image)
print("---------VARIANTS INSERTION CODE---------")
for variant in variants:
    print(variant)
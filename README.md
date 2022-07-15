# Nozama Online Store Database

For my database final project, I built an ecommerce relational database and created a front-end product management portal for a theoretical online store called Nozama (Amazon spelled backwards).

## Usage

To make things easier, I prepared the SQLite database called ecommerce.db. Thus, you just need to run the main python file.

Navigate to this p8 directory on terminal and run final.py.

```console
python3 final.py
```

Once the terminal has loaded the data and prepared the website, open a web browser and visit http://localhost:8080/.

## Completion Status

### Features

Everything is complete and more! The RelationX is the product table and RelationY are all the products' variants (ex., color, size).

You can create, edit and delete products. Deleting any product will delete all of its associated variants since the database is set to cascade delete.

You can create and edit variants, each associated with its corresponding product via foreign key (more specifically, the product ID is passed by hidden input).

Searching also is comprehensive, allowing any combination of field to be filled. Leaving all fields blank will return all products. Each search is always limited to max of 20 results per project guidelines.

### Error Handling

I implemented 3 layers of error handling.

The first defence is via HTML/CSS, where each field with value/format restriction will check the input and either block certain keyboard inputs and also trigger a warning popup when clicking the button for the specific fields that need correcting.

The second defence is in the main Python code, where attributes are checked in each insertion, update, and deletion fields (as well as other functions in umbrella try-except clauses) to specifically verify format and return a custom error handling page with guidance on what needs to be fixed (for example, non-empty values, negative numbers, etc.).

The third and final defence is implemented by a combination of Bottle's HTTPError exception and error() decorator, with Bottle automatically detecting any 404 or 500 status codes and returning our custom error handling page.


## Rebuilding/Editing the Database
If you'd like new data, you can follow these steps below (you can pick and choose which parts you need).

To generate new fake data for the store, run on terminal:
```console
python3 data_generator.py
```

This will write new fake data into the populate_db.sql file. Now, rebuild the ecommerce.db file.

Launch sqlite on terminal:
```console
sqlite3 
```

Once it's launched, create the tables, populate it, and then save the new database:

```sql
.read create_db.sql
.read populate_db.sql
.save ecommerce.db
```

Exit sqlite and rerun the main final.py file.
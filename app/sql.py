import sqlite3


with sqlite3.connect("losquatroamigos.db") as connection:
    c = connection.cursor()

    ##TABLES##

    #restaurant##
    c.execute('DROP TABLE if EXISTS restaurant')
    c.execute("""CREATE TABLE restaurant (
    res_id nchar(1) not null,
    name varchar(20) not null,
    address varchar(40) not null,
    phone nchar(10) not null,
    postal nchar(5) not null,
    PRIMARY KEY (res_id)
    )""")

    #employees##
    c.execute('DROP TABLE if EXISTS employees')
    c.execute("""CREATE TABLE employees (
    emp_id VARCHAR(5) not null,
    emp_fname varchar(20) not null,
    emp_lname varchar(20) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    phone nchar(10) not null,
    ssn varchar(9),
    birthdate DATE not null,
    salary decimal(5,2) not null,
    date_hired [timestamp] timestamp,
    PRIMARY KEY (emp_id)
    )""")

    #users##
    c.execute('DROP TABLE if EXISTS users')
    c.execute("""CREATE TABLE users (
    user_id VARCHAR(9) not null,
    user_fname varchar(20) not null,
    user_lname varchar(40) not null,
    password VARCHAR(20) NOT NULL,
    email VARCHAR(40),
    address varchar(40) not null,
    city varchar(20) not null,
    postal nchar(5) not null,
    phone nchar(10) not null,
    memb_since DATE not null,
    acc_funds decimal(7,2) not null,
    PRIMARY KEY (user_id)
    )""")

    #ratings##
    c.execute('DROP TABLE if EXISTS foodrating')
    c.execute("""CREATE TABLE foodrating (
    user_id VARCHAR(9) not null,
    menu_id VARCHAR(5) not null,
    menu_item varchar(50) not null,
    rating nchar(1),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")

    #complaints##
    c.execute('DROP TABLE if EXISTS complaints')
    c.execute("""CREATE TABLE complaints (
    user_id VARCHAR(9) not null,
    emp_id VARCHAR(5) not null,
    complaint text,
    date_posted [timestamp] timestamp,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    #compliments##
    c.execute('DROP TABLE if EXISTS compliments')
    c.execute("""CREATE TABLE compliments (
    user_id VARCHAR(9) PRIMARY KEY NOT NULL,
    emp_id VARCHAR(5) NOT NULL,
    date_posted [timestamp] timestamp,
    compliment text,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    #orders##
    c.execute('DROP TABLE if EXISTS orders')
    c.execute("""CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id VARCHAR(9) not null,
    chef_id VARCHAR(5) NOT NULL,
    menu_id nchar(5) not null,
    menu_Item varchar(20) not null,
    price decimal(5,2) not null,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (chef_id) REFERENCES chefs(chef_id)
    )""")

    #figuring out how autoincrement works.
    c.execute('INSERT INTO orders VALUES(NULL,"U0001","C0001","M0001","STEAK", "10.00")')
    #select_top5_ratings("U0001")


    ##chefs##chef rating will be average of all menu item ratings.
    c.execute('DROP TABLE if EXISTS chefs')
    c.execute("""CREATE TABLE chefs (
    chef_id VARCHAR(5) NOT NULL,
    emp_id VARCHAR(5) NOT NULL,
    chef_rating nchar(1),
    PRIMARY KEY (chef_id),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
    )""")

    ##delivery information##
    c.execute('DROP TABLE if EXISTS deliveryinfo')
    c.execute("""CREATE TABLE deliveryinfo (
    order_id INTEGER PRIMARY KEY,
    emp_id VARCHAR(5) not null,
    user_id VARCHAR(9) not null,
    user_fname varchar(20) not null,
    address varchar(40) not null,
    city varchar(20) not null,
    postal nchar(5) not null,
    cust_warning text,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""")

    ##menu/menu items##
    c.execute('DROP TABLE if EXISTS menus')
    c.execute("""CREATE TABLE menus (
    chef_id nchar(5) not null,
    menu_id nchar(5) not null,
    item_name varchar(50) not null,
    price decimal(5,2) not null,
    rating varchar(1),
    FOREIGN KEY (chef_id) REFERENCES chefs(chef_id)
    )""")


CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    email TEXT,
    password TEXT,
    role TEXT,
    amount_of_pluts DOUBLE
)

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    category_id INTEGER,
    price INTEGER,
    photo TEXT
)

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    status TEXT,
    address_id INTEGER
)


CREATE TABLE order_position (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    amount INTEGER
)

CREATE TABLE payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    amount DOUBLE,
    date DATE
)

CREATE TABLE address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    street TEXT,
    city TEXT,
    local_number INTEGER,
    user_id INTEGER
)

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
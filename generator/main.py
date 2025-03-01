from faker import Faker
from sqlalchemy import create_engine, text
import time

time.sleep(30)  # wait for mysql to start

with create_engine('mysql+pymysql://mysqluser:mysqlpw@mysql:3306/customers').connect() as cnx:
    cnx.execute(text(f"CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255))"))
    cnx.commit()
    fake = Faker()
    while True:
        name = fake.name()
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[1]
        email = fake.email()
        cnx.execute(text(f"INSERT INTO customers(first_name, last_name, email) VALUES ('{first_name}', '{last_name}', '{email}')"))
        cnx.commit()
        time.sleep(1)

import random

import os
import sys

# Add Parent folder into project path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database import get_db_connection

import mysql.connector

from faker import Faker

from faker import Faker
from Database import get_db_connection

from werkzeug.security import generate_password_hash

fake = Faker()

conn = get_db_connection()

cursor = conn.cursor()

for i in range(46):

    username = fake.user_name()

    email = fake.unique.email()

    password = generate_password_hash("123456")

    cursor.execute(

        """
        INSERT INTO users
        (username,email,password)
        VALUES(%s,%s,%s)
        """,

        (

            username,

            email,

            password

        )

    )

conn.commit()

cursor.close()

conn.close()

print("50 Dummy Users Created Successfully.")
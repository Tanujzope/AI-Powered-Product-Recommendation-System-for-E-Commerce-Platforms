import random

import os
import sys

# Add Parent folder into project path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
from Database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Get all user ids
cursor.execute("SELECT user_id FROM users")
users = [row[0] for row in cursor.fetchall()]

# Get all product ids
cursor.execute("SELECT product_id FROM products")
products = [row[0] for row in cursor.fetchall()]

interaction_types = ["view", "favorite"]

created = set()

while len(created) < 5000:

    user_id = random.choice(users)

    product_id = random.choice(products)

    interaction = random.choices(
        interaction_types,
        weights=[80, 20],
        k=1
    )[0]

    key = (user_id, product_id, interaction)

    if key not in created:

        created.add(key)

        cursor.execute(
            """
            INSERT INTO user_interactions
            (user_id, product_id, interaction_type)
            VALUES (%s,%s,%s)
            """,
            (user_id, product_id, interaction)
        )

conn.commit()

cursor.close()

conn.close()

print("5000 User Interactions Created Successfully!")
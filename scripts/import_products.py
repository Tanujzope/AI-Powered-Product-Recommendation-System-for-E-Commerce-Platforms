import pandas as pd
import mysql.connector

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ai_recommendation_db"
)

cursor = conn.cursor()

# Read CSV
df = pd.read_csv("../products.csv")

print(df.columns)

print(f"Total Products Found : {len(df)}")

# Optional: Delete old data to avoid duplicates
cursor.execute("DELETE FROM products")

# Insert Products

query = """
INSERT INTO products
(product_id, name, category, brand, price, description)
VALUES (%s,%s,%s,%s,%s,%s)
"""

for _, row in df.iterrows():

    cursor.execute(
        query,
        (
           (
    (
    int(row["product_id"]),
    row["name"],
    row["category"],
    row["brand"],
    float(row["price"]),
    row["description"]
)
)
        )
    )

conn.commit()

print("Products Imported Successfully!")

cursor.close()
conn.close()
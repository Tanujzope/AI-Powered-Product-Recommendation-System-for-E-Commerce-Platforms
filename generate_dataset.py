import pandas as pd
import random

categories = {
    "Electronics": [
        "Smartphone", "Laptop", "Earbuds", "Smart Watch", "Tablet",
        "Power Bank", "Speaker", "Monitor", "Keyboard", "Mouse"
    ],
    "Fashion": [
        "T-Shirt", "Shirt", "Jeans", "Jacket", "Shoes",
        "Sneakers", "Watch", "Cap", "Hoodie", "Sunglasses"
    ],
    "Books": [
        "Programming Book", "Novel", "Science Book", "History Book",
        "Math Book", "AI Book", "Business Book", "Biography",
        "Story Book", "Exam Guide"
    ],
    "Home Appliances": [
        "Refrigerator", "Washing Machine", "Microwave", "Mixer",
        "Vacuum Cleaner", "Air Purifier", "Water Heater",
        "Ceiling Fan", "Iron", "Air Cooler"
    ],
    "Sports": [
        "Cricket Bat", "Football", "Basketball", "Tennis Racket",
        "Gym Gloves", "Yoga Mat", "Dumbbells", "Sports Shoes",
        "Helmet", "Skipping Rope"
    ],
    "Beauty": [
        "Face Wash", "Shampoo", "Perfume", "Body Lotion",
        "Hair Oil", "Lip Balm", "Sunscreen", "Face Cream",
        "Beard Oil", "Deodorant"
    ]
}

brands = [
    "Apple", "Samsung", "HP", "Dell", "Lenovo",
    "Boat", "Nike", "Adidas", "Puma", "Sony",
    "LG", "Philips", "Loreal", "Nivea", "Himalaya",
    "Mi", "OnePlus", "Realme", "Acer", "Asus"
]

products = []

product_id = 1

for _ in range(500):
    category = random.choice(list(categories.keys()))
    product_name = random.choice(categories[category])
    brand = random.choice(brands)

    full_name = f"{brand} {product_name}"

    price = random.randint(500, 100000)

    description = f"{full_name} in {category} category with premium quality features."

    products.append([
        product_id,
        full_name,
        category,
        brand,
        price,
        description
    ])

    product_id += 1

df = pd.DataFrame(
    products,
    columns=[
        "product_id",
        "name",
        "category",
        "brand",
        "price",
        "description"
    ]
)

df.to_csv("products.csv", index=False)

print("products.csv created successfully with 500 products!")
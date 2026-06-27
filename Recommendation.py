import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from Database import get_db_connection

conn = get_db_connection()

products = pd.read_sql("SELECT * FROM products", conn)

conn.close()

products["combined_features"] = (

    products["name"].fillna("") + " " +

    products["brand"].fillna("") + " " +

    products["category"].fillna("") + " " +

    products["description"].fillna("")

)

vectorizer = TfidfVectorizer(stop_words="english")

feature_vectors = vectorizer.fit_transform(
    products["combined_features"]
)

similarity = cosine_similarity(feature_vectors)

def get_recommendations(product_id, top_n=5):

    # Check whether product exists
    if product_id not in products["product_id"].values:
        return pd.DataFrame()

    # Get DataFrame index of the selected product
    product_index = products[products["product_id"] == product_id].index[0]

    # Get similarity scores
    similarity_scores = list(enumerate(similarity[product_index]))

    # Sort by similarity (Highest First)
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected product itself
    similarity_scores = similarity_scores[1:top_n + 1]

    # Get recommended product indices
    recommended_indices = [item[0] for item in similarity_scores]

    # Return recommended products
    return products.iloc[recommended_indices]


# print(products.head())
# print(similarity.shape)

# recommended = get_recommendations(1)

# print(recommended[[
#     "product_id",
#     "name",
#     "brand",
#     "category",
#     "price"
# ]])
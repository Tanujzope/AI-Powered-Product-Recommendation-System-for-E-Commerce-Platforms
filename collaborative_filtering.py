import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from Database import get_db_connection

conn = get_db_connection()

query = """
SELECT
    user_id,
    product_id
FROM user_interactions
"""

interactions = pd.read_sql(query, conn)

conn.close()

user_product_matrix = interactions.pivot_table(
    index="user_id",
    columns="product_id",
    aggfunc=len,
    fill_value=0
)

user_product_matrix = (user_product_matrix > 0).astype(int)

user_similarity = cosine_similarity(user_product_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_product_matrix.index,
    columns=user_product_matrix.index
)

def get_similar_users(user_id, top_n=5):

    if user_id not in user_similarity_df.index:
        return []

    similar_users = user_similarity_df[user_id].sort_values(
        ascending=False
    )

    similar_users = similar_users.drop(user_id)

    return similar_users.head(top_n)


def get_collaborative_recommendations(user_id, top_n=5):

    # Check if user exists
    if user_id not in user_product_matrix.index:
        return pd.DataFrame()

    # Get top similar users
    similar_users = get_similar_users(user_id)

    # Products already interacted by current user
    current_user_products = set(
        user_product_matrix.loc[user_id][
            user_product_matrix.loc[user_id] == 1
        ].index
    )

    recommended_products = set()

    # Loop through similar users
    for similar_user in similar_users.index:

        similar_user_products = set(
            user_product_matrix.loc[similar_user][
                user_product_matrix.loc[similar_user] == 1
            ].index
        )

        new_products = similar_user_products - current_user_products

        recommended_products.update(new_products)

        if len(recommended_products) >= top_n:
            break

    if not recommended_products:
        return pd.DataFrame()

    conn = get_db_connection()

    placeholders = ",".join(["%s"] * len(recommended_products))

    query = f"""
    SELECT *
    FROM products
    WHERE product_id IN ({placeholders})
    LIMIT {top_n}
    """

    products = pd.read_sql(
        query,
        conn,
        params=list(recommended_products)
    )

    conn.close()

    return products

# print(user_product_matrix.head())

# print()

# print(user_similarity_df.head())

# print()

# print(get_similar_users(1))

print()

recommended = get_collaborative_recommendations(1)

print(recommended[
    [
        "product_id",
        "name",
        "brand",
        "category"
    ]
])
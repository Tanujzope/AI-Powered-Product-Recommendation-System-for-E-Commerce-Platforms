import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ai_recommendation_db"
    )
    return connection


# if __name__ == "__main__":
#     try:
#         conn = get_db_connection()
#         print("Database connected successfully!")
#         conn.close()
#     except Exception as e:
#         print("Error:", e)
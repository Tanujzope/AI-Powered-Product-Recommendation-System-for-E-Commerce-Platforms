from flask import Flask, render_template, request
from Database import get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO users(username,email,password)
        VALUES(%s,%s,%s)
        """

        cursor.execute(query, (username, email, password))

        conn.commit()

        cursor.close()

        conn.close()

        return render_template("success.html")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from Database import get_db_connection

app = Flask(__name__)
app.secret_key = "mca_project_2026"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            flash("Email already registered!", "danger")

            cursor.close()
            conn.close()

            return render_template("register.html")

        cursor.execute(
            """
            INSERT INTO users(username,email,password)
            VALUES(%s,%s,%s)
            """,
            (username, email, hashed_password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return render_template(
            "success.html",
            username=username
        )

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(

            "SELECT * FROM users WHERE email=%s",

            (email,)

        )

        user = cursor.fetchone()

        cursor.close()

        conn.close()

        if user:

            if check_password_hash(user["password"], password):

                session["user_id"] = user["user_id"]

                session["username"] = user["username"]

                flash("Login Successful!", "success")

                return redirect(url_for("dashboard"))

            else:

                flash("Invalid Password!", "danger")

        else:

            flash("Email not found!", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash("Please Login First.", "warning")

        return redirect(url_for("login"))

    return render_template(

        "dashboard.html",

        username=session["username"]

    )
    
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("login"))

@app.route("/products")
def products():

    if "user_id" not in session:

        flash("Please Login First.", "warning")

        return redirect(url_for("login"))

    return "<h1>Products Page Coming in Step 7</h1>"


if __name__ == "__main__":
    app.run(debug=True)
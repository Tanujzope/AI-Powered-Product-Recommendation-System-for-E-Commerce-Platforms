from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from Database import get_db_connection
from Recommendation import get_recommendations
from collaborative_filtering import get_collaborative_recommendations

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
    
@app.route("/recommendations")
def recommendations():

    if "user_id" not in session:

        flash("Please login first!", "warning")

        return redirect(url_for("login"))

    user_id = session["user_id"]

    recommended = get_collaborative_recommendations(user_id)

    return render_template(

        "recommendations.html",

        products=recommended.to_dict(orient="records")

    )
    
@app.route("/feedback", methods=["POST"])
def feedback():

    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    product_id = request.form["product_id"]
    feedback_type = request.form["feedback_type"]

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    # Check if feedback already exists
    cursor.execute(
        """
        SELECT feedback_id, feedback_type
        FROM feedback
        WHERE user_id = %s AND product_id = %s
        """,
        (user_id, product_id)
    )

    existing_feedback = cursor.fetchone()

    if existing_feedback:

        feedback_id = existing_feedback[0]
        old_feedback = existing_feedback[1]

        # Same feedback already exists
        if old_feedback == feedback_type:

            cursor.close()
            conn.close()

            flash(
                "You have already submitted this feedback.",
                "warning"
            )

            return redirect(url_for("recommendations"))

        # Update feedback
        cursor.execute(
            """
            UPDATE feedback
            SET feedback_type = %s
            WHERE feedback_id = %s
            """,
            (feedback_type, feedback_id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Your feedback has been updated.",
            "success"
        )

        return redirect(url_for("recommendations"))

    # Insert new feedback
    cursor.execute(
        """
        INSERT INTO feedback
        (user_id, product_id, feedback_type)
        VALUES (%s, %s, %s)
        """,
        (user_id, product_id, feedback_type)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Thank you for your feedback!",
        "success"
    )

    return redirect(url_for("recommendations"))
    
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("login"))

@app.route("/products")
def products():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def product_details(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Product Details
    cursor.execute(
        "SELECT * FROM products WHERE product_id=%s",
        (product_id,)
    )

    product = cursor.fetchone()

    # Save Interaction
    cursor.execute(
        """
        INSERT INTO user_interactions
        (user_id, product_id, interaction_type)
        VALUES(%s,%s,%s)
        """,
        (
            session["user_id"],
            product_id,
            "view"
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    recommended_products = get_recommendations(product_id)

    return render_template(
    "product_details.html",
    product=product,
    recommended_products=recommended_products.to_dict(orient="records")
)
    
@app.route("/favorite/<int:product_id>")
def favorite_product(product_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_interactions
        (user_id, product_id, interaction_type)
        VALUES (%s,%s,%s)
        """,
        (
            session["user_id"],
            product_id,
            "favorite"
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash("Product added to Favorites!", "success")

    return redirect(url_for("product_details", product_id=product_id))

if __name__ == "__main__":
    app.run(debug=True)
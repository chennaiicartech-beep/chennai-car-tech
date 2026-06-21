from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db, User

auth = Blueprint(
    "auth",
    __name__
)

# ======================
# LOGIN
# ======================

@auth.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect("/admin")

            return redirect("/dashboard")

    return render_template("login.html")
# ======================
# LOGOUT
# ======================

@auth.route("/logout")
def logout():

    session.clear()
    return redirect("/")

#=======================
#CUSTOMER REGISTRATION
#=======================
@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="customer"
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")
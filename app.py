from flask import Flask, render_template, request, redirect, session, flash
import webbrowser
import os
from utils.core import recent_transactions, get_user_by_phone, get_all_users
from utils.filters import filter_transactions, filter_summary
from utils.viewers import view_transactions, view_passbook, view_summary
from utils.transactions import new_transaction, delete_transaction
from utils.records_update import new_person, update_records, delete_person

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ---------------- HOME / LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone    = request.form["phone"]
        password = request.form["password"]

        user = get_user_by_phone(phone)

        if user and user["password"] == password:
            session["phone"]   = phone
            session["role"]    = user["role"]
            session["user_id"] = user["id"]

            if user["role"] == "admin":
                return redirect("/admin")
            elif user["role"] == "analyst":
                return redirect("/analyst")
            else:
                return redirect("/user")

        flash("Invalid phone number or password.", "danger")
        return render_template("login.html")

    return render_template("login.html")


# ---------------- USER DASHBOARD ----------------
@app.route("/user")
def user_dashboard():
    if "user_id" not in session:
        return redirect("/")

    uid  = session["user_id"]
    user = get_user_by_phone(session["phone"])

    return render_template(
        "user.html",
        user=user,
        transactions=view_transactions(uid),
        passbook=view_passbook(uid),
        summary=view_summary(uid),
        recent_txns=recent_transactions(uid, n=5)
    )


# ---------------- ADD TRANSACTION ----------------
@app.route("/add_transaction", methods=["POST"])
def add_txn():
    if "user_id" not in session:
        return redirect("/")

    uid      = session["user_id"]
    category = request.form["Category"]
    amount   = float(request.form["Amount"])
    notes    = request.form.get("Notes", "")
    txn_type = request.form["Type"]
    date     = request.form["Date"]

    new_transaction(uid, category, amount, notes, txn_type, date)
    flash("Transaction added successfully!", "success")
    return redirect("/user")


# ---------------- DELETE TRANSACTION ----------------
@app.route("/delete_transaction/<int:txn_id>")
def delete_txn(txn_id):
    if "user_id" not in session:
        return redirect("/")

    deleted = delete_transaction(session["user_id"], txn_id)
    if deleted:
        flash("Transaction deleted successfully!", "success")
    else:
        flash("Transaction not found.", "danger")
    return redirect("/user")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/")
    return render_template("admin.html", users=get_all_users())


@app.route("/admin/update", methods=["POST"])
def admin_update():
    if session.get("role") != "admin":
        return redirect("/")

    phone = request.form["phone"]
    field = request.form["field"]
    value = request.form["value"]

    user = get_user_by_phone(phone)

    if user:
        updated = update_records(field, value, user["id"])
        if updated:
            flash("Person updated successfully!", "success")
        else:
            flash(f"Invalid field '{field}' — no update made.", "danger")
    else:
        flash("Person not found!", "danger")

    return redirect("/admin")


@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    if session.get("role") != "admin":
        return redirect("/")

    name  = request.form["name"]
    dob   = request.form["dob"]
    phone = request.form["phone"]

    deleted = delete_person(name, dob, phone)
    if deleted:
        flash("Person deleted successfully!", "success")
    else:
        flash("Name, DOB or phone did not match any record.", "danger")

    return redirect("/admin")


@app.route("/admin/create", methods=["POST"])
def admin_create():
    if session.get("role") != "admin":
        return redirect("/")

    result = new_person(
        request.form["name"],
        request.form["dob"],
        request.form["phone"],
        request.form["password"]
    )

    if result == "User already exists":
        flash("A user with that phone number already exists.", "danger")
    else:
        flash("Record created successfully!", "success")

    return redirect("/admin")


# ---------------- ANALYST ----------------
@app.route("/analyst")
def analyst():
    if session.get("role") != "analyst":
        return redirect("/")
    return render_template("analyst.html", users=get_all_users())


@app.route("/filter", methods=["POST"])
def filter_data():
    if session.get("role") != "analyst":
        return redirect("/")

    phone = request.form.get("phone", "").strip()

    if not phone:
        flash("Please enter a phone number to filter.", "danger")
        return render_template("analyst.html", users=get_all_users())

    user = get_user_by_phone(phone)

    if not user:
        flash("No user found with that phone number.", "danger")
        return render_template("analyst.html", users=get_all_users())

    filtered = filter_transactions(
        user["id"],
        request.form.get("start_date"),
        request.form.get("end_date"),
        request.form.get("category"),
        request.form.get("type")
    )

    summary = filter_summary(filtered)

    return render_template("analyst.html", filtered=filtered, summary=summary, users=get_all_users())


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    webbrowser.open_new("http://127.0.0.1:5000/")
    app.run(debug=True, use_reloader=False)

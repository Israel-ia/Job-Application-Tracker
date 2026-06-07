from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    
    search_term = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    sort_order = request.args.get("sort", "")
    
    order_clause = ""

    if sort_order == "newest":
        order_clause = " ORDER BY date_applied DESC"

    elif sort_order == "oldest":
        order_clause = " ORDER BY date_applied ASC"

    connection = sqlite3.connect("applications.db")

    cursor = connection.cursor()

    if search_term and status_filter:

        cursor.execute(
            """
            SELECT * FROM applications
            WHERE company LIKE ?
            AND status = ?
            """ + order_clause,
            (f"%{search_term}%", status_filter)
        )

    elif search_term:

        cursor.execute(
            """
            SELECT * FROM applications
            WHERE company LIKE ?
            """ + order_clause,
            (f"%{search_term}%",)
        )

    elif status_filter:

        cursor.execute(
            """
            SELECT * FROM applications
            WHERE status = ?
            """ + order_clause,
            (status_filter,)
        )

    else:

        cursor.execute(
            "SELECT * FROM applications" + order_clause
        )

    applications = cursor.fetchall()
        
    total_applications = len(applications)

    applied_count = sum(
        1 for application in applications
        if application[3] == "Applied"
    )

    interview_count = sum(
        1 for application in applications
        if application[3] == "Interview"
    )

    offer_count = sum(
        1 for application in applications
        if application[3] == "Offer"
    )

    rejected_count = sum(
        1 for application in applications
        if application[3] == "Rejected"
    )

    connection.close()

    return render_template(
        "index.html",
        applications=applications,
        total_applications=total_applications,
        applied_count=applied_count,
        interview_count=interview_count,
        offer_count=offer_count,
        rejected_count=rejected_count,  
        search_term=search_term,
        status_filter=status_filter,
        sort_order=sort_order
    )   

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]
        notes = request.form["notes"]

        connection = sqlite3.connect("applications.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO applications
            (company, position, status, date_applied, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                company,
                position,
                status,
                date_applied,
                notes
            )
        )
        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("add.html")
@app.route("/delete/<int:id>")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):

    if request.method == "POST":

        status = request.form["status"]

        connection = sqlite3.connect("applications.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, id)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("edit.html")
def delete_application(id):

    connection = sqlite3.connect("applications.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)
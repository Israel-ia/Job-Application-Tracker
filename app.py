from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():

    connection = sqlite3.connect("applications.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM applications")

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
        rejected_count=rejected_count
    )   

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]

        connection = sqlite3.connect("applications.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO applications
            (company, position, status, date_applied)
            VALUES (?, ?, ?, ?)
            """,
            (company, position, status, date_applied)
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
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():

    connection = sqlite3.connect("applications.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM applications")

    applications = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        applications=applications
    )

@app.route("/add", methods=["GET", "POST"])
def add_application():

    if request.method == "POST":

        company = request.form["company"]
        position = request.form["position"]
        status = request.form["status"]

        connection = sqlite3.connect("applications.db")

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO applications
            (company, position, status)
            VALUES (?, ?, ?)
            """,
            (company, position, status)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
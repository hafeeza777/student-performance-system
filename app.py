from flask import Flask, render_template, request, redirect, url_for, session, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = "student_secret_key"


# ---------------- HOME ----------------
@app.route("/")
def home():
     return redirect(url_for("login"))


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin":
            return redirect(url_for("student_form"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- STUDENT FORM ----------------
@app.route("/student_form", methods=["GET", "POST"])
def student_form():
    if request.method == "POST":

        name = request.form.get("name")
        regno = request.form.get("regno")

        subjects = [
            request.form.get("subject1"),
            request.form.get("subject2"),
            request.form.get("subject3"),
            request.form.get("subject4"),
            request.form.get("subject5")
        ]

        marks = [
            int(request.form.get("mark1")),
            int(request.form.get("mark2")),
            int(request.form.get("mark3")),
            int(request.form.get("mark4")),
            int(request.form.get("mark5"))
        ]

        total = sum(marks)
        percentage = round(total / 5, 2)
        maximum = max(marks)
        minimum = min(marks)

        result = "PASS" if all(m >= 40 for m in marks) else "FAIL"

        session["name"] = name
        session["regno"] = regno
        session["subjects"] = subjects
        session["marks"] = marks
        session["total"] = total
        session["percentage"] = percentage
        session["maximum"] = maximum
        session["minimum"] = minimum
        session["result"] = result

        return redirect(url_for("result_page"))

    return render_template("student_form.html")


# ---------------- RESULT ----------------
@app.route("/result")
def result_page():
    if not session.get("subjects"):
        return redirect(url_for("student_form"))

    return render_template(
        "result.html",
        name=session.get("name"),
        regno=session.get("regno"),
        subjects=session.get("subjects"),
        marks=session.get("marks"),
        total=session.get("total"),
        percentage=session.get("percentage"),
        maximum=session.get("maximum"),
        minimum=session.get("minimum"),
        result=session.get("result")
    )


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("subjects"):
        return redirect(url_for("student_form"))

    if session.get("result") == "FAIL":
        return redirect(url_for("resource"))

    return render_template(
        "dashboard.html",
        name=session.get("name"),
        total=session.get("total"),
        percentage=session.get("percentage"),
        maximum=session.get("maximum"),
        minimum=session.get("minimum"),
        result=session.get("result"),
        marks=session.get("marks"),
        subjects=session.get("subjects")
    )


# ---------------- CERTIFICATE PAGE ----------------
@app.route("/certificate")
def certificate():
    if not session.get("subjects"):
        return redirect(url_for("student_form"))

    if session.get("result") == "FAIL":
        return redirect(url_for("resource"))

    return render_template(
        "certificate.html",
        name=session.get("name"),
        regno=session.get("regno"),
        percentage=session.get("percentage"),
        issue_date=datetime.today().strftime("%d %B %Y")
    )


# ---------------- DOWNLOAD CERTIFICATE (PDF) ----------------
@app.route("/download_certificate")
def download_certificate():

    if not session.get("subjects"):
        return redirect(url_for("student_form"))

    if session.get("result") == "FAIL":
        return redirect(url_for("resource"))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "CERTIFICATE OF ACHIEVEMENT")

    # Student Details
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 200, f"Name: {session.get('name')}")
    c.drawString(100, height - 240, f"Register No: {session.get('regno')}")
    c.drawString(100, height - 280, f"Percentage: {session.get('percentage')}%")

    # Date
    current_date = datetime.now().strftime("%d-%m-%Y")
    c.drawString(100, height - 320, f"Date: {current_date}")

    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Certificate.pdf",
        mimetype="application/pdf"
    )


# ---------------- RESOURCE ----------------
@app.route("/resource")
def resource():
    if not session.get("subjects"):
        return redirect(url_for("student_form"))

    return render_template(
        "resource.html",
        subjects=session.get("subjects")
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()

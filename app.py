from flask import Flask, render_template, request, redirect, url_for, session
import random
import smtplib

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Dane użytkowników
users = {
    "J_Burza": "J_Burza123",
    "S_Burza": "S_Burza123",
    "N_Trzopek": "N_Trzopek123",
    "W_Trzopek": "W_Trzopek123",
    "K_Burza": "K_Burza123",
    "M_Burza": "M_Burza123",
    "S_Burza2": "S_Burza2123",
    "H_Burza": "H_Burza123",
    "Admin": "Pogotowie112@!"
}

pairs = {}
drawn = []

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username in users and users[username] == password:
        session["username"] = username
        return redirect(url_for("dashboard"))
    return "Niepoprawne dane logowania. Spróbuj ponownie!"

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    if not username:
        return redirect(url_for("index"))
    if username == "Admin":
        return render_template("admin.html", pairs=pairs)
    return render_template("dashboard.html", username=username)

@app.route("/draw", methods=["POST"])
def draw():
    username = session.get("username")
    if username not in pairs:
        available = [user for user in users if user != username and user not in drawn and user != "Admin"]
        if not available:
            return "Brak dostępnych osób do wylosowania!"
        choice = random.choice(available)
        pairs[username] = choice
        drawn.append(choice)
        email = request.form["email"]
        send_email(email, choice)
    return f"Twój wylosowany to: {pairs[username]}"

def send_email(recipient, draw):
    sender_email = "losowanie.osob@gmail.com"  # Zmień na swój e-mail
    sender_password = "twoje_haslo"  # Wprowadź hasło
    subject = "Twój wylosowany na Święta!"
    message = f"Twój wylosowany to: {draw}."

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, f"Subject: {subject}\n\n{message}")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

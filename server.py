from flask import Flask, request, jsonify, redirect, session
import json, os, datetime

app = Flask(__name__)
app.secret_key = "darksecret"

DB_FILE = "keys.json"

if os.path.exists(DB_FILE):
    with open(DB_FILE) as f:
        VALID_KEYS = json.load(f)
else:
    VALID_KEYS = {}

ADMIN_USER = "admin"
ADMIN_PASS = "dark123"

@app.route("/check")
def check():
    key = request.args.get("key")

    if key in VALID_KEYS:
        exp = VALID_KEYS[key]["exp"]
        now = datetime.datetime.now().strftime("%Y-%m-%d")

        if now <= exp:
            return jsonify({"status": "valid", "exp": exp})
        else:
            return jsonify({"status": "expired"})

    return jsonify({"status": "invalid"})

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == ADMIN_USER and request.form["pass"] == ADMIN_PASS:
            session["login"] = True
            return redirect("/panel")

    return """
    <h2>ADMIN LOGIN</h2>
    <form method="POST">
    <input name="user">
    <input name="pass" type="password">
    <button>Login</button>
    </form>
    """

@app.route("/panel", methods=["GET","POST"])
def panel():
    if not session.get("login"):
        return redirect("/")

    if request.method == "POST":
        key = request.form.get("key")
        days = int(request.form.get("days", 30))

        exp = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")

        VALID_KEYS[key] = {"exp": exp}

        with open(DB_FILE, "w") as f:
            json.dump(VALID_KEYS, f)

    html = "<h2>LICENSE PANEL</h2><form method=POST>"
    html += "Key:<input name=key><br>Days:<input name=days value=30><br>"
    html += "<button>Add</button></form><hr>"

    for k,v in VALID_KEYS.items():
        html += f"{k} | Exp: {v['exp']}<br>"

    return html

app.run(host="0.0.0.0", port=5000)

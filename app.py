from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    # Visitor counter
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")
    result = db.query("SELECT COUNT(*) FROM visits")
    count = result[0]
    workouts = db.query("SELECT * FROM logs")
    return render_template("index.html", workouts=workouts)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    try:
      sql = "SELECT password_hash FROM users WHERE username = ?"
      password_hash = db.query(sql, [username])[0][0]
    except:
      return "ERROR: no users found"
    
    if check_password_hash(password_hash, password):
        session["username"] = username
        sql = "SELECT id FROM users WHERE username = ?"
        user_id = db.query(sql, [username])[0][0]
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "ERROR: wrong username or password"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
  return render_template("register.html")

@app.route("/create_account", methods=["POST"])
def create_account():
  username = request.form["username"]
  password1 = request.form["password1"]
  password2 = request.form["password2"]
  if password1 != password2:
     return "ERROR: passwords do not match"
  password_hash = generate_password_hash(password1)

  try:
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
  except:
     return "ERROR: there is already a user with this username"
  
  return "Account created"

@app.route("/log_form")
def log_form():
   types = db.query("SELECT workout_type FROM workout_types")
   return render_template("log_form.html", types=types)

@app.route("/create_log", methods=["POST"])
def create_log():
   title = request.form["title"]
   content = request.form["content"]
   type = request.form["type"]
   sql = "INSERT INTO logs (user_id, content, posted_at, workout_type, title) VALUES (?, ?, datetime('now'), ?, ?)"
   db.execute(sql, [session["user_id"], content, type, title])
   return redirect("/")

@app.route("/new_type")
def new_type():
   return render_template("new_type.html")

@app.route("/create_type", methods=["POST"])
def create_type():
   workout_type = request.form["workout_type"]
   db.execute("INSERT INTO workout_types (workout_type) VALUES (?)", [workout_type])
   return redirect("/log_form")

@app.route("/workouts/<int:workout_id>")
def show_workout(workout_id):
   sql = "SELECT w.*, u.username FROM logs w, users u WHERE w.id = ? AND u.id = w.user_id"
   workout = db.query(sql, [workout_id])[0]
   return render_template("workout.html", workout=workout)
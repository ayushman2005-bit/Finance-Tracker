from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ------------------ MODELS ------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()

        if not user:
            error = "Username not found"
        elif user.password != request.form['password']:
            error = "Password is Incorrect"
        else:
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    expenses = (
        Expense.query
        .filter_by(user_id=current_user.id)
        .order_by(Expense.date.desc(), Expense.id.desc())
        .all()
    )
    total = sum([e.amount for e in expenses])
    return render_template("dashboard.html", expenses=expenses, total=total)

@app.route("/add", methods=["POST"])
@login_required
def add():
    date_str = request.form.get('date')
    expense_date = None
    if date_str:
        try:
            expense_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            expense_date = None

    category = (request.form.get('category') or '').strip()
    if not category:
        category = "Uncategorized"

    expense = Expense(
        title=request.form['title'],
        amount=float(request.form['amount']),
        category=category,
        date=expense_date or datetime.datetime.now(),
        user_id=current_user.id,
    )
    db.session.add(expense)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    exp = Expense.query.get(id)
    db.session.delete(exp)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

# ------------------ RUN ------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

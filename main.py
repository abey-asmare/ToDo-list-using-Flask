from flask import Flask, redirect, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import Register, Login, Todo,CheckBox
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 't 13!@#asdfasfq#$asdfvzcxbgfjfjfgyue%^#'
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email= db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    todo_list = db.relationship('TodoList', back_populates='author')

class TodoList(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    todo_title = db.Column(db.String(100), nullable=False)
    todo_state = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='todo_list')

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/todo-lists", methods=["GET", "POST"])
@login_required
def todo_lists():
    forms = Todo()
    check_form = CheckBox()
    if forms.validate_on_submit():
        new_todo = TodoList(
            todo_title=forms.todo.data,
            todo_state=False,
            author=current_user,
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo_lists'))
    return render_template('todo_list.html', forms=forms, check_form = check_form)

@app.route("/login", methods=["GET", "POST"])
def login():
    forms = Login()
    if forms.validate_on_submit():
        email = forms.email.data
        password = forms.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash(f'Welcome back, {user.name}')
            else:
                flash('Invalid credentials')
                return redirect(url_for('login'))
        else:
            flash('Account doesn\'t exist, please register instead')
            return redirect(url_for('register'))
        return redirect(url_for('todo_lists'))
    return render_template("login.html", forms=forms)

@app.route("/register", methods=["GET", "POST"])
def register():
    forms = Register()
    if forms.validate_on_submit():
        email = forms.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Account already exists. Please login instead.")
            return redirect(url_for('login'))
        new_user = User(
            name=forms.name.data,
            email=forms.email.data,
            password=generate_password_hash(forms.password.data, 'pbkdf2:sha256', salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        if user is not None and user.is_active:
            login_user(user)
            print(user.email)
            print(user.password)
        else:
            return redirect(url_for('login'))
        return redirect(url_for('todo_lists'))
    return render_template("register.html", forms=forms)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/edit/<int:todo_id>", methods = ["GET", "POST"])
@login_required
def edit(todo_id):
    todo_item = TodoList.query.get(todo_id)
    forms = Todo(
                 todo=todo_item.todo_title
                 )
    if forms.validate_on_submit():
        todo_item.todo_title = forms.todo.data
        db.session.commit()


        return redirect(url_for('todo_lists'))
    return render_template('edit.html', forms = forms)

@app.route("/delete/<int:todo_id>")
@login_required
def delete(todo_id):
    todo_item = TodoList.query.get(todo_id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for('todo_lists'))

@app.route("/update-state/<int:todo_id>", methods = ["GET","POST"])
@login_required
def update_state(todo_id):
        todo_item = TodoList.query.get(todo_id)
        todo_item.todo_state = not todo_item.todo_state
        db.session.commit()

        return redirect(url_for('todo_lists'))

if __name__ == "__main__":
    app.run(debug=True)


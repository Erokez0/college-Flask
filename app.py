from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Post, User
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__, template_folder='static')
app.config['SECRET_KEY'] = 'very very secret key blah blah blah'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)
if __name__ == "__main__":
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.get('/')
    def get_root():
        posts = Post.query.order_by('created_at').all()
        return render_template("main.html", posts=posts)

    @app.get('/create')
    @login_required
    def get_create():
        return render_template("create.html")

    @app.get('/login')
    def get_login():
        return render_template("login.html")

    @app.get('/signup')
    def get_signup():
        return render_template("signup.html")

    @app.get('/logout')
    def post_logout():
        logout_user()
        return redirect(url_for('get_login'))

    @app.post('/create')
    def post_create():
        title = request.form.get('title')
        content = request.form.get('content')

        user_id = current_user.id
        post = Post(title=title, content=content, author_id=user_id)

        db.session.add(post)
        db.session.commit()
        return redirect('/')

    @app.post('/login')
    def post_login():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Неправильный ник или пароль")
            return redirect(url_for('get_login'))
        login_user(user)
        return redirect('/')

    @app.post('/signup')
    def post_signup():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash(f"Никнейм занят")
            return redirect(url_for('post_login'))

        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('post_login'))


    app.run(debug=True)
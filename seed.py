import datetime
from models import User, Post, db
from flask import  Flask

if __name__  == '__main__':
    app = Flask(__name__, template_folder='static')
    app.config['SECRET_KEY'] = 'very very secret key blah blah blah'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        user1 = User(username="Erokez", password="123456")
        user2 = User(username="test", password="pbkdf2:sha256:1000000$6NgGfReHobdtGMPj$dcc31f91f57d49b403508a96cdd34620a8072e9ccb5c8216d8d6a5f0c7ad9ab6'")
        db.session.add_all([user1, user2])
        post1 = Post(
            title="WHY DOES SH#TPOST EXIST?",
            author_id=1,
            content="""
            The idea of this stuff came to me when I was thinking about the checkpoint of "python on web" and rigth after that I had to do it.
            
            The worst forum there is.
            
            
            Just sh#itposting.
            """,
            created_at=datetime.datetime.now()
        )

        db.session.add_all([post1])
        db.session.commit()
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from portfolio import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_image = db.Column(db.String, nullable=False, default='default.jpg')
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    skills = db.Column(db.String)
    bio = db.Column(db.String)
    resume = db.Column(db.String)
    theme_color = db.Column(db.String, default="red")
    text_color = db.Column(db.String, default="white")
    background1 = db.Column(db.String, default="default1.png")
    background2 = db.Column(db.String, default="default2.png")
    background3 = db.Column(db.String, default="default3.png")
    jobs = db.relationship('Job', backref='employee', lazy=True)
    achievements = db.relationship('Achievement', backref='winner', lazy=True)
    projects = db.relationship('Project', backref='creator', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    role = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    volunteer = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Job('{self.company_name}', '{self.category}', '{self.employee}')"

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Achievement('{self.name}', '{self.category}', '{self.winner}')"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Project('{self.name}', '{self.year}', '{self.creator}')"
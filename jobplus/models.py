from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow)

class User(Base, UserMixin):
    __tablename__ = "user"  
    ROLE_USER = 10 
    ROLE_STAFF = 20  
    ROLE_ADMIN = 30 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), unique=True)  
    email = db.Column(db.String(100))
    _password = db.Column('password',db.String(100)) 
    role = db.Column(db.SmallInteger, default=ROLE_USER) 
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  
    user_company_info = db.relationship('Company', backref='user') 
    user_user_info = db.relationship('Personal', backref='user')  

    def __repr__(self):
        return "<User %r>" % self.name


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)


    def check_password(self, password):
        return check_password_hash(self._password, password)


        



class Personal(Base):
    __tablename__ = "personal"  
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            index=True,unique=True)
    name = db.Column(db.String(20))  
    phone = db.Column(db.String(11))
    jobyear = db.Column(db.Integer)  
    resume = db.Column(db.String(255)) 
    personal_jobwanted = db.relationship('JobWanted', backref='personal')

    def __repr__(self):
        return "<Personal %r>" % self.name



class Company(Base):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    name = db.Column(db.String(100), unique=True)  
    address = db.Column(db.String(100)) 
    phone = db.Column(db.String(11)) 
    logo = db.Column(db.String(255))  
    summary = db.Column(db.Text)  
    field = db.Column(db.String(64)) 
    financing = db.Column(db.String(64)) 
    company_job = db.relationship('Job', backref='company')

    def __repr__(self):
        return "<Company %r>" % self.name



class Job(Base):
    __tablename__ = "job"  
    id = db.Column(db.Integer, primary_key=True)  
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  
    name = db.Column(db.String(100))  
    min_pay = db.Column(db.Integer)
    max_pay = db.Column(db.Integer) 
    address = db.Column(db.String(100))
    label = db.Column(db.String(255))
    jobyear = db.Column(db.String(20))  
    education = db.Column(db.String(20))  
    description = db.Column(db.Text)
    job_JobWanted = db.relationship('JobWanted', backref='job')

    def __repr__(self):
        return "<Job %r>" % self.id

class JobWanted(Base):
    __tablename__ = 'jobwanted' 
    id = db.Column(db.Integer, primary_key=True)  
    personal_id = db.Column(db.Integer, db.ForeignKey('personal.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  

    def __repr__(self):
        return "<JobWanted %r>" % self.id

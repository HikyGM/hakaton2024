import datetime
from flask_login import UserMixin
from sqlalchemy import orm, Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    about = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_date = Column(String, default=datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
    total_score = Column(Integer, default=0)
    source_image = Column(String, nullable=True, default='default.png')

    score = orm.relationship("Score", back_populates='user')

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'email': self.email,
        }

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

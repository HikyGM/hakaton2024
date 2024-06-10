from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, ForeignKey


class Score(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'score'

    id = Column(Integer, primary_key=True, autoincrement=True)
    level_rate = Column(Integer, nullable=True, default=0)
    level_all = Column(Integer, nullable=True, default=0)
    level_last_date = Column(String, nullable=True, default="Никогда")
    level_url_image = Column(String, nullable=True)
    level_answer = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = orm.relationship('User')

    difficulty_levels_id = Column(Integer, ForeignKey("difficulty_levels.id"))
    difficulty_levels = orm.relationship('Difficulty_levels')



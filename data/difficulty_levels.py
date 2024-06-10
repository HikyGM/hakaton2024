from .db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String


class Difficulty_levels(SqlAlchemyBase):
    __tablename__ = 'difficulty_levels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    difficulty_levels_title = Column(String)
    difficulty_levels_complexity = Column(Integer)
    difficulty_levels_type = Column(String)
    difficulty_levels_weight = Column(Integer)

    score = orm.relationship("Score", back_populates='difficulty_levels')


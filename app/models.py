"""
Модуль описывает модели данных в БД.

Содержит таблицы для описания ингредиентов,
рецептов и ассоциативная таблица для связи
M2M рецептов и ингредиентов.
"""

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# Ассоциативная таблица для связи
# M2M рецептов и ингредиентов.
association_table = Table(
    "association_table",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("component_id", ForeignKey("components.id"), primary_key=True),
)


class Recipe(Base):
    """Модель для описания рецептов."""

    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    cook_time = Column(Integer, nullable=False)
    view_count = Column(Integer, default=0)
    description = Column(String, default='')
    components = relationship("Component", secondary=association_table, backref="recipes")


class Component(Base):
    """Модель для описания ингредиентов."""

    __tablename__ = 'components'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)

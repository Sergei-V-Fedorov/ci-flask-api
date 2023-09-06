"""
Модуль для определения схем для сериализации
сущностей БД.

Содержит схемы для сериализации ингредиентов
и рецептов.
"""

from pydantic import BaseModel, Field
from typing import List


class ComponentBase(BaseModel):
    """Схема для сериализации ингредиента."""

    name: str = Field(description="Название ингредиента")


class Component(ComponentBase):
    """Схема для сериализации ингредиента в БД."""

    id: int

    class Config:
        orm_mode = True


class RecipeBase(BaseModel):
    """Базовая схема для сериализации рецепта."""

    name: str = Field(description="Название рецепта")
    cook_time: int = Field(description="Время приготовления в минутах")
    description: str = Field(description="Описание рецепта")
    view_count: int = Field(description="Количество просмотров")
    components: List[Component] = Field(description="Список ингредиентов")


class Recipe(RecipeBase):
    """Схема для сериализации рецептов в БД."""

    id: int

    class Config:
        orm_mode = True


class RecipeBrief(BaseModel):
    """Сокращенная схема для сериализации списка рецептов."""
    name: str = Field(description="Название рецепта")
    cook_time: int = Field(description="Время приготовления в минутах")
    view_count: int = Field(description="Количество просмотров")

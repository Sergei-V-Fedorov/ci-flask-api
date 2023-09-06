"""
Описывает эндпоинты асинхронного API приложения.

Содежит эндпоинты инициализации и закрытия сессии,
отображения списка рецептов и детальной информации
о рецепте.
"""

import uvicorn
from fastapi import FastAPI
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.init_db import init
from app.database import engine, session

from app.models import Recipe, Base
import app.schemas as schemas

app = FastAPI(title='RecipeBook')


@app.on_event("startup")
async def startup():
    """Инициализация БД."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init()


@app.on_event("shutdown")
async def shutdown():
    """Закрытие сессии."""

    await session.close()
    await engine.dispose()


@app.get('/recipes/', response_model=List[schemas.RecipeBrief])
async def recipes() -> List[schemas.RecipeBrief]:
    """Отображает список рецептов."""

    stmt = select(Recipe).options(joinedload(Recipe.components)).order_by(Recipe.view_count.desc(), Recipe.cook_time)
    res = await session.execute(stmt)
    return res.scalars().unique()


@app.get('/recipe/{recipe_id}/', response_model=schemas.RecipeBase)
async def recipe_detail(recipe_id: int) -> Optional[schemas.RecipeBase]:
    """Отображает детали рецепта."""

    recipe = await session.get(Recipe, recipe_id)

    if recipe is None:
        return

    recipe.view_count += 1
    await session.commit()

    stmt = select(Recipe).where(Recipe.id == recipe_id).options(joinedload(Recipe.components))
    res = await session.execute(stmt)

    return res.scalars().unique().one()


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=4557, reload=True, workers=3)

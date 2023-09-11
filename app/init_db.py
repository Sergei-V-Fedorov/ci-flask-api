"""Модуль для инициализации таблиц базы данных."""

from sqlalchemy import select

import app.models as models
from app.database import session


async def insert_data():
    """Вставляет начальные данные в таблицы."""

    component_1 = models.Component(id=1, name="Соль")
    component_2 = models.Component(id=2, name="Яйца")
    component_3 = models.Component(id=3, name="Растительное масло")
    component_4 = models.Component(id=4, name="Помидоры")
    component_5 = models.Component(id=5, name="Колбаса")

    components = [
        component_1,
        component_2,
        component_3,
        component_4,
        component_5
    ]

    recipe_1 = models.Recipe(
        id=1,
        name="Яичница-глазунья",
        cook_time=10,
        description="Сковороду разогрейте на сильном огне. "
        "Налейте немного растительного масла. "
        "Вбейте яйцо, стараясь не повредить целостность желтка."
        "Посолить по вкусу.",
    )

    recipe_2 = models.Recipe(
        id=2,
        name="Яичница с колбасой и помидорами",
        cook_time=20,
        description="Разогрейте сковороду. Налейте немного растительного масла"
        " и выложите порезанную колбасу. Обжарить колбасу с "
        "двух сторон. Вбейте яйца. Рядом разложите помидоры."
        "Посолить по вкусу.",
    )

    recipe_1.components = [component_2, component_1, component_3]

    recipe_2.components = [
        component_2,
        component_1,
        component_3,
        component_4,
        component_5,
    ]

    components.extend([recipe_1, recipe_2])
    async with session.begin():
        session.add_all(components)
    await session.commit()


async def init():
    """
    Если таблицы пустые, вставляет начальные данные,
    иначе данные не вставляются.
    """

    async with session:
        stmt = select(models.Recipe)
        result = await session.execute(stmt)
        check_exist = result.scalar()
    if not check_exist:
        await insert_data()

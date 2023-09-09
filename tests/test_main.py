"""
Модуль тестов для эндпоинтов.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

count = 0


def test_get_recipes_list():
    """Получение списка из двух рецептов."""

    response = client.get("/recipes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_recipe_detail():
    """Проверка получения деталей рецепта."""

    response = client.get("/recipe/1/")
    assert response.status_code == 200
    assert response.json()["name"] == "Яичница-глазунья"
    global count
    count = response.json()["view_count"]


def test_increment_view_count():
    """Проверка увеличения кол-ва просмотров."""

    response = client.get("/recipe/1/")
    assert response.status_code == 200
    assert response.json()["view_count"] == count + 1

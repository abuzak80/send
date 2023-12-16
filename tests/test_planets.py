import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import DDL

import src.entities as entities
from src.database import SCHEMA_NAME, engine
from src.main import app
from src.models import CreatePlanet, Planet


@pytest.fixture(scope="session", autouse=True)
async def session_cleanup():
    yield

    async with engine.begin() as conn:
        await conn.execute(
            DDL(
                'TRUNCATE "%(schema)s"."%(table)s" CASCADE',
                {"schema": SCHEMA_NAME, "table": entities.Planet.__tablename__},
            )
        )


async def test_planet_creation():
    request = CreatePlanet(name="test", project_id=uuid.uuid4(), population_millions=1)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/planets",
            content=request.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
    assert response.status_code == 200, response.text

    planet = Planet.model_validate_json(response.content)
    assert planet.name == request.name
    assert planet.project_id == request.project_id
    assert planet.population_millions == request.population_millions
    assert planet.id is not None

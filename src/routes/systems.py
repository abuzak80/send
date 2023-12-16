import logging
from datetime import datetime
from uuid import UUID, uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .. import entities, models
from ..database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/systems", tags=["Systems"])


@router.get("", response_model=list[models.System])
async def get_systems(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(entities.System))).scalars().all()


@router.get("/{system_id}", response_model=models.System)
async def get_system(system_id: UUID, db: AsyncSession = Depends(get_db)):
    system = await db.get(entities.System, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="system not found")
    return system


async def get_supreme_commander_name(
        email: EmailStr = Query(..., description="Email of the supreme commander"),#jo email dalenge to wo name de dega jo str hoga
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://jsonplaceholder.typicode.com/users?email={email}"
        )
        if response.status_code == 200:
            user_data = response.json()
            if user_data:
                return user_data[0]["name"]
    raise HTTPException(
        status_code=404, detail=f"Supreme commander not found for email: {email}"
    )


@router.post("", response_model=models.System)
async def create_system(
        request: models.CreateSystem,
        supreme_commander_name: EmailStr = Depends(get_supreme_commander_name),#supreme_name input should be email
        db: AsyncSession = Depends(get_db),
):
    system = entities.System()
    system.id = uuid4()
    system.name = request.name
    system.supreme_commander = request.supreme_commander
    system.supreme_commander_name = supreme_commander_name
    system.date_created = datetime.now()

    db.add(system)
    await db.commit()

    return system
@router.delete("/{system_id}", response_model=models.System)
async def delete_system(
    system_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    system = await db.get(entities.System, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="system not found")

    logger.info(f"Deleting system {system.name}.")

    await db.delete(system)
    await db.commit()

    return system
@router.put("/{system_id}", response_model=models.System)
async def update_system(
    system_id: UUID, request: models.UpdateSystem,
        supreme_commander_name: EmailStr = Depends(get_supreme_commander_name),
    db: AsyncSession = Depends(get_db)
):
    system = await db.get(entities.System, system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="system not found")

    system.name = request.name
    system.supreme_commander=request.supreme_commander
    system.supreme_commander_name=supreme_commander_name


    logger.info(f"Updating planet {system.name}.")

    await db.commit()

    return system
@router.get("/system_population_sum/{system_id}")
async def get_system_population_sum(system_id: UUID, db: AsyncSession = Depends(get_db)):

    system = await db.get(models.System, system_id)

    if system is None:
        raise HTTPException(status_code=404, detail="System not found")

    query = text(f"SELECT sum(population_millions) FROM planets WHERE system_id = :system_id")

    # Execute the query and retrieve the result
    result = await db.execute(query, {"system_id": str(system_id)})
    population_sum = await result.scalar()

    return {"population_sum": population_sum}
@router.get("/get_system_by_name/{system_name}")
async def get_system_by_name(system_name: str, db: AsyncSession = Depends(get_db)):
    try:
        # Using the filter method to retrieve a System record based on the 'name' column
        system = await db.get(entities.System, {"name": system_name})
        if system is None:
            raise HTTPException(status_code=404, detail="System not found")

        return {"system_name": system.name, "system_id": system.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

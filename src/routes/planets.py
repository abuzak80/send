import logging
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import entities, models
from ..database import get_db

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/planets", tags=["Planets"])


@router.get("", response_model=list[models.Planet])
async def get_planets(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(entities.Planet))).scalars().all()


@router.get("/{planet_id}", response_model=models.Planet)
async def get_planet(planet_id: UUID, db: AsyncSession = Depends(get_db)):
    planet = await db.get(entities.Planet, planet_id)
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet



@router.post("", response_model=models.Planet)
async def create_planet(
    request: models.CreatePlanet, db: AsyncSession = Depends(get_db)
):
    system = await db.get(entities.System, request.system_id)
    if system is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    planet = entities.Planet()
    planet.id = uuid4()
    planet.name = request.name
    planet.project_id = request.project_id
    planet.population_millions = request.population_millions
    planet.system_id=request.system_id
    planet.system=system

    db.add(planet)
    await db.commit()

    return planet


@router.put("/{planet_id}", response_model=models.Planet)
async def update_planet(
    planet_id: UUID, request: models.UpdatePlanet, db: AsyncSession = Depends(get_db)
):
    planet = await db.get(entities.Planet, planet_id)
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    planet.name = request.name
    planet.population_millions = request.population_millions

    logger.info(f"Updating planet {planet.name}.")

    await db.commit()

    return planet


@router.delete("/{planet_id}", response_model=models.Planet)
async def delete_planet(
    planet_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    planet = await db.get(entities.Planet, planet_id)
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    logger.info(f"Deleting planet {planet.name}.")

    await db.delete(planet)
    await db.commit()

    return planet

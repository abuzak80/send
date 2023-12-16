import uuid
from datetime import datetime
from enum import Flag, auto

from sqlalchemy import TIMESTAMP, UUID, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import SCHEMA_NAME, Base

class System(Base):
    __tablename__ = "system"
    __table_args__ = {"schema": SCHEMA_NAME}

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    supreme_commander: Mapped[str] = mapped_column(Text, nullable=False)
    supreme_commander_name: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )



class Planet(Base):
    __tablename__ = "planets"
    __table_args__ = {"schema": SCHEMA_NAME}

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    population_millions: Mapped[int] = mapped_column(Integer, nullable=False)
    system_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(System.id, ondelete="CASCADE"), nullable=False
    )
    system: Mapped[System] = relationship(System)

class StationType(Flag):
    military = auto()
    mining = auto()


class Station(Base):
    __tablename__ = "stations"
    __table_args__ = {"schema": SCHEMA_NAME}

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    commander: Mapped[str] = mapped_column(Text, nullable=False)
    established_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    type: Mapped[StationType] = mapped_column(
        Enum(StationType, schema=SCHEMA_NAME), nullable=False
    )

    planet_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(Planet.id, ondelete="CASCADE"), nullable=False
    )
    planet: Mapped[Planet] = relationship(Planet)

from uuid import UUID

import httpx
from pydantic import BaseModel, Field

from ..auth import httpx_ssl_context
from ..settings import settings

_client = httpx.AsyncClient(
    base_url="https://localhost",
    verify=httpx_ssl_context if not settings.is_development() else False,
)


class Project(BaseModel):
    id: UUID = Field(alias="Id")
    name: str = Field(alias="Name")


async def get_project(project_id: UUID):
    response = await _client.get(url=f"projects/{project_id}")
    response.raise_for_status()

    return Project.model_validate_json(response.content)

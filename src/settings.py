from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    db_connection_string: str = Field(alias="DB_CONNECTION_STRING")
    environment: str = Field(alias="ENVIRONMENT", default="Production")

    def is_development(self) -> bool:
        return self.environment.lower() == "development"


settings = Settings()  # type: ignore

import logging

from fastapi import FastAPI

from .routes import planets, stations,systems

logger = logging.getLogger(__name__)

app = FastAPI(docs_url="/openapi", redoc_url=None)
app.include_router(systems.router)
app.include_router(planets.router)
app.include_router(stations.router)



@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"status": "healthy"}

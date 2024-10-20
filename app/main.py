from fastapi import FastAPI

from app.users.router import router as router_users
from app.builds.router import router as router_builds
from app.components.router import router as router_components
from app.clients.router import router as router_clients
from app.incidents.router import router as router_incidents

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": None}


app.include_router(router_users)
app.include_router(router_builds)
app.include_router(router_components)
app.include_router(router_clients)
app.include_router(router_incidents)

from fastapi import APIRouter

from app.users.dependencies import get_current_user
from app.builds.schemas import SBuildCreate, SUserCheck, SGetBuild
from app.builds.dao import ClientsDAO, ComponentsDAO, BuildsDAO


router = APIRouter(prefix='/builds', tags=['build'])


@router.post("/create/")
async def create_build(build: SBuildCreate):
    try:
        user_data = await get_current_user(build.key)
    except Exception as ex:
        print(ex)
        return {"status": "error", "message": "Token error"}

    client = await ClientsDAO.find_one_or_none(fio=build.client)
    if client is None:
        return {"status": "error", "message": "There is no such client in database"}

    build_data = build.dict()
    build_data["key"] = user_data.id
    build_data["client"] = client.id

    for component in build_data["components"]:
        component_object = await ComponentsDAO.find_one_or_none(name=component["title"])
        component["id"] = component_object.id

    await BuildsDAO.fill_build(build_data)

    return {"status": "ok", "message": "New build created"}


@router.post("/all/")
async def get_all_builds(user: SUserCheck):
    try:
        user_data = await get_current_user(user.key)
    except Exception as ex:
        print(ex)
        return {"status": "error", "message": "Token error"}

    builds = await BuildsDAO.find_joined_builds_by_user_id(user_id=user_data.id)

    return {"status": "ok", "message": "Successful request", "data": builds}


@router.post("/build/")
async def get_build(build: SGetBuild):
    try:
        await get_current_user(build.key)
    except Exception as ex:
        print(ex)
        return {"status": "error", "message": "Token error"}

    data = await BuildsDAO.find_joined_build_by_id(build.id)

    return {"status": "ok", "message": "Successful request", "data": data}

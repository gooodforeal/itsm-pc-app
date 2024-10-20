from fastapi import APIRouter

from app.components.dao import ComponentsDAO


router = APIRouter(prefix='/components', tags=['components'])


@router.get("/all/")
async def get_components():
    components = await ComponentsDAO.find_all()
    return {"status": "ok", "message": "Successful request", "data": components}

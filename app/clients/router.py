from fastapi import APIRouter

from app.clients.dao import ClientsDAO


router = APIRouter(prefix='/clients', tags=['clients'])


@router.get("/all/")
async def get_clients():
    clients = await ClientsDAO.find_all()
    return {"status": "ok", "message": "Successful request", "data": clients}

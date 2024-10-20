from fastapi import APIRouter

from app.incidents.dao import IncidentsDAO
from app.incidents.schemas import SCreateIncident, SEditIncident
from app.users.dao import UsersDAO

from app.users.dependencies import get_current_user

router = APIRouter(prefix='/incidents', tags=['incidents'])


@router.get("/all/")
async def get_incidents():
    incidents = await IncidentsDAO.find_all_joined()
    return {"status": "ok", "message": "Successful request", "data": incidents}


@router.post("/create/")
async def create_incidents(incident: SCreateIncident):
    incident_dict = incident.dict()
    user = await get_current_user(incident.user_id)
    incident_dict["user_id"] = user.id
    print(incident_dict)
    await IncidentsDAO.add(**incident_dict)
    return {"status": "ok", "message": "Successful incident creation!"}


@router.get("/incident/{incident_id}")
async def get_incident(incident_id: int):
    incident = await IncidentsDAO.find_one_joined_by_id(incident_id=incident_id)
    return {"status": "ok", "message": "Successful request", "data": incident}


@router.post("/edit/")
async def edit_incident(incident: SEditIncident):
    await IncidentsDAO.edit_inc_status(incident_id=incident.incident_id, incident_status=incident.status)
    return {"status": "ok", "message": "Successful incident edit!"}

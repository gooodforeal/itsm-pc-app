from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.incidents.models import Incidents
from app.users.models import Users


class IncidentsDAO(BaseDAO):
    model = Incidents

    @classmethod
    async def find_all_joined(cls):
        async with async_session_maker() as session:
            query = (
                select(Incidents)
                .options(joinedload(Incidents.user).load_only(Users.fio))
            )
            res = await session.execute(query)
            result_orm = res.unique().scalars().all()
            return result_orm

    @classmethod
    async def find_one_joined_by_id(cls, incident_id: int):
        async with async_session_maker() as session:
            query = (
                select(Incidents)
                .options(joinedload(Incidents.user).load_only(Users.fio))
                .filter(Incidents.id == incident_id)

            )
            res = await session.execute(query)
            result_orm = res.scalar_one_or_none()
            return result_orm

    @classmethod
    async def edit_inc_status(cls, incident_id: int, incident_status: str):
        async with async_session_maker() as session:
            stmt = update(Incidents).where(Incidents.id == incident_id).values(status=incident_status)
            res = await session.execute(stmt)
            await session.commit()
            return res

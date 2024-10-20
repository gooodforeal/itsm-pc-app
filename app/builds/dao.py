from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload, joinedload, load_only
from sqlalchemy import select

from app.dao.base import BaseDAO

from app.builds.models import Builds
from app.clients.models import Clients
from app.components.models import Components
from app.users.models import Users

from app.database import async_session_maker


class BuildsDAO(BaseDAO):
    model = Builds

    @classmethod
    async def fill_build(cls, data: dict):
        async with async_session_maker() as session:
            new_build = Builds(user_id=data["key"], client_id=data["client"])

            for component in data["components"]:
                get_new_component = select(Components).options(selectinload(Components.builds_replied)).filter_by(id=component["id"])
                new_component = (await session.execute(get_new_component)).scalar_one()
                new_component.builds_replied.append(new_build)

            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e

            return new_build

    @classmethod
    async def find_joined_builds_by_user_id(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Builds)
                .options(load_only(Builds.id, Builds.created_at))
                .options(joinedload(Builds.user).load_only(Users.id, Users.fio))
                .options(joinedload(Builds.client).load_only(Clients.id, Clients.fio))
                .filter(Builds.user_id == user_id)
            )
            res = await session.execute(query)
            result_orm = res.unique().scalars().all()
            return result_orm

    @classmethod
    async def find_joined_build_by_id(cls, build_id: int):
        async with async_session_maker() as session:
            query = (
                select(Builds)
                .options(load_only(Builds.id, Builds.created_at))
                .options(joinedload(Builds.user).load_only(Users.id, Users.fio))
                .options(joinedload(Builds.client).load_only(Clients.id, Clients.fio))
                .options(selectinload(Builds.components_replied).load_only(Components.type, Components.name, Components.price))
                .filter(Builds.id == build_id)
            )
            res = await session.execute(query)
            result_orm = res.unique().scalars().all()
            return result_orm




class ComponentsDAO(BaseDAO):
    model = Components


class ClientsDAO(BaseDAO):
    model = Clients

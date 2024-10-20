from app.dao.base import BaseDAO
from app.components.models import Components


class ComponentsDAO(BaseDAO):
    model = Components

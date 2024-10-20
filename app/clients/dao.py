from app.dao.base import BaseDAO
from app.clients.models import Clients


class ClientsDAO(BaseDAO):
    model = Clients

from api.dao.base import BaseDAO
from api.pois.models import POI


class POIDAO(BaseDAO):
    model = POI

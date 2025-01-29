from ..auth.authorization import Authorization as Authz
from ...services import StationsService
from ...schemas import TimeFrame
from fastapi import Query, Depends
from sqlalchemy.orm import Session
from typing import Annotated
'''
Stations Controller
this controller is in charge of datarequest
as "from this station give me all data from 9-2-2024 to 11-2-2024"
'''

template_controller = APIRouter()

service = StationsService()


@template_controller.get("/station/{station_id}/data", # return un model time serie (no creado aun)
                         dependencies=[Depends(Authz.validate_station_from_user)])
async def get_station_data(station_id: int,
                                 timeframe: Annotated[TimeFrame, Query()],
                                 db: SessionDep):
    station = service.get_station_data(station_id, timeframe, db)
    if station is None:
        raise HTTPException(404, 'Station not found!')
    return station
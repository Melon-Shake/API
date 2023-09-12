from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import session_scope
from flo_orm import ChartFloORM
from load_vibe import VibeORM

with session_scope() as session :
     
        start_time = datetime(2023, 9, 8, 0, 0, 0)
        end_time = datetime(2023, 9, 8, 23, 59, 0)
        result_flo = session.query(ChartFloORM).filter(
        ChartFloORM.created_datetime >= start_time,
        ChartFloORM.created_datetime <= end_time
    ).all()
     
        for data in result_flo:
            print(data.track_name,data.artist_name,data.album_name,data.release_ymd,data.points,data.created_datetime)



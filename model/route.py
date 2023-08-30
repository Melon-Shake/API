from pydantic import BaseModel

class Route(BaseModel):
    track_name : str
    album_name : str
    artist_name : str

# CREATE TABLE IF NOT EXISTS route (
# 	id serial,
# 	track_name name,
# 	album_name name,
# 	artist_name name,
# 	is_melonshake boolean DEFAULT false,
# 	is_spotify boolean DEFAULT false,
# 	is_itunes boolean DEFAULT false,
# 	is_genius boolean DEFAULT false,
# 	created_datetime timestamp DEFAULT current_timestamp,
# 	modified_datetime timestamp DEFAULT current_timestamp,
# 	PRIMARY KEY (id),
# 	UNIQUE (track_name, album_name, artist_name)
# )
# ;
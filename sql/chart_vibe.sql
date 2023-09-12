CREATE TABLE IF NOT EXISTS chart_vibe (
	id serial,
	track_id integer,
    track_title varchar(255),
    artist_ids integer [],
    artist_names varchar(255) [],
    album_id integer,
    album_title varchar(255),
    image_url varchar(255),
    release_date varchar(255),
    album_genres varchar(255),
    current_rank integer,
    points NUMERIC(10,3),
  	created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
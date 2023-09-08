CREATE TABLE IF NOT EXISTS chart_vibe (
	id serial,
	track_id integer,
    track_name varchar(255),
    artist_id integer,
    artist_name varchar(255),
    album_id integer,
    album_name varchar(255),
    img_url varchar(255),
    release_ymd varchar(255),
    "rank" integer,
    points NUMERIC(10,3),
  	created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
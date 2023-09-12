CREATE TABLE IF NOT EXISTS chart_bugs (
	id serial,
	track_id integer,
    track_title varchar(255),
    album_id integer,
    album_title varchar(255),
    album_image_path varchar(255),
    album_release_ymd varchar(255),
    album_release_local_ymd varchar(255),
    artist_ids integer[],
    artist_nms varchar(255) [], 
   	genres_name varchar(255), 
   	likes_count integer,
    "rank" integer,
    rank_peak integer,
    rank_last integer,
    points NUMERIC(10,3),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
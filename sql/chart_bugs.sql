--DROP TABLE IF EXISTS chart_bugs CASCADE
;
CREATE TABLE IF NOT EXISTS chart_bugs (
	id serial,
    track_name varchar(255),
    album_name varchar(255),
    img_url varchar(255),
    release_date varchar(255),
    release_local_date varchar(255),
    artist_names varchar(255) [], 
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
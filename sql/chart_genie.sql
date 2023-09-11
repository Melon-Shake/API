CREATE TABLE IF NOT EXISTS chart_genie (
	id serial,
	song_id integer,
    song_name varchar(255),
    artist_id integer,
    artist_name varchar(255),
    album_id integer,
    album_name varchar(255),
    album_img_path varchar(255),
    rank_no integer,
    pre_rank_no integer,
    points NUMERIC(10,3),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
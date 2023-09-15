--DROP TABLE IF EXISTS chart_genie CASCADE
;
CREATE TABLE IF NOT EXISTS chart_genie (
	id serial,
    track_name varchar(255),
    artist_names varchar(255),
    album_name varchar(255),
    img_url varchar(255),
    rank_no integer,
    pre_rank_no integer,
    points NUMERIC(10,3),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
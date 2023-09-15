CREATE TABLE IF NOT EXISTS chart_melon (
	id serial,
	song_name varchar(255),
	album_name varchar(255),
	album_img varchar(255),
	cur_rank integer,
	past_rank integer,
	issue_date varchar(255),
	artist_names varchar(255) [],
	genre_name varchar(255), 
    points NUMERIC(10,3),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
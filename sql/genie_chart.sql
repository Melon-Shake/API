CREATE TABLE IF NOT EXISTS genie_chart (
	song_id varchar(255),
    song_name varchar(255),
    artist_id varchar(255),
    artist_name varchar(255),
    album_id varchar(255),
    album_name varchar(255),
    album_img_path varchar(255),
    rank_no varchar(255),
    pre_rank_no varchar(255),
    created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
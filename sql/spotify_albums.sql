CREATE TABLE IF NOT EXISTS spotify_albums (
	id varchar(255),
	name varchar(255),
	uri varchar(255),
	href varchar(255),
	external_urls varchar(255),
	images_url varchar(255),
	album_type varchar(255),
	total_tracks varchar(255),
	release_date varchar(255),
	release_date_precision varchar(255),
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
CREATE TABLE IF NOT EXISTS spotify_artists (
	id varchar(255),
	name varchar(255),
	uri varchar(255),
	href varchar(255),
	external_urls varchar(255),
	images_url varchar(255),
	genres varchar(255),
	popularity varchar(255),
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
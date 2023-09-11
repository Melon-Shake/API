CREATE TABLE IF NOT EXISTS spotify_tracks (
	id varchar(255),
	name varchar(255),
	uri varchar(255),
	href varchar(255),
	external_urls varchar(255),
	duration_ms integer,
	popularity integer,
	disc_number integer,
	track_number integer,
	artists_ids varchar(255) [],
	album_id varchar(255),
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
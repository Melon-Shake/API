CREATE TABLE IF NOT EXISTS spotify_tracks (
	id varchar(255),
	name varchar(255),
	uri varchar(255),
	href varchar(255),
	external_urls varchar(255),
	duration_ms integer,
	explicit boolean,
	is_playable boolean,
	linked_form varchar(255),
	restrictions_reason varchar(255),
	available_markets varchar(255),
	popularity integer,
	preview_url varchar(255),
	disc_number integer,
	track_number integer,
	is_local boolean,
	albums_id varchar(255),
	artists_ids varchar(255),
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
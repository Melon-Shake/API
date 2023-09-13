CREATE TABLE IF NOT EXISTS lyrics (
    spotify_tracks_id varchar(255),
	content TEXT NOT NULL,
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
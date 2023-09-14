CREATE TABLE IF NOT EXISTS lyrics_temp (
    spotify_tracks_id varchar(255),
	content TEXT NOT NULL,
    romantic_words integer,
    adventurous_words integer,
    powerful_words integer,
    depressed_words integer,
    musix_match boolean,
    genius boolean,
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
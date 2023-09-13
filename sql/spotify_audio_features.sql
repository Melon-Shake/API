CREATE TABLE IF NOT EXISTS spotify_audio_features (
	track_id varchar(255),
	acousticness NUMERIC(10,5),
	danceability NUMERIC(10,5),
	energy NUMERIC(10,5),
	instrumentalness NUMERIC(10,5),
	liveness NUMERIC(10,5),
	loudness NUMERIC(10,5),
	speechiness NUMERIC(10,5),
	tempo NUMERIC(10,5),
	valence NUMERIC(10,5),
	created_datetime timestamp DEFAULT current_timestamp
)
;
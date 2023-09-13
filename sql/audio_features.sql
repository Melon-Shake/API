CREATE TABLE IF NOT EXISTS audio_features (
	track_id varchar(255),
	romantic NUMERIC(10,5) DEFAULT 0,
	adventurous NUMERIC(10,5) DEFAULT 0,
	melancholic NUMERIC(10,5) DEFAULT 0,
	powerful NUMERIC(10,5) DEFAULT 0,
	popularity NUMERIC(10,5) DEFAULT 0,
	created_datetime timestamp DEFAULT current_timestamp,
	modified_datetime timestamp DEFAULT current_timestamp
)
;
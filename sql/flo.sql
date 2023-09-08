CREATE TABLE IF NOT EXISTS flo_artists (
	id integer,
    name varchar(255),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
CREATE TABLE IF NOT EXISTS flo_albums (
	id integer,
    title varchar(255),
    release_ymd varchar(255),
    img_url varchar(255),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
CREATE TABLE IF NOT EXISTS flo_tracks (
	id integer,
    name varchar(255),
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id)
)
;
CREATE TABLE IF NOT EXISTS flo_relations (
	id integer,
    track_id integer,
    album_id integer,
    artist_id integer,
    created_datetime timestamp DEFAULT current_timestamp,
    PRIMARY KEY (id),
    FOREIGN KEY (track_id) REFERENCES flo_tracks (id),
    FOREIGN KEY (album_id) REFERENCES flo_albums (id),
    FOREIGN KEY (artist_id) REFERENCES flo_artists (id)
)
;
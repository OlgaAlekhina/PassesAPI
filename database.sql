BEGIN;

CREATE TABLE IF NOT EXISTS public.users
(
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    data_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.passes
(
    id BIGSERIAL PRIMARY KEY,
    beauty_title TEXT NOT NULL,
    title TEXT NOT NULL,
    other_titles TEXT,
    title_connect TEXT,
    data_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK(status in ('new', 'pending', 'accepted', 'rejected')),
    level_winter TEXT,
    level_spring TEXT,
    level_summer TEXT,
    level_autumn TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    height INT NOT NULL,
    user_id BIGINT REFERENCES users(id)
);


CREATE TABLE IF NOT EXISTS public.images
(
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url_path TEXT NOT NULL,
    data_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pass_id BIGINT REFERENCES passes(id)
);


END;
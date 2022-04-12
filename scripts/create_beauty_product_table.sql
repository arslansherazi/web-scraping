create table if not exists beauty_product (
	id serial primary key,
	name varchar(500) not null,
	description varchar(255) null default null,
	rating float null default 0.0,
	total_ratings int null default 0,
	price varchar(255) null default 0.0,
	image_url varchar(255) null default null,
	created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NULL DEFAULT NULL
);

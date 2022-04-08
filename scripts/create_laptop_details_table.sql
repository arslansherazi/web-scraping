create table if not exists laptop_details (
	id serial primary key,
	details text not null,
	price varchar(255) not null,
	image_url varchar(255) null default null,
	created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NULL DEFAULT NULL
);

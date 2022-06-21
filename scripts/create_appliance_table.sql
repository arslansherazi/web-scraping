create table if not exists appliance (
	id serial primary key,
	name varchar(500) not null,
	price varchar(255) null default 0.0,
	url varchar(255) null default null,
	created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(120) UNIQUE NOT NULL,
	username VARCHAR(255) UNIQUE NOT NULL,
	real_index INT DEFAULT NULL,
	last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS honeywords (
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	password_index INT NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	UNIQUE (user_id, password_index),
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs (
	id SERIAL PRIMARY KEY,
	email VARCHAR(255) NOT NULL,
	origin_ip VARCHAR(255) DEFAULT NULL,
	decoy_detected BOOLEAN NOT NULL,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
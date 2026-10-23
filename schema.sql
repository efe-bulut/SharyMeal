CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
email TEXT NOT NULL UNIQUE,
password_hash TEXT NOT NULL,
display_name TEXT NOT NULL,
role TEXT NOT NULL CHECK(role IN('recipient', 'organization')),
is_verified_organization INTEGER NOT NULL DEFAULT 0 CHECK(is_verified_organization IN(0,1)),
created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE food_listings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
organization_id INTEGER NOT NULL REFERENCES users(id),
title TEXT NOT NULL,
description TEXT NOT NULL,
food_type TEXT NOT NULL CHECK(food_type IN('prepared','packaged')),
quantity_initial INTEGER NOT NULL CHECK(quantity_initial > 0),
quantity_remaining INTEGER NOT NULL CHECK(quantity_remaining >= 0),
prepared_at TEXT,
consume_by TEXT,
collection_start TEXT NOT NULL,
collection_end TEXT NOT NULL,
location TEXT NOT NULL,
ingredients TEXT NOT NULL,
allergens TEXT,
status TEXT NOT NULL DEFAULT 'active' CHECK(status IN('active', 'cancelled', 'closed')),
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE reservations(
id INTEGER PRIMARY KEY AUTOINCREMENT,
listing_id INTEGER NOT NULL REFERENCES food_listings(id),
recipient_id INTEGER NOT NULL REFERENCES users(id),
reservation_code TEXT NOT NULL UNIQUE,
status TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
collected_at TEXT,

);

CREATE UNIQUE INDEX uq_active_reservation_per_recipient ON reservations(listing_id, recipient_id) WHERE status = 'reserved';
CREATE INDEX idx_listings_availability ON food_listings (status, collection_end);
CREATE INDEX idx_reservations_recipient ON reservations (recipient_id, status);
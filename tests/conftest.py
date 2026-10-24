import os
os.environ.setdefault('SECRET_KEY', 'test-key')

from datetime import timedelta

import pytest
from werkzeug.security import generate_password_hash

from db import connect
from init_db import init_db
from timeutil import utc_now, to_iso

PASSWORD_HASH = generate_password_hash('Password123')

@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / 'test.db'
    init_db(path)
    return path

@pytest.fixture
def db(db_path):
    conn = connect(db_path)
    yield conn
    conn.close()

@pytest.fixture
def make_user(db_path):
    def make(email='u@example.com', role='recipient', verified=0):
        conn = connect(db_path)
        try:
            return conn.execute(
                'INSERT INTO users (email, password_hash, display_name, role, is_verified_organization) '
                'VALUES (?, ?, ?, ?, ?)',
                (email, PASSWORD_HASH, 'Test', role, verified)).lastrowid
        finally:
            conn.close()
    return make

@pytest.fixture
def make_listing(db_path):
    def make(org_id, quantity = 1, **overrides):
        now = utc_now()
        values = {
            'organization_id': org_id, 'title': 'Test', 'description': '',
            'food_type': 'packaged', 'quantity_initial': quantity,
            'quantity_remaining': quantity,
            'collection_start': to_iso(now - timedelta(hours=1)),
            'collection_end': to_iso(now + timedelta(hours=5)),
            'location': 'Lefkosa', 'ingredients': 'Test', 'allergens': 'Yok',
            'status': 'active',
        }
        values.update(overrides)

        cols = ', '.join(values)
        marks = ', '.join('?' for _ in values)
        conn = connect(db_path)

        try:
            return conn.execute(
                'INSERT INTO food_listings (' + cols + ') VALUES (' + marks + ')',
                tuple(values.values())).lastrowid
        finally:
            conn.close()
    return make
            


from datetime import timedelta

from werkzeug.security import generate_password_hash

import config
from db import connect
from timeutil import utc_now, to_iso

USER_SQL = (
    'INSERT INTO users (email, password_hash, display_name, role, is_verified_organization)'
    'VALUES (?,?,?,?,?)' 
)

def seed(conn):
    password = generate_password_hash('Password123')

    org_id = conn.execute(USER_SQL,('org@example.com', password, 'Ornek Mutfak', 'organization',1)).lastrowid
    conn.execute(USER_SQL,('user@example.com', password, 'Ornek Alici', 'recipient',0))

    now = utc_now()

    conn.execute(
        'INSERT INTO food_listings(organization_id, title, description, food_type, quantity_initial, quantity_remaining,'
        'prepared_at, consume_by, collection_start, collection_end, location, ingredients, allergens)'
        'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (org_id, 'Mercimek Corbasi', 'Sicak corba', 'prepared', 5, 5, to_iso(now), to_iso(now + timedelta(hours=8)),
         to_iso(now),to_iso(now + timedelta(days=1)), 'Lefkosa, Ornek Sokak 1','Mercimek, sogan, havuc', 'Yok')
    )

if __name__ == '__main__':
    conn = connect(config.DB_PATH)
    seed(conn)
    conn.close()
    print('Seed okey. org@example.com and user@example.com, password: Password123')
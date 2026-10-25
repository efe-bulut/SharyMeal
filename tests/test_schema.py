import sqlite3
import pytest

def test_quantity_must_be_positive(make_user, make_listing):
    org = make_user('org@example.com', 'organization', 1)
    with pytest.raises(sqlite3.IntegrityError):
        make_listing(org, quantity=0)


def test_unknown_organization_is_rejected(make_listing):
    # Foreign key'ler gerçekten açık mı, Bu test onu kanıtlar.
    with pytest.raises(sqlite3.IntegrityError):
        make_listing(999)

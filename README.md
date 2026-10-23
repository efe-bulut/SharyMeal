# SharyMeal

A web platform that helps registered organizations share surplus food with people in their local communities.

> **Status:** In development. Built as a CS50x final project.

## 1. Product Overview

### 1.1 Purpose

SharyMeal lets registered organizations publish available surplus food. Visitors browse listings, and registered recipients reserve portions on a first-come, first-served basis.

A reservation is confirmed automatically when enough stock is available. Organizations do not have to evaluate individual recipients or approve reservation requests.

The goal is to make surplus food more accessible, reduce avoidable food waste, and give organizations a straightforward way to coordinate local food collection.

### 1.2 Product Principles

- **Free to use:** No payments or transaction fees.
- **Organization-led supply:** Only registered and approved organizations can publish listings.
- **Open discovery:** Anyone can browse available listings without an account.
- **First-come, first-served:** Available portions are reserved automatically.
- **Privacy-conscious collection:** A reservation code verifies collection. Staff never see the recipient's name during collection.
- **Reliable stock management:** A portion cannot be reserved by more than one person.
- **Clear food information:** Listings distinguish prepared from packaged food and show relevant dates, ingredients, allergens, and collection details.
- **Simple implementation:** A Flask monolith with SQLite, server-rendered HTML, and CSS.

### 1.3 Target Users

| User | Role |
|---|---|
| **Organizations** | Community kitchens, charities, food-sharing organizations, and similar institutions. They publish surplus food and confirm collection. New organization accounts must be approved before they can publish. |
| **Recipients** | Individuals who browse listings, reserve portions, and collect food using a reservation code. An account is required to reserve. |
| **Visitors** | Anyone. Can browse public listings and view their details without signing in. |

Individual household food providers are not supported in Version 1.0.

## 2. How It Works

1. An organization registers and is approved by an administrator.
2. The organization publishes a listing: food, quantity, ingredients, allergens, collection window, and location.
3. A recipient registers, reserves a portion, and receives a reservation code.
4. The recipient visits during the collection window and shows the code.
5. The organization enters the code to confirm collection. Each code works only once, and only for that organization's own listings.

## 3. Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3 |
| Web framework | Flask |
| Database | SQLite (via the standard `sqlite3` module, raw SQL) |
| Templates | Jinja2 (server-rendered HTML) |
| Styling | CSS |
| Forms and CSRF | Flask-WTF |
| Password hashing | Werkzeug (`generate_password_hash`) |
| Tests | pytest |

## 4. Project Structure

```
SharyMeal/
├── app.py              # Flask app and routes
├── config.py           # Configuration
├── db.py               # Database connection helpers
├── auth.py             # Login checks and role decorators
├── services.py         # Business logic (reservations, listings, validation)
├── timeutil.py         # Time zone conversions
├── init_db.py          # Creates the database from schema.sql
├── seed.py             # Creates sample data
├── schema.sql          # Tables, constraints, indexes
├── templates/          # Jinja2 templates
├── static/             # CSS
├── tests/              # pytest test suite
└── instance/           # Local SQLite database (not committed)
```

`services.py` does not depend on Flask. Its functions take a database connection as a parameter, which allows the reservation logic to be tested directly, including with concurrent threads.

## 5. Getting Started

Requirements: Python 3.11 or newer.

```powershell
# 1. Clone the repository and enter it
git clone <repository-url>
cd SharyMeal

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set a secret key (use any long random string)
$env:SECRET_KEY = "change-me-to-a-long-random-string"

# 5. Create the database and sample data
python init_db.py
python seed.py

# 6. Run the app
python app.py
```

The app runs at `http://127.0.0.1:5000`.

On macOS or Linux, use `source .venv/bin/activate` and `export SECRET_KEY="..."` instead.

### Approving an organization

New organization accounts start unverified and cannot publish listings. There is no admin panel in Version 1.0. Approve an organization directly in the database:

```sql
UPDATE users SET is_verified_organization = 1 WHERE email = 'org@example.com';
```

## 6. Running Tests

```powershell
pytest
```

The test suite covers the database constraints, the reservation logic, concurrent reservations, authentication, role permissions, and collection verification.

## 7. Design Decisions

**Why a monolith?** One developer, one deployable unit, no scaling problem that would justify splitting services. The extra complexity of microservices would cost more than it gives.

**Why SQLite?** It needs no server and no setup. Anyone can clone the repository and run it in under a minute. The expected workload is a few reservations at a time, which suits SQLite's single-writer model. The schema is plain SQL, so moving to PostgreSQL later would be straightforward. See [Limitations](#8-limitations).

**Stock integrity.** Stock is decremented with a single atomic `UPDATE ... WHERE quantity_remaining >= 1`, in the same transaction that inserts the reservation. Two simultaneous requests for the last portion cannot both succeed. A `CHECK` constraint prevents stock from ever going negative.

**One active reservation per recipient per listing.** Enforced by a partial unique index on `(listing_id, recipient_id) WHERE status = 'reserved'`, not only by application code. This holds even if two requests arrive at the same moment.

**Reservation codes.** Codes are generated with Python's `secrets` module from an alphabet without look-alike characters. A code is accepted only for listings owned by the organization entering it, and only once.

**Passwords.** Only salted hashes are stored. Plain passwords are never written to the database.

**Time.** All timestamps are stored in UTC in one ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`) and displayed in local time (Europe/Nicosia).

**Validation.** The database enforces rules where a bug would cause real damage (stock, duplicate reservations, valid statuses). Rules that need friendly error messages, such as required dates for prepared food, are validated in Python.

## 8. Limitations

- **SQLite allows one writer at a time.** It is fine for this workload but not for high traffic. Past that point, PostgreSQL is the next step.
- **No password reset.** Not part of Version 1.0.
- **No email notifications.**
- **No admin panel.** Organization approval is done manually in the database.
- **No household food providers.** Only organizations can publish.
- **Hosting requires a persistent disk.** The SQLite file must survive restarts and redeploys.

## 9. Disclaimer

SharyMeal connects people with food. It does not inspect, prepare, store, or guarantee the safety of any food. Organizations are responsible for the accuracy of their listings and for food safety. Recipients should check ingredients and allergens before consuming any food.

## Project Status

- [x] Database schema (`users`, `food_listings`, `reservations`)
- [ ] Database setup and seed scripts
- [ ] Public listing pages
- [ ] Reservation logic with concurrency tests
- [ ] Registration and login
- [ ] Role-based access control and CSRF protection
- [ ] Recipient reservation flow
- [ ] Organization listing creation
- [ ] Organization dashboard
- [ ] Collection verification
- [ ] Security review and error pages
- [ ] Final styling and deployment notes

## Author

Efe Bulut. Built as a final project for Harvard's CS50x.
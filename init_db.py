import sys
from pathlib import Path

import config
from db import connect

def init_db(path = config.DB_PATH, reset = False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if not reset:
            raise SystemExit('DB zaten var. Silip yeniden kurmak icin: python init_db.py --reset')
        path.unlink()
    schema = (Path(__file__).parent / 'schema.sql').read_text(encoding='utf-8')
    conn = connect(path)
    conn.executescript(schema)
    conn.close()
    print('Database created: ', path)

if __name__ == '__main__':
    init_db(reset='--reset' in sys.argv)
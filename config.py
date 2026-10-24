import os
from pathlib import Path

#configuration settings

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR/'instance'/'sharymeal.db'
DEBUG = os.environ.get('FLASK_DEBUG') == '1'
SECRET_KEY = os.environ.get('SECRET_KEY') or ('dev-only-key' if DEBUG else None)
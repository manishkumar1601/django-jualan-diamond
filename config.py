import os

DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
SANDBOX = os.environ.get("SANDBOX", "True") == "True"
DEBUG = os.environ.get("DEBUG", "True") == "True"
TRIPAY_API_KEY = os.environ.get("TRIPAY_API_KEY")
TRIPAY_PRIVATE_KEY = os.environ.get("TRIPAY_PRIVATE_KEY")
MERCHANT_CODE = os.environ.get("MERCHANT_CODE")
HOST = os.environ.get("HOST")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DATABASE_URI = os.environ.get("DATABASE_URI")

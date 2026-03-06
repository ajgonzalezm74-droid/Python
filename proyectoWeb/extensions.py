from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from exchange_provider import ExchangeProvider

exchange_provider = ExchangeProvider()
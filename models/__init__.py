from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .inscriptions import *                # noqa: E402, F401, F403
from .users import *                       # noqa: E402, F401, F403
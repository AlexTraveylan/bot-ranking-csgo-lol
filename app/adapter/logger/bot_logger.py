import logging

from app.core.constants import PRODUCTION

if PRODUCTION:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

import os
import logging

logger = logging.getLogger(__file__)

# load form environment (as many globals as possible shall be in
# environment configuration)
try:
    PORT = os.environ['PORT']
    API_NAME = os.environ['API_NAME']
    DB_URL = os.environ['DB_URL']
except IndexError as e:
    logger.critical('PORT API_NAME DB_URL shall be defined'
                    'as environment variables')
    raise

DEBUG = True
HYDRUS_SERVER_URL = 'http://localhost:{}/'.format(PORT)




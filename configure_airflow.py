import os
import logging

from yaml import load
from airflow import models
from airflow import settings
from airflow.models import Connection
from airflow.contrib.auth.backends.password_auth import PasswordUser

from sqlalchemy.exc import IntegrityError

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

AIRFLOW_USERNAME = os.environ.get('AIRFLOW_USERNAME')
AIRFLOW_EMAIL = os.environ.get('AIRFLOW_EMAIL')
AIRFLOW_PASSWORD = os.environ.get('AIRFLOW_PASSWORD')

user = PasswordUser(models.User())
user.username = AIRFLOW_USERNAME
user.email = AIRFLOW_EMAIL
user.password = AIRFLOW_PASSWORD

session = settings.Session()

try:
    session.add(user)
    session.commit()
    logger.info('Created user: %s (%s)', AIRFLOW_USERNAME, AIRFLOW_EMAIL)
except IntegrityError:
    session.rollback()
    logger.info('User already exists.')

with open('connections.yml', 'r') as f:
    connections = load(f)

for conn in connections['airflow']:
    try:
        new_conn = Connection(conn_id=conn['id'], conn_type=conn['type'], extra=conn['extra'])
        session.add(new_conn)
        session.commit()
        logger.info('Created new connection - %s', conn['id'])
    except IntegrityError:
        session.rollback()
        logger.info('Connection already exists.')

session.close()
exit()

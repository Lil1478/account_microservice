import configparser

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# PostgreSQL
print("Init database...")

config = configparser.ConfigParser()
config.read('configuration.ini')

host = config['postgresql']['host']
port = config['postgresql']['port']
user = config['postgresql']['user']
passwd = config['postgresql']['passwd']
db = config['postgresql']['db']


# app.add_middleware(DBSessionMiddleware,
#                    db_url='postgresql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db)

# engine = create_engine('postgresql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db,
#                        echo=True
#                        )

Base = declarative_base()
#
# SessionLocal = sessionmaker(bind=engine)


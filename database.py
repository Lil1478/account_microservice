import configparser
import os

import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


print("Init database...")

config = configparser.ConfigParser()
config.read('configuration.ini')

#local
host = config['postgresql']['host']
port = config['postgresql']['port']
user = config['postgresql']['user']
passwd = config['postgresql']['passwd']
db = config['postgresql']['db']

# db_user = "postgres"
# db_pass = "postgres"
# db_name = "shop"
# db_host="10.87.16.4"
# db_socket_dir = "/cloudsql/integrated-systems-348617:europe-west1:shop-database"
# instance_connection_name = "integrated-systems-348617:europe-west1:shop-database"

#local
engine = create_engine('postgresql://' + user + ':' + passwd + '@' + host + ':' + port + '/' + db,
                       echo=True
                       )


# print('postgresql://' + db_user + ':' + db_pass + '@' + '10.87.16.4:5432/'+db_name)
# engine = create_engine('postgresql://' + db_user + ':' + db_pass + '@' + '10.87.16.4:5432/'+db_name
#                         )


Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

